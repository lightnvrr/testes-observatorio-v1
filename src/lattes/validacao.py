"""Validação dos arquivos brutos baixados do painel Lattes."""

import json
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import pandas as pd

from lattes import config
from lattes.leitura import ErroFormato, detectar_formato, ler_bruto


class ErroValidacao(ValueError):
    """O bruto não pode ser usado (formato, colunas ou conteúdo inválidos)."""


@dataclass
class ResultadoValidacao:
    ano: int
    encoding: str
    separador: str
    n_linhas: int
    n_pessoas: int
    data_extracao_original: str
    data_extracao: str  # ISO (AAAA-MM-DD)
    avisos: list[str] = field(default_factory=list)


def converter_data_extracao(texto: str) -> date:
    """Converte a data de extração do CSV para `date`.

    O formato (mês/dia/ano) está em config.FORMATO_DATA_EXTRACAO, junto com a
    evidência que o confirmou.
    """
    try:
        return datetime.strptime(texto.strip(), config.FORMATO_DATA_EXTRACAO).date()
    except ValueError as e:
        raise ErroValidacao(
            f"Data de extração {texto!r} fora do formato esperado "
            f"({config.FORMATO_DATA_EXTRACAO})."
        ) from e


def validar_bruto(caminho: Path, ano_esperado: int) -> ResultadoValidacao:
    """Confere formato, colunas e conteúdo de um bruto. Levanta ErroValidacao se inválido.

    Problemas que não impedem o uso (ex.: nível de formação desconhecido) vão
    para `avisos`.
    """
    if not caminho.exists():
        raise ErroValidacao(f"{caminho}: arquivo não encontrado.")
    try:
        formato = detectar_formato(caminho)
        df = ler_bruto(caminho)
    except ErroFormato as e:
        raise ErroValidacao(str(e)) from e
    except (UnicodeDecodeError, pd.errors.ParserError) as e:
        raise ErroValidacao(f"{caminho.name}: não foi possível ler o CSV ({e}).") from e

    faltando = [c for c in config.COLUNAS_OBRIGATORIAS_BRUTO if c not in df.columns]
    if faltando:
        raise ErroValidacao(f"{caminho.name}: colunas ausentes: {faltando}.")
    if df.empty:
        raise ErroValidacao(f"{caminho.name}: cabeçalho sem nenhum registro.")

    anos = set(df[config.COLUNA_ANO])
    if anos != {str(ano_esperado)}:
        raise ErroValidacao(
            f"{caminho.name}: esperado só o ano {ano_esperado}, encontrado {sorted(anos)}."
        )

    datas = set(df[config.COLUNA_DATA_EXTRACAO])
    if len(datas) != 1:
        raise ErroValidacao(
            f"{caminho.name}: mais de uma data de extração no arquivo: {sorted(datas)}."
        )
    data_original = datas.pop()
    data_iso = converter_data_extracao(data_original).isoformat()

    pessoas = pd.to_numeric(df[config.COLUNA_PESSOAS], errors="coerce")
    if pessoas.isna().any() or (pessoas < 1).any():
        raise ErroValidacao(
            f"{caminho.name}: coluna {config.COLUNA_PESSOAS} com valores não inteiros positivos."
        )

    avisos = []
    niveis_novos = sorted(set(df[config.COLUNA_NIVEL]) - set(config.NIVEIS_FORMACAO))
    if niveis_novos:
        avisos.append(
            f"níveis de formação fora da lista conhecida: {niveis_novos}. "
            "Discutir antes de incluir nos indicadores."
        )

    return ResultadoValidacao(
        ano=ano_esperado,
        encoding="utf-16" if formato.encoding == "utf-16" else "utf-8",
        separador=formato.sep,
        n_linhas=len(df),
        n_pessoas=int(pessoas.sum()),
        data_extracao_original=data_original,
        data_extracao=data_iso,
        avisos=avisos,
    )


def carregar_referencia(data_extracao_iso: str) -> dict | None:
    """Lê tests/referencias/{data}.json, se existir."""
    caminho = config.PASTA_REFERENCIAS / f"{data_extracao_iso}.json"
    if not caminho.exists():
        return None
    return json.loads(caminho.read_text(encoding="utf-8"))


def comparar_com_referencia(resultado: ResultadoValidacao, referencia: dict | None) -> list[str]:
    """Avisos (sem travar) quando as contagens divergem da referência da extração."""
    if referencia is None:
        return [f"sem arquivo de referência para a extração {resultado.data_extracao}."]
    esperado = referencia.get("anos", {}).get(str(resultado.ano))
    if esperado is None:
        return [f"referência {resultado.data_extracao} não tem o ano {resultado.ano}."]
    avisos = []
    for chave in ("n_pessoas", "n_linhas"):
        obtido = getattr(resultado, chave)
        if chave in esperado and esperado[chave] != obtido:
            avisos.append(f"{chave} = {obtido:,}, referência = {esperado[chave]:,}.")
    return avisos
