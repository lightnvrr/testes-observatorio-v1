"""Configuração central do pipeline Lattes (KatieNet / Observatório de Mulheres na Ciência).

Tudo que define o escopo da análise fica aqui: anos, caminhos, colunas e a
definição de STEM. Mudanças neste arquivo alteram os indicadores publicados,
então só devem ser feitas com decisão registrada na metodologia.

Este módulo não contém números esperados (contagens, percentuais). Valores de
referência para conferência ficam apenas em tests/referencias/.
"""

from pathlib import Path

# ── Caminhos ─────────────────────────────────────────────────────────────────
RAIZ = Path(__file__).resolve().parents[2]
PASTA_DATA = RAIZ / "data"
PASTA_RAW = PASTA_DATA / "raw"
PASTA_PROCESSED = PASTA_DATA / "processed"
PASTA_INDICADORES = PASTA_PROCESSED / "indicadores"
PASTA_REFERENCIAS = RAIZ / "tests" / "referencias"

# Downloads em andamento (antes de sabermos a data de extração do arquivo)
PASTA_BAIXANDO = PASTA_RAW / "_baixando"
# Arquivos baixados à mão, que o script de download valida e organiza
PASTA_ENTRADA_MANUAL = PASTA_RAW / "_entrada"

ARQUIVO_CONSOLIDADO = PASTA_PROCESSED / "lattes_consolidado.csv"
NOME_MANIFEST = "manifest.json"

# Saídas da etapa de indicadores (consumidas pelo front e pela metodologia)
ARQUIVO_INDICADORES = PASTA_INDICADORES / "indicadores_v1.csv"
ARQUIVO_DICIONARIO = PASTA_INDICADORES / "indicadores_dicionario.csv"
ARQUIVO_INDICADORES_META = PASTA_INDICADORES / "indicadores_v1.meta.json"
ARQUIVO_QUALIDADE = PASTA_INDICADORES / "qualidade_v1.csv"


def pasta_extracao(data_extracao_iso: str) -> Path:
    """Pasta dos brutos de uma extração, ex.: data/raw/2026-10-04/."""
    return PASTA_RAW / data_extracao_iso


def caminho_bruto(ano: int, data_extracao_iso: str) -> Path:
    """Caminho padronizado do arquivo bruto de um ano numa extração."""
    return pasta_extracao(data_extracao_iso) / f"lattes_{ano}.csv"


# ── Fonte ────────────────────────────────────────────────────────────────────
# Página do CNPq (http, não https). Ela apenas embute o workbook do Tableau Public.
URL_PAINEL = "http://bi.cnpq.br/painel/formacao-atuacao-lattes/"

# Exportação da aba "Painel - Download" do workbook no Tableau Public.
# `:showVizHome=no` é obrigatório: sem ele a URL redireciona para uma página 404.
URL_EXPORTACAO = (
    "https://public.tableau.com/views/PainelLattes-FormaoeAtuao/Painel-Download.csv"
)
PARAMETROS_FIXOS_EXPORTACAO = ":showVizHome=no"
# Os filtros usam o nome do campo como aparece na view, com o ponto inicial.
# A view vem pré-filtrada (Ano=2023, Doutorado); passar o nível vazio limpa o filtro.
FILTRO_ANO = ".Ano"
FILTRO_NIVEL = ".Nível (Formação)"

# ── Anos ─────────────────────────────────────────────────────────────────────
# `Ano` é o ano de obtenção do título (campo ANOOBTENCAOTITULO do workbook),
# não o ano de um extrato. Todos os anos vêm da mesma extração.

# Anos baixados por padrão.
ANOS_DISPONIVEIS = [2020, 2021, 2022, 2023, 2024, 2025, 2026]

# Anos que entram na consolidação e nos indicadores. Para ampliar a série,
# basta mudar esta lista. 2026 fica de fora da V1: a coorte de titulação está
# incompleta e o atraso de atualização do Lattes não é aleatório, então
# enviesaria até as proporções (ver metodologia).
ANOS = [2020, 2021, 2022, 2023, 2024, 2025]

# Extração usada como base. A V1 usa a de 2026-10-04 (a única que pode ser
# baixada de novo na fonte). Trocar de extração é decisão metodológica.
EXTRACAO = "2026-10-04"

# Arquivo com os metadados do consolidado (extração, anos, contagens, SHA-256 dos brutos).
ARQUIVO_CONSOLIDADO_META = PASTA_PROCESSED / "lattes_consolidado.meta.json"

# ── Formato dos arquivos ─────────────────────────────────────────────────────
# Os brutos são guardados exatamente como vieram. Formatos aceitos na leitura:
#   exportação por URL do Tableau: UTF-8, vírgula
#   "Download > Tabela de referência cruzada" da interface: UTF-16, tabulação
CONSOLIDADO_ENCODING = "utf-8"
CONSOLIDADO_SEP = ","

# ── Colunas ──────────────────────────────────────────────────────────────────
COLUNA_ANO = "Ano"
COLUNA_PESSOAS = "Totalpessoas"
COLUNA_DATA_EXTRACAO = "Data Extração BD Lattes"
COLUNA_NIVEL = "Nível (Formação)"

# A exportação do Tableau escreve datas no padrão americano (mês/dia/ano).
# Evidência: o extrato .hyper do workbook guarda DATAEXTRACAO = 2026-10-04 como
# tipo data, e o CSV exportado traz a string "10/4/2026".
FORMATO_DATA_EXTRACAO = "%m/%d/%Y"

# Níveis de formação conhecidos. Um nível fora desta lista gera aviso e deve
# ser discutido antes de entrar nos indicadores.
NIVEIS_FORMACAO = ["Mestrado", "Doutorado", "Mestrado Profissional"]

# As 16 colunas de análise (as mesmas do pipeline legado).
COLUNAS_ANALITICAS = [
    "Ano",
    "Sexo",
    "Cor ou Raça",
    "Região (Formação)",
    "UF (Formação)",
    "Grande Área (Formação)",
    "Área (Formação)",
    "Nível (Formação)",
    "Região (Atuação)",
    "UF (Atuação)",
    "Grande Área (Atuação)",
    "Área (Atuação)",
    "Setor de Atividade (Atuação)",
    "Enquadramento (Atuação)",
    "Bolsista - PQ",
    "Bolsista - DT",
]

# Colunas de controle: o peso de cada linha (pessoas) e a proveniência.
COLUNAS_CONTROLE = [COLUNA_PESSOAS, COLUNA_DATA_EXTRACAO]

# O consolidado tem 18 colunas: as 16 de análise + as 2 de controle.
COLUNAS_CONSOLIDADAS = COLUNAS_ANALITICAS + COLUNAS_CONTROLE

# Colunas que todo bruto precisa ter para ser aceito.
COLUNAS_OBRIGATORIAS_BRUTO = COLUNAS_CONSOLIDADAS

# ── Definição de STEM ────────────────────────────────────────────────────────
# STEM é definido por Grande Área (não por lista de áreas específicas).
# "Tecnologias" fica fora: não existe na Árvore do Conhecimento do CNPq.
GRANDES_AREAS_STEM = frozenset({"Ciências Exatas e da Terra", "Engenharias"})

# Área específica do recorte de Computação (situação atual).
AREA_COMPUTACAO = "Ciência da Computação"

# ── Categorias (conferidas contra os valores distintos reais da base) ────────
FEMININO = "Feminino"
MASCULINO = "Masculino"
SEXOS_DECLARADOS = (FEMININO, MASCULINO)
SEXO_NAO_DECLARADO = "Não declarado"

RACAS_DECLARADAS = ["Branca", "Parda", "Preta", "Amarela", "Indígena"]
RACA_NAO_DECLARADA = "Não desejo declarar"

# Bolsas: "Sim" = já recebeu a bolsa do CNPq (histórico, Plataforma Carlos Chagas).
# Qualquer outro valor ("Não" ou vazio, nos brutos antigos) conta como não.
BOLSA_SIM = "Sim"
# Bolsas verificadas no relatório de qualidade (lidas dos brutos; só PQ e DT estão no consolidado).
COLUNAS_BOLSAS_QUALIDADE = [
    "Bolsista - Iniciação Científica",
    "Bolsista - Mestrado",
    "Bolsista - Doutorado",
    "Bolsista - PQ",
    "Bolsista - DT",
]

# "Não informado" em campos de formação e atuação. Sai dos denominadores e
# a taxa vai para o relatório de qualidade.
NAO_INFORMADO = "Não informado"

# ── Regras do recorte de raça ────────────────────────────────────────────────
# Categoria Negra = Preta + Parda (convenção do IBGE). Ligada por padrão até
# confirmação com a professora; desligada, as linhas "Negra" somem e o resto
# da saída fica idêntico.
AGREGAR_NEGRA = True
GRUPOS_RACIAIS_AGREGADOS = {"Negra": ("Preta", "Parda")}

# Raças cujo número principal é o agregado do período: as linhas anuais saem
# com flag_preferir_agregado.
RACAS_PREFERIR_AGREGADO = frozenset({"Indígena"})

# Limites das flags de amostra pequena (parâmetros de exibição, não resultados).
LIMITE_DENOMINADOR = 30
LIMITE_NUMERADOR = 10
