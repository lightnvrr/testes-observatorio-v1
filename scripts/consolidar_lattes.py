"""Consolida os brutos de uma extração em data/processed/lattes_consolidado.csv.

Uso:
    python scripts/consolidar_lattes.py                       # config.EXTRACAO, config.ANOS
    python scripts/consolidar_lattes.py --extracao 2026-10-04

Lê os anos de config.ANOS, seleciona as colunas de config.COLUNAS_CONSOLIDADAS
(16 de análise + Totalpessoas + Data Extração BD Lattes) e grava UTF-8 com
vírgula. Nenhum registro é removido. Os metadados (extração, contagens por ano,
SHA-256 dos brutos) vão para lattes_consolidado.meta.json.
"""

import argparse
import json
import logging
import sys

from lattes import config
from lattes.consolidacao import ErroConsolidacao, consolidar
from lattes.download import agora_iso, ler_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--extracao", default=config.EXTRACAO, help=f"pasta em data/raw/ (padrão {config.EXTRACAO})")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    pasta = config.pasta_extracao(args.extracao)
    print(f"Extração {args.extracao}, anos {config.ANOS[0]} a {config.ANOS[-1]}")
    try:
        resumo = consolidar(pasta, config.ANOS, config.ARQUIVO_CONSOLIDADO)
    except ErroConsolidacao as e:
        print(f"[ERRO] {e}", file=sys.stderr)
        return 1

    manifest = ler_manifest(pasta)
    meta = {
        "gerado_em": agora_iso(),
        "extracao": resumo.extracao,
        "anos": resumo.anos,
        "colunas": resumo.colunas,
        "n_linhas": resumo.n_linhas,
        "n_pessoas": resumo.n_pessoas,
        "por_ano": {str(a): v | {"sha256_bruto": manifest["anos"][str(a)]["sha256"]}
                    for a, v in resumo.por_ano.items()},
    }
    config.ARQUIVO_CONSOLIDADO_META.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Gravado {config.ARQUIVO_CONSOLIDADO.relative_to(config.RAIZ)} "
          f"({len(resumo.colunas)} colunas) e {config.ARQUIVO_CONSOLIDADO_META.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
