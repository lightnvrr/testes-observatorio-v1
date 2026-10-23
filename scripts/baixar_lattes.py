"""Baixa os brutos do Painel Formação e Atuação Lattes (CNPq) para data/raw/.

Uso:
    python scripts/baixar_lattes.py                  # anos de config.ANOS_DISPONIVEIS
    python scripts/baixar_lattes.py --anos 2020-2026
    python scripts/baixar_lattes.py --anos 2023,2025 --force

Os arquivos são guardados como vieram em data/raw/{data_extracao}/lattes_{ano}.csv,
com um manifest.json por extração. Arquivos colocados à mão em data/raw/_entrada/
são validados e organizados da mesma forma (origem "manual").
"""

import argparse
import shutil
import sys
import time
from pathlib import Path

import requests

from lattes import config
from lattes.download import (
    ErroDownload,
    agora_iso,
    baixar_ano,
    instrucoes_manuais,
    ler_manifest,
    registrar_no_manifest,
    sha256,
)
from lattes.validacao import (
    ErroValidacao,
    ResultadoValidacao,
    carregar_referencia,
    comparar_com_referencia,
    validar_bruto,
)


def interpretar_anos(texto: str) -> list[int]:
    """Aceita "2020-2026", "2020,2023" ou combinações ("2020-2022,2025")."""
    anos: set[int] = set()
    for parte in texto.split(","):
        parte = parte.strip()
        if "-" in parte:
            inicio, fim = (int(x) for x in parte.split("-", 1))
            anos.update(range(inicio, fim + 1))
        elif parte:
            anos.add(int(parte))
    return sorted(anos)


def extracoes_existentes() -> list[Path]:
    """Pastas de extração em data/raw/, da mais recente para a mais antiga."""
    if not config.PASTA_RAW.exists():
        return []
    pastas = [p for p in config.PASTA_RAW.iterdir() if p.is_dir() and not p.name.startswith("_")]
    return sorted(pastas, key=lambda p: p.name, reverse=True)


def bruto_valido_existente(ano: int) -> tuple[Path, ResultadoValidacao] | None:
    """Arquivo válido do ano na extração mais recente que o tenha, se houver."""
    for pasta in extracoes_existentes():
        caminho = pasta / f"lattes_{ano}.csv"
        if not caminho.exists():
            continue
        entrada = ler_manifest(pasta).get("anos", {}).get(str(ano))
        if entrada is None or entrada.get("sha256") != sha256(caminho):
            print(f"  {caminho.relative_to(config.RAIZ)} não confere com o manifest; baixando de novo.")
            return None
        try:
            return caminho, validar_bruto(caminho, ano)
        except ErroValidacao as e:
            print(f"  arquivo existente inválido ({e}); baixando de novo.")
            return None
    return None


def arquivar(temporario: Path, ano: int, origem: str, metodo: str, baixado_em: str) -> ResultadoValidacao:
    """Valida o arquivo, move para a pasta da extração e atualiza o manifest."""
    resultado = validar_bruto(temporario, ano)
    destino = config.caminho_bruto(ano, resultado.data_extracao)
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(temporario), destino)

    registrar_no_manifest(
        destino.parent,
        {
            "ano": ano,
            "arquivo": destino.name,
            "metodo": metodo,
            "origem": origem,
            "baixado_em": baixado_em,
            "tamanho_bytes": destino.stat().st_size,
            "sha256": sha256(destino),
            "encoding": resultado.encoding,
            "separador": "tab" if resultado.separador == "\t" else resultado.separador,
            "n_linhas": resultado.n_linhas,
            "n_pessoas": resultado.n_pessoas,
            "data_extracao_original": resultado.data_extracao_original,
        },
        resultado.data_extracao_original,
        resultado.data_extracao,
    )
    return resultado


def relatar(resultado: ResultadoValidacao, rotulo: str) -> None:
    pasta = config.pasta_extracao(resultado.data_extracao).relative_to(config.RAIZ)
    print(
        f"  {rotulo}: {resultado.n_linhas:,} linhas, {resultado.n_pessoas:,} pessoas, "
        f"{resultado.encoding}, extração {resultado.data_extracao_original!r} "
        f"({resultado.data_extracao}) em {pasta}"
    )
    avisos = resultado.avisos + comparar_com_referencia(
        resultado, carregar_referencia(resultado.data_extracao)
    )
    for aviso in avisos:
        print(f"  [AVISO] {aviso}")


def importar_manuais(anos: list[int]) -> set[int]:
    """Processa arquivos colocados à mão em data/raw/_entrada/. Devolve os anos importados."""
    importados = set()
    for ano in anos:
        caminho = config.PASTA_ENTRADA_MANUAL / f"lattes_{ano}.csv"
        if not caminho.exists():
            continue
        print(f"[{ano}] arquivo manual encontrado em {caminho.relative_to(config.RAIZ)}")
        try:
            resultado = arquivar(caminho, ano, origem="download manual pelo painel",
                                 metodo="manual", baixado_em=agora_iso())
        except ErroValidacao as e:
            print(f"  [ERRO] arquivo manual inválido, mantido em _entrada/: {e}")
            continue
        relatar(resultado, "importado")
        importados.add(ano)
    return importados


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--anos", type=interpretar_anos,
                        default=config.ANOS_DISPONIVEIS, help="ex.: 2020-2026 ou 2020,2023")
    parser.add_argument("--force", action="store_true", help="baixa de novo mesmo se já houver arquivo válido")
    parser.add_argument("--timeout", type=float, default=300, help="segundos sem resposta antes de desistir (padrão 300)")
    parser.add_argument("--tentativas", type=int, default=3, help="tentativas por ano (padrão 3)")
    parser.add_argument("--espera", type=float, default=20, help="espera base entre tentativas, em segundos (padrão 20)")
    parser.add_argument("--pausa", type=float, default=5, help="pausa entre anos, em segundos (padrão 5)")
    args = parser.parse_args()

    print(f"Anos: {args.anos[0]} a {args.anos[-1]} ({len(args.anos)})" if args.anos else "Nenhum ano.")
    importados = importar_manuais(args.anos)
    falhas: list[int] = []
    sessao = requests.Session()
    primeiro_download = True

    for ano in args.anos:
        if ano in importados:
            continue
        if not args.force:
            existente = bruto_valido_existente(ano)
            if existente:
                relatar(existente[1], f"[{ano}] já existe, pulando")
                continue

        # Uma requisição por vez, com pausa entre anos para não sobrecarregar o servidor.
        if not primeiro_download:
            time.sleep(args.pausa)
        primeiro_download = False

        print(f"[{ano}] baixando...", flush=True)
        temporario = config.PASTA_BAIXANDO / f"lattes_{ano}.csv"
        inicio = time.monotonic()
        try:
            url = baixar_ano(sessao, ano, temporario, args.timeout, args.tentativas, args.espera)
            resultado = arquivar(temporario, ano, origem=url,
                                 metodo="http: exportação CSV do Tableau Public", baixado_em=agora_iso())
        except (ErroDownload, ErroValidacao) as e:
            print(f"  [ERRO] {e}")
            temporario.unlink(missing_ok=True)
            falhas.append(ano)
            continue
        relatar(resultado, f"baixado em {time.monotonic() - inicio:.0f} s")

    if config.PASTA_BAIXANDO.exists() and not any(config.PASTA_BAIXANDO.iterdir()):
        config.PASTA_BAIXANDO.rmdir()

    datas = {p.name for p in extracoes_existentes()}
    if len(datas) > 1:
        print(f"\n[AVISO] há mais de uma extração em data/raw/: {sorted(datas)}. "
              "Não misture anos de extrações diferentes na consolidação.")

    if falhas:
        print(f"\nFalharam: {falhas}")
        print(instrucoes_manuais(falhas))
        return 1
    print("\nConcluído.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
