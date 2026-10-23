"""Testes unitários de leitura e validação dos brutos (sem dados reais)."""

from pathlib import Path

import pytest

from lattes import config
from lattes.download import montar_url
from lattes.leitura import UTF8_VIRGULA, UTF16_TAB, ErroFormato, detectar_formato, ler_bruto
from lattes.validacao import (
    ErroValidacao,
    comparar_com_referencia,
    converter_data_extracao,
    validar_bruto,
)

FIXTURES = Path(__file__).parent / "fixtures"
UTF8 = FIXTURES / "bruto_utf8_virgula.csv"
UTF16 = FIXTURES / "bruto_utf16_tab.csv"


@pytest.mark.parametrize("arquivo, formato", [(UTF8, UTF8_VIRGULA), (UTF16, UTF16_TAB)])
def test_detecta_os_dois_formatos(arquivo, formato):
    assert detectar_formato(arquivo) == formato


@pytest.mark.parametrize("arquivo", [UTF8, UTF16])
def test_leitura_normaliza_colunas_e_mantem_texto(arquivo):
    df = ler_bruto(arquivo)
    assert "Ano" in df.columns and ".Ano" not in df.columns
    assert list(df["Cor ou Raça"]) == ["Parda", "Branca", "Não desejo declarar"]
    assert list(df["Totalpessoas"]) == ["1", "2", "1"]


def test_os_dois_formatos_leem_o_mesmo_conteudo():
    assert ler_bruto(UTF8).equals(ler_bruto(UTF16))


def test_leitura_de_colunas_selecionadas():
    df = ler_bruto(UTF16, colunas=["Sexo", "Totalpessoas"])
    assert list(df.columns) == ["Sexo", "Totalpessoas"]


def test_validacao_conta_linhas_e_pessoas():
    r = validar_bruto(UTF16, 2023)
    assert (r.n_linhas, r.n_pessoas) == (3, 4)
    assert r.encoding == "utf-16" and r.separador == "\t"
    assert r.data_extracao_original == "10/4/2026"
    assert r.data_extracao == "2026-10-04"
    assert r.avisos == []


def test_data_de_extracao_e_mes_dia_ano():
    assert converter_data_extracao("10/4/2026").isoformat() == "2026-10-04"
    with pytest.raises(ErroValidacao):
        converter_data_extracao("2026-10-04")


def test_arquivo_vazio(tmp_path):
    vazio = tmp_path / "vazio.csv"
    vazio.write_bytes(b"")
    with pytest.raises(ErroValidacao, match="vazio"):
        validar_bruto(vazio, 2023)


def test_codificacao_errada(tmp_path):
    latin1 = tmp_path / "latin1.csv"
    latin1.write_bytes(UTF8.read_text(encoding="utf-8").encode("latin-1"))
    with pytest.raises(ErroValidacao, match="UTF"):
        validar_bruto(latin1, 2023)


def test_utf16_com_separador_errado(tmp_path):
    errado = tmp_path / "utf16_virgula.csv"
    errado.write_text(UTF8.read_text(encoding="utf-8"), encoding="utf-16")
    with pytest.raises(ErroFormato, match="separador"):
        detectar_formato(errado)


def test_html_no_lugar_do_csv(tmp_path):
    html = tmp_path / "erro.csv"
    html.write_text("<!DOCTYPE html><html><body>404</body></html>", encoding="utf-8")
    with pytest.raises(ErroValidacao, match="HTML"):
        validar_bruto(html, 2023)


def test_coluna_faltando(tmp_path):
    texto = UTF8.read_text(encoding="utf-8").replace(".Cor ou Raça", ".Outra Coluna")
    sem_raca = tmp_path / "sem_raca.csv"
    sem_raca.write_text(texto, encoding="utf-8")
    with pytest.raises(ErroValidacao, match="Cor ou Raça"):
        validar_bruto(sem_raca, 2023)


def test_so_cabecalho(tmp_path):
    so_cabecalho = tmp_path / "cabecalho.csv"
    so_cabecalho.write_text(UTF8.read_text(encoding="utf-8").splitlines()[0] + "\n", encoding="utf-8")
    with pytest.raises(ErroValidacao, match="nenhum registro"):
        validar_bruto(so_cabecalho, 2023)


def test_ano_diferente_do_esperado():
    with pytest.raises(ErroValidacao, match="2024"):
        validar_bruto(UTF8, 2024)


def test_nivel_desconhecido_gera_aviso(tmp_path):
    texto = UTF8.read_text(encoding="utf-8").replace("Mestrado Profissional", "Especialização")
    novo = tmp_path / "nivel_novo.csv"
    novo.write_text(texto, encoding="utf-8")
    r = validar_bruto(novo, 2023)
    assert len(r.avisos) == 1 and "Especialização" in r.avisos[0]


def test_comparacao_com_referencia_avisa_sem_travar():
    r = validar_bruto(UTF8, 2023)
    assert comparar_com_referencia(r, {"anos": {"2023": {"n_pessoas": 4, "n_linhas": 3}}}) == []
    avisos = comparar_com_referencia(r, {"anos": {"2023": {"n_pessoas": 5}}})
    assert len(avisos) == 1 and "n_pessoas" in avisos[0]
    assert "sem arquivo de referência" in comparar_com_referencia(r, None)[0]


def test_url_de_exportacao():
    url = montar_url(2023)
    assert url.startswith(config.URL_EXPORTACAO + "?:showVizHome=no&")
    assert "&.Ano=2023&" in url
    assert url.endswith("&.N%C3%ADvel%20%28Forma%C3%A7%C3%A3o%29=")
    assert "+" not in url
