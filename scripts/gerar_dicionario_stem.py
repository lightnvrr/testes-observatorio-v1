"""Gera docs/dicionario_stem_lattes.md (documento do Notion) a partir do CSV de classificação.

Fora do pipeline. A fonte única é data/referencias/stem_areas_lattes.csv: o
documento não deve ser editado à mão; edite o CSV e rode de novo.

Uso:
    python scripts/gerar_dicionario_stem.py
"""

import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO_CLASSIFICACAO = RAIZ / "data" / "referencias" / "stem_areas_lattes.csv"
ARQUIVO_DOC = RAIZ / "docs" / "dicionario_stem_lattes.md"

URL_PAINEL = "http://bi.cnpq.br/painel/formacao-atuacao-lattes/"
URL_TABELA = ("http://lattes.cnpq.br/documents/11871/24930/TabeladeAreasdoConhecimento.pdf/"
              "d192ff6b-3e0a-4074-a74d-c280521bd5f7")
SEM_CODIGO = "sem código"

# Códigos das grandes áreas na Tabela de Áreas do Conhecimento (relatório de 30/06/2025)
CODIGO_GRANDE_AREA = {
    "Ciências Exatas e da Terra": "1.00.00.00-3",
    "Ciências Biológicas": "2.00.00.00-6",
    "Engenharias": "3.00.00.00-9",
    "Ciências da Saúde": "4.00.00.00-1",
    "Ciências Agrárias": "5.00.00.00-4",
    "Ciências Sociais Aplicadas": "6.00.00.00-7",
    "Ciências Humanas": "7.00.00.00-0",
    "Lingüística, Letras e Artes": "8.00.00.00-2",
    "Outra": "9.00.00.00-5",
}

# Grupos da lista, na mesma ordem da lista da Evellyn, pelo subgrupo da COD
GRUPOS = [
    ("2.1 Ciências físicas, químicas, geociências e astronomia", ("211",)),
    ("2.2 Matemática e estatística", ("212",)),
    ("2.3 Ciências biológicas e agrárias", ("213",)),
    ("2.4 Engenharias", ("214", "215", "216")),
    ("2.5 Computação e tecnologia da informação", ("25",)),
]

# Problema de cada grande área mista (texto da tabela "Mistura | Problema")
PROBLEMAS = {
    "Ciências Agrárias": "Na COD, veterinários ficam em profissionais da saúde (`2250`), fora do STEM.",
    "Ciências Sociais Aplicadas": "Na COD, demógrafos podem estar em `2120` (STEM) ou `2632` (não STEM); a confirmar.",
    "Outra": "Grande área residual do CNPq, para áreas sem lugar na Árvore; mistura engenharias novas com áreas interdisciplinares.",
    "Tecnologias": "Não existe na Tabela de Áreas do Conhecimento; abarca sobretudo especialidades próximas das Engenharias.",
}
ACAO = {"STEM": "manter", "não STEM": "excluir", "ambígua": "a decidir"}


def carregar(caminho: Path = ARQUIVO_CLASSIFICACAO) -> pd.DataFrame:
    return pd.read_csv(caminho, dtype=str, keep_default_na=False)


def grupo_da_area(cod_correspondente: str) -> str:
    primeiro = re.search(r"\d{4}", cod_correspondente)
    if not primeiro:
        raise ValueError(f"área STEM sem código COD: {cod_correspondente!r}")
    for titulo, prefixos in GRUPOS:
        if primeiro.group().startswith(prefixos):
            return titulo
    raise ValueError(f"código COD fora dos grupos STEM: {cod_correspondente!r}")


def _lista(nomes) -> str:
    nomes = [f"`{n}`" for n in nomes]
    return nomes[0] if len(nomes) == 1 else ", ".join(nomes[:-1]) + " e " + nomes[-1]


def renderizar(c: pd.DataFrame) -> str:
    com_area = c[c.area != "Não informado"]
    por_ga = com_area.groupby("grande_area").classificacao.agg(set)
    uniformes_stem = [ga for ga, cl in por_ga.items() if cl == {"STEM"}]
    uniformes_fora = [ga for ga, cl in por_ga.items() if cl == {"não STEM"} and ga in CODIGO_GRANDE_AREA]
    mistas = [ga for ga in PROBLEMAS if ga in por_ga and len(por_ga[ga]) > 1]
    stem = c[c.classificacao == "STEM"].copy()
    stem["grupo"] = stem.cod_correspondente.map(grupo_da_area)

    l = ["# Lattes: dicionário de áreas STEM", ""]
    l.append("No Lattes, a área de formação e a de atuação são registradas pela Tabela de Áreas do "
             "Conhecimento do CNPq. Para o observatório de dados é necessário definir quais áreas serão "
             "consideradas STEM. Este documento se propõe a fazer isso, seguindo o mesmo critério usado "
             "para as ocupações da PNADC.")
    l += ["", "## 1. Contexto", ""]
    l.append("A Tabela de Áreas do Conhecimento possui 4 níveis hierárquicos (Grande Área, Área, Subárea e "
             "Especialidade). A base Lattes traz só os dois primeiros. Das grandes áreas, as únicas cujo "
             "conteúdo é STEM por definição são:")
    l += ["", "| Código | Nome |", "| --- | --- |"]
    l += [f"| `{CODIGO_GRANDE_AREA[ga]}` | {ga} |" for ga in sorted(uniformes_stem, key=CODIGO_GRANDE_AREA.get)]
    fora = [f"**{ga}**" for ga in sorted(uniformes_fora, key=CODIGO_GRANDE_AREA.get)]
    l += ["", "Dessa forma, ficaram de fora por não serem STEM: " + ", ".join(fora[:-1]) + " e " + fora[-1] + "."]
    l += ["", "Para a classificação do que é STEM será usada apenas a Área, pois ela corresponde à forma mais "
          "especificada disponível na base. Além disso, há grandes áreas que englobam áreas STEM e não STEM:"]
    l += ["", "| Grande área | Mistura | Problema |", "| --- | --- | --- |"]
    for ga in mistas:
        partes = []
        for classe in ("STEM", "ambígua", "não STEM"):
            areas = sorted(com_area[(com_area.grande_area == ga) & (com_area.classificacao == classe)].area)
            if areas:
                partes.append(f"{_lista(areas)} ({ACAO[classe]})")
        codigo = CODIGO_GRANDE_AREA.get(ga)
        nome = f"`{codigo}` {ga}" if codigo else f"{ga} (sem código)"
        l.append(f"| {nome} | {'; '.join(partes)} | {PROBLEMAS[ga]} |")
    l += [""]
    l.append("- **Área \"Não informado\":** usa-se a Grande Área só quando todas as suas áreas têm a mesma "
             "classificação; nas grandes áreas mistas, o registro fica fora.")
    l.append("- **Só mestres e doutores:** o Lattes não tem equivalente aos técnicos de nível médio da COD "
             "(subgrupos `31` e `35`).")
    l.append("- **Nomes das áreas:** estão exatamente como na base, inclusive sem acento quando a base não tem "
             "(ex.: `Engenharia Cartografica`).")
    l += ["", "## 2. Lista proposta", "", f"Essa lista conta com {len(stem)} áreas."]
    for titulo, _ in GRUPOS:
        g = stem[stem.grupo == titulo].copy()
        g["ordem"] = g.codigo_area_cnpq.where(g.codigo_area_cnpq != SEM_CODIGO, "~")
        l += ["", f"### {titulo}", "", "| Código | Área |", "| --- | --- |"]
        for _, r in g.sort_values(["ordem", "area"]).iterrows():
            cod = r.codigo_area_cnpq if r.codigo_area_cnpq == SEM_CODIGO else f"`{r.codigo_area_cnpq}`"
            l.append(f"| {cod} | {r.area} |")
    l += ["", "## 3. Link de acesso à fonte", "", "| Recurso | Origem |", "| --- | --- |"]
    l.append(f"| Painel de Formação e Atuação do Lattes (CNPq) | [{URL_PAINEL}]({URL_PAINEL}) |")
    l.append(f"| Tabela de Áreas do Conhecimento (CNPq, relatório de 30/06/2025) | [TabeladeAreasdoConhecimento.pdf]({URL_TABELA}) |")
    l.append("| Dicionário de ocupações STEM da PNADC | Documento \"PNADC: Dicionário de ocupações STEM\", da equipe do observatório |")
    return "\n".join(l) + "\n"


def main() -> int:
    ARQUIVO_DOC.write_text(renderizar(carregar()), encoding="utf-8")
    print(f"Gravado {ARQUIVO_DOC.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
