"""Acesso à fonte pela internet (marcador `rede`, desligado por padrão).

Rode com `pytest -m rede`. Faz poucas requisições pequenas: a página do
painel e a exportação de um ano antigo, com poucos registros.
"""

import pytest
import requests

from lattes import config
from lattes.download import CABECALHOS, baixar_ano
from lattes.validacao import validar_bruto

pytestmark = pytest.mark.rede

# Ano antigo com poucos registros, para o teste ser rápido.
ANO_PEQUENO = 1990


def test_pagina_do_painel_embute_o_workbook():
    r = requests.get(config.URL_PAINEL, headers=CABECALHOS, timeout=60)
    assert r.status_code == 200
    assert "PainelLattes-FormaoeAtuao" in r.text, "a página não embute mais o workbook esperado"


def test_exportacao_csv_ainda_funciona(tmp_path):
    destino = tmp_path / f"lattes_{ANO_PEQUENO}.csv"
    with requests.Session() as sessao:
        baixar_ano(sessao, ANO_PEQUENO, destino, timeout=300, tentativas=2, espera=10)
    resultado = validar_bruto(destino, ANO_PEQUENO)
    assert resultado.n_pessoas > 0
    assert resultado.avisos == []
