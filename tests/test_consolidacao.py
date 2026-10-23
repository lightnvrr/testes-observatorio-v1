"""Testes da consolidação: unitários com fixtures e de dados com a extração real."""

import json
import shutil
from pathlib import Path

import pytest

from lattes import config
from lattes.consolidacao import ErroConsolidacao, consolidar, ler_consolidado
from lattes.download import registrar_no_manifest, sha256

FIXTURES = Path(__file__).parent / "fixtures"


def montar_extracao(tmp_path: Path, arquivos: dict[int, Path]) -> Path:
    """Cria uma pasta de extração falsa com manifest, a partir das fixtures."""
    pasta = tmp_path / "2026-10-04"
    pasta.mkdir()
    for ano, origem in arquivos.items():
        destino = pasta / f"lattes_{ano}.csv"
        texto = origem.read_text(encoding="utf-16" if "utf16" in origem.name else "utf-8")
        destino.write_text(texto.replace("2023", str(ano)),
                           encoding="utf-16" if "utf16" in origem.name else "utf-8")
        registrar_no_manifest(pasta, {"ano": ano, "sha256": sha256(destino)}, "10/4/2026", "2026-10-04")
    return pasta


# ── Unitários ────────────────────────────────────────────────────────────────

def test_consolida_formatos_misturados_sem_remover_registros(tmp_path):
    pasta = montar_extracao(tmp_path, {2022: FIXTURES / "bruto_utf16_tab.csv",
                                       2023: FIXTURES / "bruto_utf8_virgula.csv"})
    saida = tmp_path / "consolidado.csv"
    resumo = consolidar(pasta, [2022, 2023], saida)

    df = ler_consolidado(saida)
    assert list(df.columns) == config.COLUNAS_CONSOLIDADAS
    assert len(df) == resumo.n_linhas == 6
    assert resumo.n_pessoas == 8
    assert resumo.por_ano == {2022: {"n_linhas": 3, "n_pessoas": 4}, 2023: {"n_linhas": 3, "n_pessoas": 4}}
    assert df["Ano"].value_counts().to_dict() == {"2022": 3, "2023": 3}
    assert saida.read_bytes()[:3] != b"\xef\xbb\xbf"  # UTF-8 sem BOM


def test_ano_ausente_interrompe(tmp_path):
    pasta = montar_extracao(tmp_path, {2023: FIXTURES / "bruto_utf8_virgula.csv"})
    with pytest.raises(ErroConsolidacao, match="2024"):
        consolidar(pasta, [2023, 2024], tmp_path / "c.csv")
    assert not (tmp_path / "c.csv").exists()


def test_arquivo_alterado_depois_do_download_interrompe(tmp_path):
    pasta = montar_extracao(tmp_path, {2023: FIXTURES / "bruto_utf8_virgula.csv"})
    with open(pasta / "lattes_2023.csv", "a", encoding="utf-8") as f:
        f.write("\n")
    with pytest.raises(ErroConsolidacao, match="SHA-256"):
        consolidar(pasta, [2023], tmp_path / "c.csv")


def test_nivel_desconhecido_interrompe(tmp_path):
    pasta = montar_extracao(tmp_path, {2023: FIXTURES / "bruto_utf8_virgula.csv"})
    bruto = pasta / "lattes_2023.csv"
    bruto.write_text(bruto.read_text(encoding="utf-8").replace("Mestrado Profissional", "Especialização"),
                     encoding="utf-8")
    registrar_no_manifest(pasta, {"ano": 2023, "sha256": sha256(bruto)}, "10/4/2026", "2026-10-04")
    with pytest.raises(ErroConsolidacao, match="Especialização"):
        consolidar(pasta, [2023], tmp_path / "c.csv")


# ── Dados reais ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def consolidado_real(tmp_path_factory):
    saida = tmp_path_factory.mktemp("consolidado") / "lattes_consolidado.csv"
    resumo = consolidar(config.pasta_extracao(config.EXTRACAO), config.ANOS, saida)
    return resumo, ler_consolidado(saida)


@pytest.mark.dados
def test_contagens_por_ano_batem_com_a_referencia(consolidado_real, referencia):
    resumo, _ = consolidado_real
    for ano in config.ANOS:
        esperado = referencia["anos"][str(ano)]
        assert resumo.por_ano[ano] == {"n_linhas": esperado["n_linhas"], "n_pessoas": esperado["n_pessoas"]}, ano


@pytest.mark.dados
def test_consolidado_tem_o_total_da_referencia(consolidado_real, referencia):
    resumo, df = consolidado_real
    linhas = sum(referencia["anos"][str(a)]["n_linhas"] for a in config.ANOS)
    pessoas = sum(referencia["anos"][str(a)]["n_pessoas"] for a in config.ANOS)
    assert len(df) == resumo.n_linhas == linhas
    assert df["Totalpessoas"].astype(int).sum() == pessoas
    assert list(df.columns) == config.COLUNAS_CONSOLIDADAS
    assert set(df["Data Extração BD Lattes"]) == {referencia["data_extracao_original"]}
