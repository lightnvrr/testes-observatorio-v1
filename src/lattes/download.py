"""Download dos brutos pela exportação CSV do Tableau Public e registro no manifest."""

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

from lattes import config

CABECALHOS = {"User-Agent": "KatieNet-Lattes/0.1 (Observatorio de Mulheres na Ciencia, UFAL)"}
TAMANHO_BLOCO = 1024 * 1024


class ErroDownload(RuntimeError):
    """O download falhou depois de todas as tentativas."""


def montar_url(ano: int) -> str:
    """URL de exportação de um ano, com todos os níveis de formação.

    Os filtros são codificados à mão porque o Tableau não interpreta "+" como
    espaço nos nomes de campo.
    """
    filtros = [
        config.PARAMETROS_FIXOS_EXPORTACAO,
        f"{quote(config.FILTRO_ANO)}={ano}",
        f"{quote(config.FILTRO_NIVEL)}=",  # vazio: remove o filtro padrão (só Doutorado)
    ]
    return f"{config.URL_EXPORTACAO}?{'&'.join(filtros)}"


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(TAMANHO_BLOCO), b""):
            h.update(bloco)
    return h.hexdigest()


def baixar_ano(
    sessao: requests.Session,
    ano: int,
    destino: Path,
    timeout: float,
    tentativas: int,
    espera: float,
) -> str:
    """Baixa o CSV de um ano para `destino`. Devolve a URL usada.

    Tenta de novo em erro de rede, timeout, HTTP 5xx/429 ou resposta que não
    seja CSV (o Tableau devolve HTML quando a view muda de nome ou há bloqueio).
    """
    url = montar_url(ano)
    destino.parent.mkdir(parents=True, exist_ok=True)
    parcial = destino.with_suffix(destino.suffix + ".part")
    ultimo_erro = ""

    for tentativa in range(1, tentativas + 1):
        try:
            with sessao.get(url, headers=CABECALHOS, timeout=timeout, stream=True) as r:
                tipo = r.headers.get("Content-Type", "")
                if r.status_code == 429 or r.status_code >= 500:
                    raise ErroDownload(f"servidor respondeu HTTP {r.status_code}")
                if r.status_code != 200:
                    raise ErroDownload(
                        f"HTTP {r.status_code}. A view ou o workbook podem ter mudado de nome."
                    )
                if "csv" not in tipo:
                    raise ErroDownload(
                        f"resposta do tipo {tipo!r} em vez de CSV (página de erro ou bloqueio)."
                    )
                with open(parcial, "wb") as f:
                    for bloco in r.iter_content(TAMANHO_BLOCO):
                        f.write(bloco)
            parcial.replace(destino)
            return url
        except (requests.RequestException, ErroDownload) as e:
            ultimo_erro = str(e)
            parcial.unlink(missing_ok=True)
            print(f"  tentativa {tentativa}/{tentativas} falhou: {ultimo_erro}")
            if tentativa < tentativas:
                time.sleep(espera * tentativa)

    raise ErroDownload(f"ano {ano}: falhou após {tentativas} tentativas ({ultimo_erro}).")


# ── Manifest ─────────────────────────────────────────────────────────────────

def ler_manifest(pasta: Path) -> dict:
    caminho = pasta / config.NOME_MANIFEST
    if caminho.exists():
        return json.loads(caminho.read_text(encoding="utf-8"))
    return {}


def registrar_no_manifest(pasta: Path, entrada: dict, data_original: str, data_iso: str) -> None:
    """Acrescenta ou substitui a entrada de um ano no manifest da extração."""
    manifest = ler_manifest(pasta)
    manifest.setdefault("data_extracao_original", data_original)
    manifest["data_extracao"] = data_iso
    manifest["formato_data_extracao"] = config.FORMATO_DATA_EXTRACAO
    manifest["fonte"] = config.URL_PAINEL
    manifest.setdefault("anos", {})[str(entrada["ano"])] = entrada
    manifest["anos"] = dict(sorted(manifest["anos"].items()))
    (pasta / config.NOME_MANIFEST).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def agora_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


# ── Fallback manual ──────────────────────────────────────────────────────────

def instrucoes_manuais(anos: list[int]) -> str:
    entrada = config.PASTA_ENTRADA_MANUAL.relative_to(config.RAIZ)
    linhas = [
        "",
        "Download manual (se a automação falhar):",
        f"  1. Abra {config.URL_PAINEL} e vá para a aba \"Download\" do painel.",
        "  2. Em Ano, selecione um único ano; em Nível de Formação, marque todos.",
        "  3. Baixe pelo botão de download do painel ou pelo menu Download da barra",
        "     do Tableau (opção Dados ou Tabela de referência cruzada).",
        "     Os dois formatos são aceitos (UTF-8 com vírgula ou UTF-16 com tabulação).",
        f"  4. Salve cada arquivo em {entrada}\\ com o nome lattes_{{ano}}.csv:",
    ]
    linhas += [f"       {entrada}\\lattes_{ano}.csv" for ano in anos]
    linhas += [
        "  5. Rode de novo `python scripts/baixar_lattes.py`: os arquivos serão",
        "     validados e movidos para a pasta da extração, com o manifest.",
    ]
    return "\n".join(linhas)
