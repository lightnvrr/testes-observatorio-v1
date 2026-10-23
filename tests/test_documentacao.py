"""Coerência da documentação com o código e com as saídas.

Unitários (sem dados): todo número da metodologia está mapeado em
numeros_metodologia_v1.md, os links relativos resolvem e não há travessões.
Dados (`dados`): todo número citado nos documentos da V1 aparece entre os
valores calculados a partir da extração de referência.
"""

import json
import re
from pathlib import Path

import pytest

from lattes import config
from lattes import indicadores as ind
from lattes.consolidacao import consolidar, ler_bolsas, ler_consolidado

DOCS = config.RAIZ / "docs"
METODOLOGIA = DOCS / "metodologia_lattes.md"
MAPA = DOCS / "numeros_metodologia_v1.md"
# Documentos da V1 que citam números da base
COM_NUMEROS = [METODOLOGIA, DOCS / "registro_decisoes_v1.md", DOCS / "perguntas_cnpq.md",
               DOCS / "integracao_observatorio.md"]
# Documentos revisados (o histórico fica como foi entregue)
REVISADOS = [p for p in DOCS.glob("*.md")] + [config.RAIZ / n for n in ("README.md", "CHANGELOG.md", "CLAUDE.md")]

# Números com separador de milhar (430.305) ou casa decimal (34,66)
NUMERO = re.compile(r"\d{1,3}(?:\.\d{3})+|\d+,\d+")
LINK = re.compile(r"\]\(([^)#]+)(?:#[^)]*)?\)")


def numeros(caminho: Path) -> set[str]:
    return set(NUMERO.findall(caminho.read_text(encoding="utf-8")))


# ── Unitários ────────────────────────────────────────────────────────────────

def test_todo_numero_da_metodologia_esta_mapeado():
    faltando = sorted(numeros(METODOLOGIA) - numeros(MAPA))
    assert not faltando, f"números sem origem em {MAPA.name}: {faltando}"


@pytest.mark.parametrize("caminho", REVISADOS, ids=lambda p: p.name)
def test_links_relativos_resolvem(caminho):
    for alvo in LINK.findall(caminho.read_text(encoding="utf-8")):
        if alvo.startswith(("http://", "https://", "mailto:")):
            continue
        assert (caminho.parent / alvo).exists(), f"{caminho.name}: link quebrado para {alvo}"


@pytest.mark.parametrize("caminho", REVISADOS, ids=lambda p: p.name)
def test_sem_travessoes(caminho):
    texto = caminho.read_text(encoding="utf-8")
    assert "—" not in texto and "–" not in texto


# ── Dados reais ──────────────────────────────────────────────────────────────

def _br_int(n) -> str:
    return f"{int(n):,}".replace(",", ".")


def _br_dec(x, casas) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


@pytest.fixture(scope="module")
def valores_calculados(tmp_path_factory) -> set[str]:
    """Todos os valores que os documentos podem citar, recalculados do zero."""
    pasta = config.pasta_extracao(config.EXTRACAO)
    saida = tmp_path_factory.mktemp("doc") / "consolidado.csv"
    resumo = consolidar(pasta, config.ANOS, saida)
    df = ler_consolidado(saida)
    indicadores = ind.gerar_indicadores(df, config.EXTRACAO, config.ANOS)
    qualidade = ind.gerar_qualidade(df, config.ANOS, bolsas=ler_bolsas(pasta, config.ANOS))
    manifest = json.loads((pasta / config.NOME_MANIFEST).read_text(encoding="utf-8"))

    valores = {_br_int(resumo.n_linhas), _br_int(resumo.n_pessoas)}
    for tabela in (indicadores, qualidade):
        valores |= {_br_int(n) for n in tabela.numerador} | {_br_int(d) for d in tabela.denominador}
        valores |= {_br_dec(p, 2) for p in tabela.percentual.dropna()}
    for entrada in manifest["anos"].values():
        valores |= {_br_int(entrada["n_linhas"]), _br_int(entrada["n_pessoas"]),
                    _br_dec(entrada["tamanho_bytes"] / 1e6, 1)}
    return valores


@pytest.mark.dados
@pytest.mark.parametrize("caminho", COM_NUMEROS, ids=lambda p: p.name)
def test_numeros_citados_batem_com_as_saidas(caminho, valores_calculados):
    nao_encontrados = sorted(numeros(caminho) - valores_calculados)
    assert not nao_encontrados, f"{caminho.name}: números que não saem das saídas atuais {nao_encontrados}"
