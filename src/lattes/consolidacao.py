"""Consolidação dos brutos de uma extração num único CSV.

A consolidação só seleciona colunas e empilha os anos: nenhum registro é
removido e nenhum valor é alterado. Tratamentos (bolsas vazias, siglas de UF,
exclusões de denominador) ficam na etapa de indicadores.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from lattes import config
from lattes.download import ler_manifest, sha256
from lattes.leitura import ler_bruto
from lattes.validacao import ErroValidacao, validar_bruto

log = logging.getLogger(__name__)


class ErroConsolidacao(RuntimeError):
    """Os brutos não permitem uma consolidação segura."""


@dataclass
class ResumoConsolidacao:
    extracao: str
    anos: list[int]
    colunas: list[str]
    por_ano: dict[int, dict] = field(default_factory=dict)

    @property
    def n_linhas(self) -> int:
        return sum(v["n_linhas"] for v in self.por_ano.values())

    @property
    def n_pessoas(self) -> int:
        return sum(v["n_pessoas"] for v in self.por_ano.values())


def conferir_colunas() -> None:
    """Garante que a especificação de colunas tem o que os indicadores precisam."""
    obrigatorias = ["Cor ou Raça", "Sexo", config.COLUNA_ANO, config.COLUNA_PESSOAS]
    faltando = [c for c in obrigatorias if c not in config.COLUNAS_CONSOLIDADAS]
    if faltando:
        raise ErroConsolidacao(f"config.COLUNAS_CONSOLIDADAS não inclui {faltando}.")
    if len(set(config.COLUNAS_CONSOLIDADAS)) != len(config.COLUNAS_CONSOLIDADAS):
        raise ErroConsolidacao("config.COLUNAS_CONSOLIDADAS tem colunas repetidas.")


def ler_ano(pasta_extracao: Path, ano: int) -> pd.DataFrame:
    """Valida e lê o bruto de um ano, só com as colunas consolidadas."""
    caminho = pasta_extracao / f"lattes_{ano}.csv"
    entrada = ler_manifest(pasta_extracao).get("anos", {}).get(str(ano))
    if entrada is None:
        raise ErroConsolidacao(f"{caminho.name}: ano {ano} ausente do manifest da extração.")
    if not caminho.exists():
        raise ErroConsolidacao(f"{caminho}: arquivo não encontrado. Rode scripts/baixar_lattes.py.")
    if entrada.get("sha256") != sha256(caminho):
        raise ErroConsolidacao(f"{caminho.name}: SHA-256 não confere com o manifest.")
    try:
        resultado = validar_bruto(caminho, ano)
    except ErroValidacao as e:
        raise ErroConsolidacao(str(e)) from e
    if resultado.data_extracao != pasta_extracao.name:
        raise ErroConsolidacao(
            f"{caminho.name}: extração {resultado.data_extracao} diferente da pasta {pasta_extracao.name}."
        )
    if resultado.avisos:
        # Ex.: nível de formação novo. Precisa de decisão antes de entrar nos indicadores.
        raise ErroConsolidacao(f"{caminho.name}: " + " ".join(resultado.avisos))

    df = ler_bruto(caminho, colunas=config.COLUNAS_CONSOLIDADAS)
    return df[config.COLUNAS_CONSOLIDADAS]


def consolidar(
    pasta_extracao: Path,
    anos: list[int],
    saida: Path,
) -> ResumoConsolidacao:
    """Empilha os anos da extração em `saida` (UTF-8, vírgula), um ano por vez."""
    conferir_colunas()
    resumo = ResumoConsolidacao(pasta_extracao.name, list(anos), list(config.COLUNAS_CONSOLIDADAS))
    saida.parent.mkdir(parents=True, exist_ok=True)
    temporario = saida.with_suffix(saida.suffix + ".part")

    try:
        for i, ano in enumerate(anos):
            df = ler_ano(pasta_extracao, ano)
            df.to_csv(
                temporario,
                mode="w" if i == 0 else "a",
                header=i == 0,
                index=False,
                encoding=config.CONSOLIDADO_ENCODING,
                sep=config.CONSOLIDADO_SEP,
            )
            n_pessoas = int(df[config.COLUNA_PESSOAS].astype(int).sum())
            resumo.por_ano[ano] = {"n_linhas": len(df), "n_pessoas": n_pessoas}
            log.info("%s: %s linhas, %s pessoas", ano, f"{len(df):,}", f"{n_pessoas:,}")
    except Exception:
        temporario.unlink(missing_ok=True)
        raise

    temporario.replace(saida)
    log.info("Total: %s linhas, %s pessoas", f"{resumo.n_linhas:,}", f"{resumo.n_pessoas:,}")
    return resumo


def ler_consolidado(caminho: Path = config.ARQUIVO_CONSOLIDADO) -> pd.DataFrame:
    """Lê o consolidado como texto (mesmas regras de leitura dos brutos)."""
    return pd.read_csv(
        caminho,
        encoding=config.CONSOLIDADO_ENCODING,
        sep=config.CONSOLIDADO_SEP,
        dtype=str,
        keep_default_na=False,
    )
