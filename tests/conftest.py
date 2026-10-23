"""Fixtures compartilhadas e regras dos testes de dados."""

import json

import pytest

from lattes import config as cfg


def pytest_collection_modifyitems(config, items):
    """Testes `dados` são pulados se os brutos da extração não estiverem em data/raw/."""
    pasta = cfg.pasta_extracao(cfg.EXTRACAO)
    faltando = [a for a in cfg.ANOS if not (pasta / f"lattes_{a}.csv").exists()]
    if not faltando:
        return
    motivo = f"brutos ausentes em {pasta.relative_to(cfg.RAIZ)} para {faltando}"
    for item in items:
        if "dados" in item.keywords:
            item.add_marker(pytest.mark.skip(reason=motivo))


@pytest.fixture(scope="session")
def referencia() -> dict:
    """Referência da extração usada (tests/referencias/{EXTRACAO}.json)."""
    caminho = cfg.PASTA_REFERENCIAS / f"{cfg.EXTRACAO}.json"
    if not caminho.exists():
        pytest.fail(f"referência ausente: {caminho}")
    return json.loads(caminho.read_text(encoding="utf-8"))
