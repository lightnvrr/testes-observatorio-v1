"""Testes da proposta de STEM alinhado (branch stem-alinhado, fora do pipeline da V1).

Unitários: o CSV de classificação é válido e o documento do Notion bate com ele.
Dados (`dados`): o CSV cobre exatamente as áreas da base, e os números do
documento de análise saem do script de análise.
"""

import importlib.util
import re

import pandas as pd
import pytest

from lattes import config
from lattes.consolidacao import consolidar, ler_consolidado

RAIZ = config.RAIZ
CSV = RAIZ / "data" / "referencias" / "stem_areas_lattes.csv"
DOC_NOTION = RAIZ / "docs" / "dicionario_stem_lattes.md"
DOC_ANALISE = RAIZ / "docs" / "analise_definicao_stem_lattes.md"
CLASSES = {"STEM", "não STEM", "ambígua", "não informado"}
CODIGO_CNPQ = re.compile(r"^\d\.\d{2}\.\d{2}\.\d{2}-\d( \(subárea\))?$")


def _modulo(nome):
    spec = importlib.util.spec_from_file_location(nome, RAIZ / "scripts" / f"{nome}.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


gerador = _modulo("gerar_dicionario_stem")
analise = _modulo("analisar_definicao_stem")


@pytest.fixture(scope="module")
def csv():
    return pd.read_csv(CSV, dtype=str, keep_default_na=False)


# ── CSV ──────────────────────────────────────────────────────────────────────

def test_csv_colunas_e_valores(csv):
    assert list(csv.columns) == ["area", "grande_area", "classificacao", "justificativa",
                                 "cod_correspondente", "codigo_area_cnpq"]
    assert csv.area.is_unique
    assert set(csv.classificacao) <= CLASSES
    assert (csv.justificativa.str.len() > 0).all()
    assert csv.codigo_area_cnpq.map(lambda c: c == gerador.SEM_CODIGO or bool(CODIGO_CNPQ.match(c))).all()
    assert csv.loc[csv.area == config.NAO_INFORMADO, "classificacao"].tolist() == ["não informado"]


def test_toda_area_stem_tem_grupo_da_lista_da_evellyn(csv):
    stem = csv[csv.classificacao == "STEM"]
    grupos = stem.cod_correspondente.map(gerador.grupo_da_area)
    assert grupos.notna().all()


# ── Documento do Notion ──────────────────────────────────────────────────────

def _lista_do_documento() -> dict[str, str]:
    """{área: código} das tabelas "Código | Área" da seção 2 do documento."""
    texto = DOC_NOTION.read_text(encoding="utf-8")
    secao = texto.split("## 2. Lista proposta")[1].split("## 3.")[0]
    linhas = re.findall(r"^\| (`[^`]+`|sem código) \| (.+?) \|$", secao, flags=re.M)
    return {area: codigo.strip("`") for codigo, area in linhas}


def test_documento_do_notion_esta_sincronizado_com_o_csv(csv):
    assert DOC_NOTION.read_text(encoding="utf-8") == gerador.renderizar(csv), \
        "rode python scripts/gerar_dicionario_stem.py"


def test_lista_do_notion_e_igual_as_areas_stem_do_csv(csv):
    lista = _lista_do_documento()
    stem = csv[csv.classificacao == "STEM"].set_index("area").codigo_area_cnpq.to_dict()
    assert lista == stem
    n = re.search(r"Essa lista conta com (\d+) áreas\.", DOC_NOTION.read_text(encoding="utf-8"))
    assert int(n.group(1)) == len(stem)


def test_documento_do_notion_sem_travessoes_e_sem_html():
    texto = DOC_NOTION.read_text(encoding="utf-8")
    assert "—" not in texto and "–" not in texto
    assert not re.search(r"<[a-zA-Z/]", texto)
    titulos = re.findall(r"^#+ .+$", texto, flags=re.M)
    assert [t for t in titulos if t.startswith("## ")] == [
        "## 1. Contexto", "## 2. Lista proposta", "## 3. Link de acesso à fonte"]


# ── Regra de "Não informado" ─────────────────────────────────────────────────

def test_grandes_areas_uniformes_e_mascara_alinhada():
    classificacao = pd.DataFrame({
        "area": ["Física", "Química", "Agronomia", "Medicina Veterinária", "Não informado"],
        "grande_area": ["Exatas", "Exatas", "Agrárias", "Agrárias", "Não informado"],
        "classificacao": ["STEM", "STEM", "STEM", "não STEM", "não informado"],
    })
    assert analise.grandes_areas_uniformes(classificacao) == {"Exatas": "STEM"}
    df = pd.DataFrame({
        "Área (Formação)": ["Física", "Não informado", "Não informado", "Medicina Veterinária"],
        "Grande Área (Formação)": ["Outra", "Exatas", "Agrárias", "Agrárias"],
    })
    _, alinhada = analise.mascaras(df, "formacao", classificacao)
    assert alinhada.tolist() == [True, True, False, False]


# ── Dados reais ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def consolidado(tmp_path_factory):
    saida = tmp_path_factory.mktemp("stem") / "consolidado.csv"
    consolidar(config.pasta_extracao(config.EXTRACAO), config.ANOS, saida)
    return ler_consolidado(saida)


@pytest.mark.dados
def test_csv_cobre_exatamente_as_areas_da_base(consolidado, csv):
    na_base = set(consolidado["Área (Formação)"]) | set(consolidado["Área (Atuação)"])
    no_csv = set(csv.area)
    assert not na_base - no_csv, f"áreas da base sem classificação: {sorted(na_base - no_csv)}"
    assert not no_csv - na_base, f"áreas do CSV que não existem na base: {sorted(no_csv - na_base)}"


def _br(x, casas=None) -> str:
    return f"{int(x):,}".replace(",", ".") if casas is None else f"{x:.{casas}f}".replace(".", ",")


@pytest.mark.dados
def test_numeros_da_analise_saem_do_script(consolidado, csv):
    anos = config.ANOS
    tabelas = [
        analise.indicadores_por_definicao(consolidado, csv, anos),
        analise.entram_e_saem(consolidado, csv, anos),
        analise.por_grande_area(consolidado, csv, anos),
        analise.regra_nao_informado(consolidado, csv, anos),
        analise.sensibilidade(consolidado, csv, anos),
    ]
    valores = set()
    for t in tabelas:
        for coluna in ("numerador", "denominador", "mulheres", "pessoas"):
            if coluna in t:
                valores |= {_br(v) for v in t[coluna]}
        for coluna in ("percentual", "percentual_feminino", "contribuicao_pp"):
            if coluna in t:
                valores |= {_br(v, 2) for v in t[coluna].dropna()}
    # totais de quem entra e sai e diferenças entre as definições
    es = tabelas[1]
    for _, g in es.groupby(["lado", "movimento"]):
        valores |= {_br(g.mulheres.sum()), _br(g.pessoas.sum())}
    part = tabelas[0][tabelas[0].indicador == "participacao_feminina"]
    largo = part.pivot_table(index=["recorte", "periodo"], columns="definicao", values="percentual")
    valores |= {_br(d, 2) for d in (largo.alinhada - largo.v1)}
    # regra de "Não informado" somada por tratamento e volume dos casos ambíguos
    valores |= {_br(v) for v in tabelas[3].groupby(["lado", "tratamento"]).pessoas.sum()}
    volume = analise.volume_por_area(consolidado, analise.casos_decididos(csv), anos)
    valores |= {_br(v) for v in volume.to_numpy().ravel()}
    # não-aninhagem
    n = analise.nao_aninhagem(consolidado, anos)
    for _, g in n.groupby("lado"):
        fora = g.loc[~g.predominante, "pessoas"].sum()
        valores |= {_br(fora), _br(g.pessoas.sum()), _br(100 * fora / g.pessoas.sum(), 2)}
    valores |= {_br(v) for v in n.pessoas}

    numeros = set(re.findall(r"\d{1,3}(?:\.\d{3})+|\d+,\d+", DOC_ANALISE.read_text(encoding="utf-8")))
    assert not numeros - valores, f"números que não saem do script: {sorted(numeros - valores)}"
