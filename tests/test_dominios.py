"""Domínios das categorias nos dados reais (marcador `dados`).

Os valores esperados ficam em tests/referencias/{extracao}.json, em "dominios".
O teste falha se surgir categoria nova (ou sumir uma conhecida), para que
nenhuma categoria entre nos indicadores sem revisão.
"""

import pytest

from lattes import config
from lattes.consolidacao import consolidar, ler_consolidado

pytestmark = pytest.mark.dados


@pytest.fixture(scope="module")
def consolidado(tmp_path_factory):
    saida = tmp_path_factory.mktemp("dom") / "consolidado.csv"
    consolidar(config.pasta_extracao(config.EXTRACAO), config.ANOS, saida)
    return ler_consolidado(saida)


@pytest.mark.parametrize("coluna", [
    "Sexo", "Cor ou Raça", "Grande Área (Formação)", "Grande Área (Atuação)",
    "Nível (Formação)", "Setor de Atividade (Atuação)", "Região (Formação)", "Região (Atuação)",
])
def test_dominio_igual_ao_da_referencia(consolidado, referencia, coluna):
    esperado = set(referencia["dominios"][coluna])
    obtido = set(consolidado[coluna])
    assert not obtido - esperado, f"{coluna}: categorias novas {sorted(obtido - esperado)}"
    assert not esperado - obtido, f"{coluna}: categorias que sumiram {sorted(esperado - obtido)}"


def test_strings_de_configuracao_existem_no_dominio(referencia):
    dominios = referencia["dominios"]
    for coluna in ("Grande Área (Formação)", "Grande Área (Atuação)"):
        assert config.GRANDES_AREAS_STEM <= set(dominios[coluna])
    assert set(config.SEXOS_DECLARADOS) | {config.SEXO_NAO_DECLARADO} == set(dominios["Sexo"])
    assert set(config.RACAS_DECLARADAS) | {config.RACA_NAO_DECLARADA} == set(dominios["Cor ou Raça"])
    assert set(config.NIVEIS_FORMACAO) == set(dominios["Nível (Formação)"])
    assert config.NAO_INFORMADO in dominios["Região (Atuação)"]
