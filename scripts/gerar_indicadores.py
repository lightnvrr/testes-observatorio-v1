"""Gera os indicadores da V1 em data/processed/indicadores/.

Uso:
    python scripts/gerar_indicadores.py
    python scripts/gerar_indicadores.py --sem-negra    # sem a categoria Negra

Saídas:
    indicadores_v1.csv          indicadores em formato longo (para o front)
    indicadores_dicionario.csv  rótulos, definições e ressalvas
    indicadores_v1.meta.json    extração, parâmetros e SHA-256 do consolidado
    qualidade_v1.csv            taxas de "Não informado" e notas de qualidade (para a metodologia)
"""

import argparse
import json
import sys

from lattes import config
from lattes.consolidacao import ler_bolsas, ler_consolidado
from lattes.download import agora_iso, sha256
from lattes.indicadores import ErroDominio, gerar_dicionario, gerar_indicadores, gerar_qualidade


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--agregar-negra", action=argparse.BooleanOptionalAction, default=config.AGREGAR_NEGRA,
                        help=f"inclui a categoria Negra (padrão do config: {config.AGREGAR_NEGRA})")
    args = parser.parse_args()

    if not config.ARQUIVO_CONSOLIDADO_META.exists():
        print("[ERRO] consolidado não encontrado. Rode scripts/consolidar_lattes.py.", file=sys.stderr)
        return 1
    meta_consolidado = json.loads(config.ARQUIVO_CONSOLIDADO_META.read_text(encoding="utf-8"))
    if meta_consolidado["anos"] != config.ANOS:
        print(f"[ERRO] consolidado com anos {meta_consolidado['anos']}, config.ANOS = {config.ANOS}. "
              "Rode a consolidação de novo.", file=sys.stderr)
        return 1
    extracao = meta_consolidado["extracao"]

    df = ler_consolidado()
    try:
        indicadores = gerar_indicadores(df, extracao, config.ANOS, args.agregar_negra)
    except ErroDominio as e:
        print(f"[ERRO] {e}", file=sys.stderr)
        return 1
    qualidade = gerar_qualidade(df, config.ANOS, bolsas=ler_bolsas(config.pasta_extracao(extracao), config.ANOS))
    dicionario = gerar_dicionario(qualidade, extracao, config.ANOS)

    config.PASTA_INDICADORES.mkdir(parents=True, exist_ok=True)
    opcoes = {"index": False, "encoding": config.CONSOLIDADO_ENCODING, "sep": config.CONSOLIDADO_SEP}
    indicadores.to_csv(config.ARQUIVO_INDICADORES, **opcoes)
    dicionario.to_csv(config.ARQUIVO_DICIONARIO, **opcoes)
    qualidade.to_csv(config.ARQUIVO_QUALIDADE, **opcoes)

    meta = {
        "gerado_em": agora_iso(),
        "extracao": extracao,
        "anos": config.ANOS,
        "agregar_negra": args.agregar_negra,
        "grupos_raciais_agregados": config.GRUPOS_RACIAIS_AGREGADOS if args.agregar_negra else {},
        "racas_preferir_agregado": sorted(config.RACAS_PREFERIR_AGREGADO),
        "limite_denominador": config.LIMITE_DENOMINADOR,
        "limite_numerador": config.LIMITE_NUMERADOR,
        "grandes_areas_stem": sorted(config.GRANDES_AREAS_STEM),
        "sha256_consolidado": sha256(config.ARQUIVO_CONSOLIDADO),
        "linhas_por_indicador": indicadores["indicador"].value_counts().sort_index().to_dict(),
    }
    config.ARQUIVO_INDICADORES_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8")

    pasta = config.PASTA_INDICADORES.relative_to(config.RAIZ)
    print(f"Extração {extracao}, anos {config.ANOS[0]} a {config.ANOS[-1]}, Negra: {args.agregar_negra}")
    for indicador, n in meta["linhas_por_indicador"].items():
        print(f"  {indicador}: {n} linhas")
    print(f"Gravado em {pasta}: {config.ARQUIVO_INDICADORES.name} ({len(indicadores)} linhas), "
          f"{config.ARQUIVO_DICIONARIO.name}, {config.ARQUIVO_QUALIDADE.name} ({len(qualidade)} linhas), "
          f"{config.ARQUIVO_INDICADORES_META.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
