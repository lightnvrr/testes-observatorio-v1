"""Indicadores da V1 (incluindo o recorte de raça), relatório de qualidade e dicionário.

Todos os indicadores contam pessoas (soma de Totalpessoas) e trazem numerador,
denominador e número de linhas para auditoria.

Dois indicadores raciais que não podem ser confundidos:

- `participacao_feminina_no_grupo_racial`: entre as pessoas da raça R, qual %
  é mulher. Denominador: pessoas da raça R com sexo declarado.
- `composicao_racial_das_mulheres`: entre as mulheres, qual % é da raça R.
  Denominador: mulheres com raça declarada.

Duas bases temporais:

- `coorte_titulacao`: indicadores de formação, por ano da última titulação e
  no agregado do período.
- `situacao_na_extracao`: indicadores de situação atual (atuação), só no
  agregado do período. Descrevem a situação na data da extração das pessoas
  tituladas no período, um perfil de início de carreira.
"""

from dataclasses import dataclass
from datetime import date

import pandas as pd

from lattes import config

# ── Nomes ────────────────────────────────────────────────────────────────────
PARTICIPACAO = "participacao_feminina"
GRUPO_RACIAL = "participacao_feminina_no_grupo_racial"
COMPOSICAO = "composicao_racial_das_mulheres"
TAXA_ND_RACA = "taxa_nao_declaracao_raca"

BASE_COORTE = "coorte_titulacao"
BASE_SITUACAO = "situacao_na_extracao"

TODOS = "Todos"  # sexo: Feminino + Masculino
TODAS = "Todas"  # raça: sem recorte racial (inclui quem não declarou)

# Qual flag de amostra pequena vale para cada indicador.
REGRA_FLAG = {
    PARTICIPACAO: "denominador",
    GRUPO_RACIAL: "denominador",
    COMPOSICAO: "numerador",
    TAXA_ND_RACA: "denominador",
}

COLUNAS_SAIDA = [
    "indicador", "base", "periodo", "recorte", "categoria", "sexo", "raca", "raca_agregada",
    "numerador", "denominador", "percentual", "n_linhas_numerador", "n_linhas_denominador",
    "flag_denominador_pequeno", "flag_numerador_pequeno", "flag_preferir_agregado", "extracao",
]

COLUNAS_QUALIDADE = [
    "verificacao", "campo", "recorte", "periodo", "sexo", "categoria",
    "numerador", "denominador", "percentual",
]

# Campos cuja taxa de "Não informado" vai para o relatório de qualidade.
CAMPOS_NAO_INFORMADO = [
    "Grande Área (Formação)", "Área (Formação)", "Região (Formação)", "UF (Formação)",
    "Grande Área (Atuação)", "Área (Atuação)", "Região (Atuação)", "UF (Atuação)",
    "Setor de Atividade (Atuação)", "Enquadramento (Atuação)",
]

SEXO, RACA = "Sexo", "Cor ou Raça"
GA_FORMACAO, GA_ATUACAO = "Grande Área (Formação)", "Grande Área (Atuação)"
AREA_ATUACAO, REGIAO_ATUACAO = "Área (Atuação)", "Região (Atuação)"
_PESSOAS = "_pessoas"


class ErroDominio(ValueError):
    """Uma categoria usada em filtro não existe na base, ou a base tem categoria nova."""


# ── Domínios ─────────────────────────────────────────────────────────────────

def validar_dominios(df: pd.DataFrame, anos: list[int]) -> None:
    """Confere as strings de filtro contra os valores reais antes de calcular.

    Falha se a base tiver sexo, raça ou nível fora da lista conhecida, ou se
    alguma categoria usada em filtro (STEM, Computação) não existir na base.
    Isso evita que um filtro com grafia errada gere zeros em silêncio.
    """
    problemas = []

    def fora(coluna, conhecidos):
        novos = sorted(set(df[coluna]) - set(conhecidos))
        if novos:
            problemas.append(f"{coluna}: valores fora do domínio conhecido {novos}")

    fora(SEXO, [*config.SEXOS_DECLARADOS, config.SEXO_NAO_DECLARADO])
    fora(RACA, [*config.RACAS_DECLARADAS, config.RACA_NAO_DECLARADA])
    fora(config.COLUNA_NIVEL, config.NIVEIS_FORMACAO)
    fora(config.COLUNA_ANO, [str(a) for a in anos])

    for coluna in (GA_FORMACAO, GA_ATUACAO):
        ausentes = sorted(config.GRANDES_AREAS_STEM - set(df[coluna]))
        if ausentes:
            problemas.append(f"{coluna}: grandes áreas STEM ausentes da base {ausentes}")
    if config.AREA_COMPUTACAO not in set(df[AREA_ATUACAO]):
        problemas.append(f"{AREA_ATUACAO}: {config.AREA_COMPUTACAO!r} ausente da base")
    for nome, componentes in config.GRUPOS_RACIAIS_AGREGADOS.items():
        invalidos = sorted(set(componentes) - set(config.RACAS_DECLARADAS))
        if invalidos:
            problemas.append(f"grupo {nome!r}: componentes desconhecidos {invalidos}")

    if problemas:
        raise ErroDominio("; ".join(problemas))


# ── Contagem ─────────────────────────────────────────────────────────────────

def preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta a coluna numérica de pessoas (peso de cada linha)."""
    df = df.copy()
    df[_PESSOAS] = df[config.COLUNA_PESSOAS].astype(int)
    return df


def tabela(sub: pd.DataFrame) -> pd.DataFrame:
    """Pessoas e linhas por sexo e raça num recorte."""
    return sub.groupby([SEXO, RACA]).agg(pessoas=(_PESSOAS, "sum"), linhas=(_PESSOAS, "size"))


def contar(tab: pd.DataFrame, sexos, racas=None) -> tuple[int, int]:
    """(pessoas, linhas) da tabela para os sexos e raças dados."""
    mascara = tab.index.get_level_values(SEXO).isin(sexos)
    if racas is not None:
        mascara &= tab.index.get_level_values(RACA).isin(racas)
    sel = tab[mascara]
    return int(sel["pessoas"].sum()), int(sel["linhas"].sum())


def percentual(numerador: int, denominador: int) -> float | None:
    return round(100 * numerador / denominador, 2) if denominador else None


def rotulo_agregado(anos: list[int]) -> str:
    return f"{min(anos)}-{max(anos)}"


def grupos_raciais(agregar_negra: bool) -> list[tuple[str, tuple[str, ...], bool]]:
    """(nome, raças que compõem, é agregado) na ordem de saída."""
    grupos = [(r, (r,), False) for r in config.RACAS_DECLARADAS]
    if agregar_negra:
        grupos += [(nome, tuple(c), True) for nome, c in config.GRUPOS_RACIAIS_AGREGADOS.items()]
    return grupos


# ── Indicadores ──────────────────────────────────────────────────────────────

@dataclass
class Contexto:
    base: str
    periodo: str
    agregado: bool
    recorte: str
    categoria: str


class _Gerador:
    def __init__(self, extracao: str, agregar_negra: bool):
        self.extracao = extracao
        self.grupos = grupos_raciais(agregar_negra)
        self.linhas: list[dict] = []

    def linha(self, ctx: Contexto, indicador, sexo, raca, num, den, raca_agregada=False):
        (n, n_lin), (d, d_lin) = num, den
        regra = REGRA_FLAG[indicador]
        self.linhas.append({
            "indicador": indicador, "base": ctx.base, "periodo": ctx.periodo,
            "recorte": ctx.recorte, "categoria": ctx.categoria, "sexo": sexo, "raca": raca,
            "raca_agregada": raca_agregada, "numerador": n, "denominador": d,
            "percentual": percentual(n, d), "n_linhas_numerador": n_lin, "n_linhas_denominador": d_lin,
            "flag_denominador_pequeno": regra == "denominador" and d < config.LIMITE_DENOMINADOR,
            "flag_numerador_pequeno": regra == "numerador" and n < config.LIMITE_NUMERADOR,
            "flag_preferir_agregado": raca in config.RACAS_PREFERIR_AGREGADO and not ctx.agregado,
            "extracao": self.extracao,
        })

    def recorte(self, ctx: Contexto, sub: pd.DataFrame, com_raca: bool) -> None:
        tab = tabela(sub)
        F, M = config.FEMININO, config.MASCULINO
        self.linha(ctx, PARTICIPACAO, TODOS, TODAS, contar(tab, [F]), contar(tab, [F, M]))
        if not com_raca:
            return
        declaradas = config.RACAS_DECLARADAS
        for nome, racas, agregada in self.grupos:
            self.linha(ctx, GRUPO_RACIAL, TODOS, nome,
                       contar(tab, [F], racas), contar(tab, [F, M], racas), agregada)
        for nome, racas, agregada in self.grupos:
            self.linha(ctx, COMPOSICAO, F, nome,
                       contar(tab, [F], racas), contar(tab, [F], declaradas), agregada)
        for sexo, sexos in ((F, [F]), (M, [M]), (TODOS, [F, M])):
            self.linha(ctx, TAXA_ND_RACA, sexo, config.RACA_NAO_DECLARADA,
                       contar(tab, sexos, [config.RACA_NAO_DECLARADA]), contar(tab, sexos))


def categorias(df: pd.DataFrame, coluna: str) -> list[str]:
    """Valores reais da coluna, sem "Não informado" (que vai para a qualidade)."""
    return sorted(set(df[coluna]) - {config.NAO_INFORMADO})


def gerar_indicadores(
    df: pd.DataFrame,
    extracao: str,
    anos: list[int] = config.ANOS,
    agregar_negra: bool = config.AGREGAR_NEGRA,
) -> pd.DataFrame:
    """Calcula todos os indicadores da V1 a partir do consolidado."""
    validar_dominios(df, anos)
    df = preparar(df)
    g = _Gerador(extracao, agregar_negra)
    agregado = rotulo_agregado(anos)
    stem_f = df[GA_FORMACAO].isin(config.GRANDES_AREAS_STEM)
    grandes_areas = categorias(df, GA_FORMACAO)

    # Formação: por ano de titulação e no agregado
    periodos = [(str(a), df[config.COLUNA_ANO] == str(a), False) for a in anos]
    periodos.append((agregado, pd.Series(True, index=df.index), True))
    for periodo, no_periodo, eh_agregado in periodos:
        def ctx(recorte, categoria):
            return Contexto(BASE_COORTE, periodo, eh_agregado, recorte, categoria)
        g.recorte(ctx("geral", "Todas as áreas"), df[no_periodo], com_raca=True)
        g.recorte(ctx("stem_formacao", "STEM"), df[no_periodo & stem_f], com_raca=True)
        for nivel in config.NIVEIS_FORMACAO:
            g.recorte(ctx("nivel_formacao", nivel),
                      df[no_periodo & (df[config.COLUNA_NIVEL] == nivel)], com_raca=True)
        for ga in grandes_areas:
            g.recorte(ctx("grande_area_formacao", ga),
                      df[no_periodo & (df[GA_FORMACAO] == ga)], com_raca=False)

    # Situação atual: só no agregado
    def ctx_s(recorte, categoria):
        return Contexto(BASE_SITUACAO, agregado, True, recorte, categoria)
    g.recorte(ctx_s("stem_atuacao", "STEM"),
              df[df[GA_ATUACAO].isin(config.GRANDES_AREAS_STEM)], com_raca=True)
    computacao = df[df[AREA_ATUACAO] == config.AREA_COMPUTACAO]
    g.recorte(ctx_s("computacao_atuacao", config.AREA_COMPUTACAO), computacao, com_raca=False)
    for regiao in categorias(df, REGIAO_ATUACAO):
        g.recorte(ctx_s("computacao_regiao_atuacao", regiao),
                  computacao[computacao[REGIAO_ATUACAO] == regiao], com_raca=False)

    return pd.DataFrame(g.linhas, columns=COLUNAS_SAIDA)


# ── Relatório de qualidade (para a metodologia, não para o público) ──────────

def gerar_qualidade(df: pd.DataFrame, anos: list[int] = config.ANOS) -> pd.DataFrame:
    """Taxas de "Não informado", sexo não declarado e raça no grupo de sexo não declarado."""
    df = preparar(df)
    agregado = rotulo_agregado(anos)
    linhas = []

    def add(verificacao, campo, recorte, periodo, sexo, categoria, num, den):
        linhas.append({"verificacao": verificacao, "campo": campo, "recorte": recorte,
                       "periodo": periodo, "sexo": sexo, "categoria": categoria,
                       "numerador": int(num), "denominador": int(den),
                       "percentual": percentual(int(num), int(den))})

    F, M = config.FEMININO, config.MASCULINO
    computacao = df[AREA_ATUACAO] == config.AREA_COMPUTACAO
    stem_f = df[GA_FORMACAO].isin(config.GRANDES_AREAS_STEM)
    recortes = [("geral", CAMPOS_NAO_INFORMADO, pd.Series(True, index=df.index)),
                ("stem_formacao", [GA_ATUACAO], stem_f),
                ("computacao_atuacao", [REGIAO_ATUACAO], computacao)]
    periodos = [(str(a), df[config.COLUNA_ANO] == str(a)) for a in anos]
    periodos.append((agregado, pd.Series(True, index=df.index)))

    for periodo, no_periodo in periodos:
        for recorte, campos, no_recorte in recortes:
            sub = df[no_periodo & no_recorte]
            for campo in campos:
                ni = sub[campo] == config.NAO_INFORMADO
                for sexo, sexos in ((F, [F]), (M, [M]), (TODOS, [F, M])):
                    s = sub[SEXO].isin(sexos)
                    add("taxa_nao_informado", campo, recorte, periodo, sexo, config.NAO_INFORMADO,
                        sub.loc[s & ni, _PESSOAS].sum(), sub.loc[s, _PESSOAS].sum())

        sub = df[no_periodo]
        sexo_nd = sub[SEXO] == config.SEXO_NAO_DECLARADO
        add("sexo_nao_declarado", SEXO, "geral", periodo, "Todos, inclusive não declarado",
            config.SEXO_NAO_DECLARADO, sub.loc[sexo_nd, _PESSOAS].sum(), sub[_PESSOAS].sum())
        # Distribuição de raça no grupo com sexo não declarado, comparada à do sexo declarado
        for verificacao, grupo in (("raca_no_sexo_nao_declarado", sub[sexo_nd]),
                                   ("raca_no_sexo_declarado", sub[~sexo_nd])):
            for raca in [*config.RACAS_DECLARADAS, config.RACA_NAO_DECLARADA]:
                add(verificacao, RACA, "geral", periodo,
                    config.SEXO_NAO_DECLARADO if verificacao.endswith("nao_declarado") else TODOS,
                    raca, grupo.loc[grupo[RACA] == raca, _PESSOAS].sum(), grupo[_PESSOAS].sum())

    return pd.DataFrame(linhas, columns=COLUNAS_QUALIDADE)


# ── Dicionário (rótulos e ressalvas para o front) ────────────────────────────

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def _pct(valor: float) -> str:
    return f"{valor:.1f}".replace(".", ",") + "%"


def _taxa(qualidade, campo, recorte, periodo, sexo) -> float:
    sel = qualidade[(qualidade.verificacao == "taxa_nao_informado") & (qualidade.campo == campo)
                    & (qualidade.recorte == recorte) & (qualidade.periodo == periodo)
                    & (qualidade.sexo == sexo)]
    return float(sel["percentual"].iloc[0])


def gerar_dicionario(qualidade: pd.DataFrame, extracao: str, anos: list[int] = config.ANOS) -> pd.DataFrame:
    """Uma linha por indicador, base e recorte, com textos para o front.

    As ressalvas com números são montadas a partir do relatório de qualidade,
    para não haver valores fixos no código.
    """
    data = date.fromisoformat(extracao)
    quando = f"{MESES[data.month - 1]}/{data.year}"
    periodo = rotulo_agregado(anos)
    de_a = f"{min(anos)} a {max(anos)}"
    F, M = config.FEMININO, config.MASCULINO

    ga_f = _pct(_taxa(qualidade, GA_ATUACAO, "geral", periodo, F))
    ga_m = _pct(_taxa(qualidade, GA_ATUACAO, "geral", periodo, M))
    reg_f = _pct(_taxa(qualidade, REGIAO_ATUACAO, "computacao_atuacao", periodo, F))
    reg_m = _pct(_taxa(qualidade, REGIAO_ATUACAO, "computacao_atuacao", periodo, M))
    negra = " + ".join(config.GRUPOS_RACIAIS_AGREGADOS["Negra"])

    linhas = [
        # Indicadores
        ("indicador", PARTICIPACAO, "Participação feminina",
         "Percentual de mulheres entre as pessoas com sexo declarado no recorte.",
         "mulheres", "pessoas com sexo declarado (feminino ou masculino)", "denominador", ""),
        ("indicador", GRUPO_RACIAL, "Participação feminina dentro do grupo racial",
         "Entre as pessoas de cada grupo racial, o percentual que é mulher. "
         "Não confundir com a composição racial das mulheres.",
         "mulheres do grupo racial", "pessoas do grupo racial com sexo declarado", "denominador",
         f"O grupo Negra soma {negra} (convenção do IBGE) e não entra em somas com os grupos desagregados."),
        ("indicador", COMPOSICAO, "Composição racial das mulheres",
         "Entre as mulheres, o percentual de cada grupo racial. "
         "Não confundir com a participação feminina dentro do grupo racial.",
         "mulheres do grupo racial", "mulheres com raça declarada", "numerador",
         "Com poucas pessoas no numerador, variações entre anos parecem grandes mesmo com o percentual preciso."),
        ("indicador", TAXA_ND_RACA, "Taxa de não declaração de raça",
         f"Percentual de pessoas que escolheram \"{config.RACA_NAO_DECLARADA}\". "
         "Essas pessoas ficam fora dos denominadores dos indicadores raciais.",
         f"pessoas com raça \"{config.RACA_NAO_DECLARADA}\"",
         "pessoas com sexo declarado (no sexo indicado; Todos = feminino + masculino)", "denominador", ""),
        # Bases temporais
        ("base", BASE_COORTE, "Por ano de titulação",
         "Cada pessoa entra uma vez, pelo ano da última titulação (mestrado, mestrado profissional "
         f"ou doutorado). O período {periodo} agrega as coortes.", "", "", "",
         "Só inclui currículos atualizados nos últimos 60 meses."),
        ("base", BASE_SITUACAO, f"Situação em {quando} das pessoas tituladas de {de_a}",
         f"Retrato da atuação em {quando} das pessoas tituladas de {de_a}: um perfil de início de "
         "carreira, não de todas as pesquisadoras.", "", "", "", ""),
        # Recortes
        ("recorte", "geral", "Todas as áreas", "Todas as pessoas tituladas.", "", "", "", ""),
        ("recorte", "stem_formacao", "STEM (formação)",
         "Grande Área de formação: " + " ou ".join(sorted(config.GRANDES_AREAS_STEM)) + ".",
         "", "", "", "\"Tecnologias\" fica fora (não existe na Árvore do Conhecimento do CNPq)."),
        ("recorte", "nivel_formacao", "Nível de formação",
         "Última titulação: mestrado, mestrado profissional ou doutorado.", "", "", "",
         "Coortes de mestrado encolhem com o tempo, porque quem vira doutor passa para a coorte do doutorado."),
        ("recorte", "grande_area_formacao", "Grande área de formação",
         "Grande Área de formação (Árvore do Conhecimento do CNPq).", "", "", "", ""),
        ("recorte", "stem_atuacao", "STEM (atuação)",
         "Grande Área da área de atuação principal declarada no currículo: "
         + " ou ".join(sorted(config.GRANDES_AREAS_STEM)) + ".", "", "", "",
         f"Sem grande área de atuação informada: {ga_f} das mulheres e {ga_m} dos homens "
         f"titulados de {de_a}; essas pessoas ficam fora do recorte."),
        ("recorte", "computacao_atuacao", "Atuação em Computação",
         f"Área de atuação principal declarada = {config.AREA_COMPUTACAO}.", "", "", "", ""),
        ("recorte", "computacao_regiao_atuacao", "Atuação em Computação por região",
         "Região da instituição de atuação. Cobre só pessoas com vínculo de atuação registrado.",
         "", "", "",
         f"Sem região de atuação informada: {reg_f} das mulheres e {reg_m} dos homens com atuação em "
         "Computação (pode indicar desemprego ou currículo desatualizado)."),
    ]
    colunas = ["tipo", "codigo", "nome", "descricao", "numerador", "denominador",
               "flag_recomendada", "ressalva"]
    return pd.DataFrame(linhas, columns=colunas)
