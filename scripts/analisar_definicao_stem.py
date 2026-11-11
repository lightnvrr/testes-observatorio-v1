"""Compara a definição de STEM da V1 com a definição alinhada à PNADC (proposta).

Fora do pipeline: não altera config.py, os indicadores nem data/processed/indicadores/.

- Definição da V1 ("STEM estrito"): Grande Área ∈ config.GRANDES_AREAS_STEM.
- Definição alinhada ("STEM alinhado"): Área classificada como STEM em
  data/referencias/stem_areas_lattes.csv. Registros com Área "Não informado"
  entram só se a grande área for uniformemente STEM (todas as suas áreas STEM).

Usa as mesmas contagens e flags dos indicadores da V1 (lattes.indicadores).

Uso:
    python scripts/analisar_definicao_stem.py

Grava tabelas em data/processed/analise_stem/ e imprime um resumo.
"""

import sys
from pathlib import Path

import pandas as pd

from lattes import config
from lattes import indicadores as ind
from lattes.consolidacao import ler_consolidado

ARQUIVO_CLASSIFICACAO = config.RAIZ / "data" / "referencias" / "stem_areas_lattes.csv"
PASTA_SAIDA = config.PASTA_PROCESSED / "analise_stem"
STEM = "STEM"
LADOS = {"formacao": "Formação", "atuacao": "Atuação"}
F, M = config.FEMININO, config.MASCULINO


def carregar_classificacao(caminho: Path = ARQUIVO_CLASSIFICACAO) -> pd.DataFrame:
    return pd.read_csv(caminho, dtype=str, keep_default_na=False)


def grandes_areas_uniformes(classificacao: pd.DataFrame) -> dict[str, str]:
    """Grandes áreas em que todas as áreas têm a mesma classificação, e qual é ela."""
    com_area = classificacao[classificacao.area != config.NAO_INFORMADO]
    por_ga = com_area.groupby("grande_area").classificacao.agg(lambda c: set(c))
    return {ga: next(iter(c)) for ga, c in por_ga.items() if len(c) == 1}


def mascaras(df: pd.DataFrame, lado: str, classificacao: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """(V1, alinhada) para o lado ("formacao" ou "atuacao")."""
    area, ga = df[f"Área ({LADOS[lado]})"], df[f"Grande Área ({LADOS[lado]})"]
    v1 = ga.isin(config.GRANDES_AREAS_STEM)
    areas_stem = set(classificacao.loc[classificacao.classificacao == STEM, "area"])
    ga_stem = {g for g, c in grandes_areas_uniformes(classificacao).items() if c == STEM}
    alinhada = area.isin(areas_stem) | ((area == config.NAO_INFORMADO) & ga.isin(ga_stem))
    return v1, alinhada


def _periodos(df: pd.DataFrame, lado: str, anos: list[int]):
    """Mesmas bases temporais da V1: formação por ano e agregado; atuação só agregado."""
    todos = pd.Series(True, index=df.index)
    agregado = ind.rotulo_agregado(anos)
    if lado == "formacao":
        for a in anos:
            yield ind.BASE_COORTE, str(a), False, df[config.COLUNA_ANO] == str(a)
        yield ind.BASE_COORTE, agregado, True, todos
    else:
        yield ind.BASE_SITUACAO, agregado, True, todos


def indicadores_por_definicao(df: pd.DataFrame, classificacao: pd.DataFrame, anos: list[int]) -> pd.DataFrame:
    """Participação feminina, grupos raciais, composição racial e não declaração, nas duas definições."""
    df = df[df[config.COLUNA_ANO].isin([str(a) for a in anos])]
    preparado = ind.preparar(df)
    g = ind._Gerador(config.EXTRACAO, config.AGREGAR_NEGRA)
    for lado in LADOS:
        v1, alinhada = mascaras(preparado, lado, classificacao)
        for base, periodo, agregado, no_periodo in _periodos(preparado, lado, anos):
            for nome, mascara in (("v1", v1), ("alinhada", alinhada)):
                ctx = ind.Contexto(base, periodo, agregado, f"stem_{lado}", nome)
                g.recorte(ctx, preparado[no_periodo & mascara], com_raca=True)
    saida = pd.DataFrame(g.linhas, columns=ind.COLUNAS_SAIDA)
    return saida.rename(columns={"categoria": "definicao"})


def entram_e_saem(df: pd.DataFrame, classificacao: pd.DataFrame, anos: list[int]) -> pd.DataFrame:
    """Pessoas que entram ou saem do recorte com a troca, por área (agregado do período).

    `contribuicao_pp` decompõe exatamente a diferença de participação feminina:
    soma das contribuições = alinhada menos V1, em pontos percentuais.
    """
    df = df[df[config.COLUNA_ANO].isin([str(a) for a in anos]) & df["Sexo"].isin([F, M])]
    df = ind.preparar(df)
    linhas = []
    for lado, nome in LADOS.items():
        v1, alinhada = mascaras(df, lado, classificacao)
        p_v1 = df.loc[v1 & (df.Sexo == F), "_pessoas"].sum() / df.loc[v1, "_pessoas"].sum()
        total_alinhada = df.loc[alinhada, "_pessoas"].sum()
        area, ga = df[f"Área ({nome})"], df[f"Grande Área ({nome})"]
        rotulo = area.where(area != config.NAO_INFORMADO, area + " (" + ga + ")")
        for movimento, mascara, sinal in (("entra", alinhada & ~v1, 1), ("sai", v1 & ~alinhada, -1)):
            sub = df[mascara]
            for r, grupo in sub.groupby(rotulo[mascara]):
                mulheres = int(grupo.loc[grupo.Sexo == F, "_pessoas"].sum())
                pessoas = int(grupo["_pessoas"].sum())
                linhas.append({
                    "lado": lado, "movimento": movimento, "area": r,
                    "grande_area": grupo[f"Grande Área ({nome})"].mode().iloc[0],
                    "mulheres": mulheres, "pessoas": pessoas,
                    "percentual_feminino": ind.percentual(mulheres, pessoas),
                    "contribuicao_pp": round(100 * sinal * (mulheres - p_v1 * pessoas) / total_alinhada, 2),
                })
    return pd.DataFrame(linhas).sort_values(["lado", "movimento", "contribuicao_pp"], ascending=[True, True, False])


def por_grande_area(df: pd.DataFrame, classificacao: pd.DataFrame, anos: list[int]) -> pd.DataFrame:
    """Participação feminina por grande área dentro da definição alinhada (agregado)."""
    df = df[df[config.COLUNA_ANO].isin([str(a) for a in anos]) & df["Sexo"].isin([F, M])]
    df = ind.preparar(df)
    linhas = []
    for lado, nome in LADOS.items():
        _, alinhada = mascaras(df, lado, classificacao)
        sub = df[alinhada]
        for ga, grupo in sub.groupby(f"Grande Área ({nome})"):
            mulheres = int(grupo.loc[grupo.Sexo == F, "_pessoas"].sum())
            pessoas = int(grupo["_pessoas"].sum())
            linhas.append({"lado": lado, "grande_area": ga, "mulheres": mulheres, "pessoas": pessoas,
                           "percentual_feminino": ind.percentual(mulheres, pessoas),
                           "flag_denominador_pequeno": pessoas < config.LIMITE_DENOMINADOR})
    return pd.DataFrame(linhas).sort_values(["lado", "pessoas"], ascending=[True, False])


def volume_por_area(df: pd.DataFrame, areas: list[str], anos: list[int]) -> pd.DataFrame:
    """Pessoas com sexo declarado por área, sexo e lado (agregado), para as áreas dadas."""
    df = df[df[config.COLUNA_ANO].isin([str(a) for a in anos]) & df["Sexo"].isin([F, M])]
    df = ind.preparar(df)
    linhas = []
    for lado, nome in LADOS.items():
        sub = df[df[f"Área ({nome})"].isin(areas)]
        for (area, sexo), pessoas in sub.groupby([f"Área ({nome})", "Sexo"])["_pessoas"].sum().items():
            linhas.append({"lado": lado, "area": area, "sexo": sexo, "pessoas": int(pessoas)})
    t = pd.DataFrame(linhas, columns=["lado", "area", "sexo", "pessoas"])
    return t.pivot_table(index="area", columns=["lado", "sexo"], values="pessoas", aggfunc="sum", fill_value=0)


def regra_nao_informado(df: pd.DataFrame, classificacao: pd.DataFrame, anos: list[int]) -> pd.DataFrame:
    """Pessoas com Área "Não informado", pelo tratamento que a grande área recebe."""
    df = df[df[config.COLUNA_ANO].isin([str(a) for a in anos]) & df["Sexo"].isin([F, M])]
    df = ind.preparar(df)
    uniformes = grandes_areas_uniformes(classificacao)
    linhas = []
    for lado, nome in LADOS.items():
        sub = df[df[f"Área ({nome})"] == config.NAO_INFORMADO]
        for ga, pessoas in sub.groupby(f"Grande Área ({nome})")["_pessoas"].sum().items():
            if ga == config.NAO_INFORMADO:
                tratamento = "fora: grande área também não informada"
            elif ga in uniformes:
                tratamento = "entra: grande área uniforme STEM" if uniformes[ga] == STEM else "fora: grande área uniforme não STEM"
            else:
                tratamento = "fora: grande área mista"
            linhas.append({"lado": lado, "grande_area": ga, "tratamento": tratamento, "pessoas": int(pessoas)})
    return pd.DataFrame(linhas)


def nao_aninhagem(df: pd.DataFrame, anos: list[int]) -> pd.DataFrame:
    """Pessoas por área e grande área, marcando quem está fora da grande área predominante da área."""
    df = df[df[config.COLUNA_ANO].isin([str(a) for a in anos]) & df["Sexo"].isin([F, M])]
    df = ind.preparar(df)
    partes = []
    for lado, nome in LADOS.items():
        area, ga = f"Área ({nome})", f"Grande Área ({nome})"
        t = df[df[area] != config.NAO_INFORMADO].groupby([area, ga])["_pessoas"].sum().reset_index()
        t.columns = ["area", "grande_area", "pessoas"]
        predominante = t.sort_values("pessoas").groupby("area").tail(1).set_index("area").grande_area
        t["predominante"] = t.area.map(predominante) == t.grande_area
        t["lado"] = lado
        partes.append(t)
    return pd.concat(partes, ignore_index=True)[["lado", "area", "grande_area", "pessoas", "predominante"]]


def casos_decididos(classificacao: pd.DataFrame) -> list[str]:
    """Áreas que eram ambíguas (decididas ou pendentes), pela justificativa no CSV."""
    return list(classificacao.loc[classificacao.justificativa.str.startswith(("Caso ambíguo", "Pendente")), "area"])


def sensibilidade(df: pd.DataFrame, classificacao: pd.DataFrame, anos: list[int]) -> pd.DataFrame:
    """Participação feminina no agregado se cada caso decidido tivesse a classificação oposta."""
    df = df[df[config.COLUNA_ANO].isin([str(a) for a in anos]) & df["Sexo"].isin([F, M])]
    df = ind.preparar(df)
    linhas = []
    for area in casos_decididos(classificacao):
        atual = classificacao.loc[classificacao.area == area, "classificacao"].iloc[0]
        alternativa = classificacao.copy()
        alternativa.loc[alternativa.area == area, "classificacao"] = "não STEM" if atual == STEM else STEM
        for lado in LADOS:
            _, alinhada = mascaras(df, lado, alternativa)
            sub = df[alinhada]
            mulheres, pessoas = int(sub.loc[sub.Sexo == F, "_pessoas"].sum()), int(sub["_pessoas"].sum())
            linhas.append({"area": area, "classificacao_atual": atual, "lado": lado, "mulheres": mulheres,
                           "pessoas": pessoas, "percentual_feminino": ind.percentual(mulheres, pessoas)})
    return pd.DataFrame(linhas)


def main() -> int:
    if not config.ARQUIVO_CONSOLIDADO.exists():
        print("[ERRO] consolidado não encontrado. Rode scripts/consolidar_lattes.py.", file=sys.stderr)
        return 1
    df = ler_consolidado()
    classificacao = carregar_classificacao()
    tabelas = {
        "indicadores": indicadores_por_definicao(df, classificacao, config.ANOS),
        "entram_e_saem": entram_e_saem(df, classificacao, config.ANOS),
        "por_grande_area": por_grande_area(df, classificacao, config.ANOS),
        "regra_nao_informado": regra_nao_informado(df, classificacao, config.ANOS),
        "nao_aninhagem": nao_aninhagem(df, config.ANOS),
    }
    tabelas["sensibilidade"] = sensibilidade(df, classificacao, config.ANOS)
    volume = volume_por_area(df, casos_decididos(classificacao), config.ANOS)
    volume.columns = [f"{lado}_{sexo}" for lado, sexo in volume.columns]
    tabelas["volume_casos_ambiguos"] = volume.reset_index()
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, tabela in tabelas.items():
        tabela.to_csv(PASTA_SAIDA / f"{nome}.csv", index=False, encoding="utf-8")

    agregado = ind.rotulo_agregado(config.ANOS)
    i = tabelas["indicadores"]
    part = i[(i.indicador == ind.PARTICIPACAO)].pivot_table(
        index=["recorte", "periodo"], columns="definicao", values="percentual", aggfunc="first")
    print("Participação feminina (%), V1 x alinhada:")
    print(part.to_string())
    uniformes = grandes_areas_uniformes(classificacao)
    print("\nGrandes áreas uniformes:", uniformes)
    es = tabelas["entram_e_saem"]
    for lado in LADOS:
        print(f"\nMaiores contribuições para a diferença ({lado}, {agregado}):")
        top = es[es.lado == lado].reindex(es[es.lado == lado].contribuicao_pp.abs().sort_values(ascending=False).index)
        print(top.head(5)[["movimento", "area", "pessoas", "percentual_feminino", "contribuicao_pp"]].to_string(index=False))
    print(f"\nTabelas em {PASTA_SAIDA.relative_to(config.RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
