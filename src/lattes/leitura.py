"""Leitura dos arquivos brutos do painel Lattes, em qualquer dos dois formatos aceitos."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


class ErroFormato(ValueError):
    """O arquivo não está em nenhum dos formatos aceitos."""


@dataclass(frozen=True)
class Formato:
    encoding: str
    sep: str


UTF16_TAB = Formato("utf-16", "\t")
UTF8_VIRGULA = Formato("utf-8-sig", ",")


def detectar_formato(caminho: Path) -> Formato:
    """Identifica o formato do bruto pelo BOM e pela primeira linha.

    UTF-16 (com BOM) usa tabulação; UTF-8 usa vírgula. Qualquer outra coisa
    (vazio, Latin-1, HTML no lugar do CSV) gera ErroFormato.
    """
    with open(caminho, "rb") as f:
        inicio = f.read(64 * 1024)
    if not inicio:
        raise ErroFormato(f"{caminho.name}: arquivo vazio.")

    if inicio[:2] in (b"\xff\xfe", b"\xfe\xff"):
        formato = UTF16_TAB
        primeira = inicio.decode("utf-16", errors="ignore").splitlines()[0]
    else:
        formato = UTF8_VIRGULA
        try:
            texto = inicio.decode("utf-8-sig")
        except UnicodeDecodeError as e:
            # O corte em 64 KiB pode partir um caractere ao meio no final do bloco.
            if e.start < len(inicio) - 4:
                raise ErroFormato(
                    f"{caminho.name}: não é UTF-16 nem UTF-8 válido "
                    f"(byte inválido na posição {e.start})."
                ) from e
            texto = inicio[: e.start].decode("utf-8-sig")
        primeira = texto.splitlines()[0] if texto else ""

    if primeira.lstrip().lower().startswith(("<!doctype", "<html")):
        raise ErroFormato(f"{caminho.name}: o conteúdo é uma página HTML, não um CSV.")
    if formato.sep not in primeira:
        raise ErroFormato(
            f"{caminho.name}: codificação {formato.encoding} detectada, mas o cabeçalho "
            f"não usa o separador esperado ({formato.sep!r})."
        )
    return formato


def normalizar_coluna(nome: str) -> str:
    """Remove o ponto inicial que o Tableau põe nos nomes de campo (".Ano" vira "Ano")."""
    return nome.strip().lstrip(".").strip()


def ler_bruto(caminho: Path, colunas: list[str] | None = None) -> pd.DataFrame:
    """Lê um bruto como texto, com nomes de coluna normalizados.

    Tudo é lido como string e células vazias continuam vazias (não viram NaN),
    para que categorias como "Não informado" ou bolsas em branco não sejam
    reinterpretadas pelo pandas. `colunas` usa os nomes já normalizados.
    """
    formato = detectar_formato(caminho)
    usecols = None
    if colunas is not None:
        desejadas = set(colunas)
        usecols = lambda c: normalizar_coluna(c) in desejadas  # noqa: E731
    df = pd.read_csv(
        caminho,
        encoding=formato.encoding,
        sep=formato.sep,
        dtype=str,
        keep_default_na=False,
        usecols=usecols,
    )
    df.columns = [normalizar_coluna(c) for c in df.columns]
    return df
