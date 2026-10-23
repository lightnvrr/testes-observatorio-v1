"""Testes de coerência da configuração (não dependem de dados reais)."""

from lattes import config


def test_colunas_analiticas_sao_16_e_unicas():
    assert len(config.COLUNAS_ANALITICAS) == 16
    assert len(set(config.COLUNAS_ANALITICAS)) == 16


def test_consolidado_tem_16_analiticas_mais_pessoas_e_data_extracao():
    assert config.COLUNAS_CONSOLIDADAS == config.COLUNAS_ANALITICAS + [
        "Totalpessoas",
        "Data Extração BD Lattes",
    ]


def test_cor_ou_raca_esta_no_consolidado():
    assert "Cor ou Raça" in config.COLUNAS_CONSOLIDADAS


def test_anos_consolidados_sao_2020_a_2025():
    assert config.ANOS == list(range(2020, 2026))
    assert set(config.ANOS) <= set(config.ANOS_DISPONIVEIS)


def test_definicao_stem_por_grande_area():
    assert config.GRANDES_AREAS_STEM == {"Ciências Exatas e da Terra", "Engenharias"}


def test_url_do_painel_e_http():
    assert config.URL_PAINEL.startswith("http://")


# ── Decisões da V1 (docs/registro_decisoes_v1.md) ────────────────────────────

def test_decisao_extracao_de_referencia():
    assert config.EXTRACAO == "2026-10-04"


def test_decisao_2026_fora_da_v1():
    assert 2026 not in config.ANOS
    assert 2026 in config.ANOS_DISPONIVEIS  # continua sendo baixado


def test_decisao_categoria_negra_publicada():
    assert config.AGREGAR_NEGRA is True
    assert config.GRUPOS_RACIAIS_AGREGADOS == {"Negra": ("Preta", "Parda")}


def test_decisao_tecnologias_fora_do_stem():
    assert "Tecnologias" not in config.GRANDES_AREAS_STEM


def test_decisao_regras_de_amostra_pequena():
    assert config.LIMITE_DENOMINADOR == 30
    assert config.LIMITE_NUMERADOR == 10
    assert config.RACAS_PREFERIR_AGREGADO == {"Indígena"}
