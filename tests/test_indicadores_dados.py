"""Testes de identidade dos indicadores nos dados reais (marcador `dados`).

Valem para todo recorte e período, sem números fixos: conferem que os
indicadores são coerentes entre si.
"""

import pandas as pd
import pytest

from lattes import config
from lattes import indicadores as ind
from lattes.consolidacao import consolidar, ler_consolidado

pytestmark = pytest.mark.dados

CHAVE = ["base", "periodo", "recorte", "categoria"]


@pytest.fixture(scope="module")
def consolidado(tmp_path_factory):
    saida = tmp_path_factory.mktemp("ind") / "consolidado.csv"
    consolidar(config.pasta_extracao(config.EXTRACAO), config.ANOS, saida)
    return ler_consolidado(saida)


@pytest.fixture(scope="module")
def com_negra(consolidado):
    return ind.gerar_indicadores(consolidado, config.EXTRACAO, config.ANOS, agregar_negra=True)


@pytest.fixture(scope="module")
def sem_negra(consolidado):
    return ind.gerar_indicadores(consolidado, config.EXTRACAO, config.ANOS, agregar_negra=False)


def por_chave(saida, indicador, **filtros):
    sel = saida[saida.indicador == indicador]
    for coluna, valor in filtros.items():
        sel = sel[sel[coluna] == valor]
    return sel


def test_composicao_soma_o_denominador(com_negra):
    comp = por_chave(com_negra, ind.COMPOSICAO, raca_agregada=False)
    soma = comp.groupby(CHAVE).agg(num=("numerador", "sum"), den=("denominador", "first"),
                                   dens=("denominador", "nunique"))
    assert (soma.dens == 1).all()
    assert (soma.num == soma.den).all(), soma[soma.num != soma.den]
    assert len(soma) > 0


def test_grupos_raciais_somam_participacao_menos_nao_declarados(com_negra):
    grupos = por_chave(com_negra, ind.GRUPO_RACIAL, raca_agregada=False).groupby(CHAVE).denominador.sum()
    participacao = por_chave(com_negra, ind.PARTICIPACAO).set_index(CHAVE).denominador
    nao_declarou = por_chave(com_negra, ind.TAXA_ND_RACA, sexo=ind.TODOS).set_index(CHAVE).numerador
    esperado = (participacao - nao_declarou).dropna().astype(int)
    assert len(esperado) == len(grupos) > 0
    pd.testing.assert_series_equal(grupos.sort_index(), esperado.sort_index(), check_names=False)


@pytest.mark.parametrize("indicador", [ind.GRUPO_RACIAL, ind.COMPOSICAO])
def test_negra_e_parda_mais_preta(com_negra, indicador):
    sel = por_chave(com_negra, indicador)
    negra = sel[sel.raca == "Negra"].set_index(CHAVE)[["numerador", "denominador"]]
    componentes = config.GRUPOS_RACIAIS_AGREGADOS["Negra"]
    partes = sel[sel.raca.isin(componentes)].groupby(CHAVE)
    assert len(negra) > 0
    pd.testing.assert_series_equal(negra.numerador.sort_index(), partes.numerador.sum().sort_index(),
                                   check_names=False)
    if indicador == ind.GRUPO_RACIAL:
        pd.testing.assert_series_equal(negra.denominador.sort_index(),
                                       partes.denominador.sum().sort_index(), check_names=False)
    else:  # composição: mesmo denominador (mulheres com raça declarada)
        assert (negra.denominador.sort_index() == partes.denominador.first().sort_index()).all()


def test_saida_sem_negra_e_identica_exceto_linhas_negra(com_negra, sem_negra):
    pd.testing.assert_frame_equal(com_negra[com_negra.raca != "Negra"].reset_index(drop=True),
                                  sem_negra.reset_index(drop=True))


def test_taxa_todos_e_feminino_mais_masculino(com_negra):
    taxa = por_chave(com_negra, ind.TAXA_ND_RACA)
    t = taxa.pivot_table(index=CHAVE, columns="sexo", values=["numerador", "denominador"])
    for medida in ("numerador", "denominador"):
        assert (t[medida][ind.TODOS] == t[medida]["Feminino"] + t[medida]["Masculino"]).all()


def test_situacao_atual_so_no_agregado(com_negra):
    situacao = com_negra[com_negra.base == ind.BASE_SITUACAO]
    assert set(situacao.periodo) == {ind.rotulo_agregado(config.ANOS)}
