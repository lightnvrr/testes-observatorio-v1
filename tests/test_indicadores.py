"""Testes unitários dos indicadores, com uma base pequena montada à mão.

Base (ano 2023, salvo indicação; p = Totalpessoas):

    STEM formação (Engenharias), atuação em Engenharias, Nordeste:
      F Parda p=2 | F Parda p=1 | F Preta p=1 | F Branca p=2 | F Não desejo declarar p=1
      M Branca p=4 | M Parda p=1 | sexo Não declarado, Preta p=1
    STEM formação (Exatas), atuação em Ciência da Computação, Sudeste:
      F Branca p=1
    Ciências Humanas, atuação "Não informado":
      F Indígena p=1 | M Indígena p=1
    2024: F Indígena p=1 (Humanas, atuação "Não informado") | M Branca p=1 (Engenharias)

Contas de cabeça para 2023:
    geral:           F = 9, M = 6                       -> 9/15 = 60%
    STEM formação:   F = 8, M = 5                       -> 8/13
    Parda (STEM):    F = 3, F+M = 4                     -> 75%
    Negra (STEM):    F = 3+1 = 4, F+M = 5               -> 80%
    mulheres STEM com raça declarada = 3 + 1 + 3 = 7    -> Parda 3/7, Negra 4/7
    não declaração (STEM): F 1/8, M 0/5, Todos 1/13
"""

import pandas as pd
import pytest

from lattes import config
from lattes import indicadores as ind

ANOS = [2023, 2024]
ENG, EXATAS, HUM = "Engenharias", "Ciências Exatas e da Terra", "Ciências Humanas"
NI = "Não informado"


def pessoa(sexo, raca, p=1, ano=2023, ga_f=ENG, ga_a=ENG, area_a="Engenharia Civil",
           regiao_a="Nordeste", nivel="Doutorado"):
    linha = {c: "x" for c in config.COLUNAS_CONSOLIDADAS}
    linha.update({
        "Ano": str(ano), "Sexo": sexo, "Cor ou Raça": raca, "Nível (Formação)": nivel,
        "Grande Área (Formação)": ga_f, "Grande Área (Atuação)": ga_a, "Área (Atuação)": area_a,
        "Região (Atuação)": regiao_a, "Setor de Atividade (Atuação)": "Ensino Superior",
        "Totalpessoas": str(p), "Data Extração BD Lattes": "10/4/2026",
    })
    return linha


def base_mini() -> pd.DataFrame:
    F, M, ND = "Feminino", "Masculino", "Não declarado"
    humanas = {"ga_f": HUM, "ga_a": NI, "area_a": NI, "regiao_a": NI}
    return pd.DataFrame([
        pessoa(F, "Parda", p=2), pessoa(F, "Parda"), pessoa(F, "Preta"), pessoa(F, "Branca", p=2),
        pessoa(F, "Não desejo declarar"), pessoa(M, "Branca", p=4), pessoa(M, "Parda"), pessoa(ND, "Preta"),
        pessoa(F, "Branca", ga_f=EXATAS, ga_a=EXATAS, area_a="Ciência da Computação", regiao_a="Sudeste"),
        pessoa(F, "Indígena", **humanas), pessoa(M, "Indígena", **humanas),
        pessoa(F, "Indígena", ano=2024, **humanas), pessoa(M, "Branca", ano=2024),
    ])


@pytest.fixture
def saida():
    return ind.gerar_indicadores(base_mini(), "2026-10-04", ANOS, agregar_negra=True)


def pega(saida, indicador, recorte="stem_formacao", periodo="2023", raca=None, sexo=None, categoria=None):
    sel = saida[(saida.indicador == indicador) & (saida.recorte == recorte) & (saida.periodo == periodo)]
    if raca is not None:
        sel = sel[sel.raca == raca]
    if sexo is not None:
        sel = sel[sel.sexo == sexo]
    if categoria is not None:
        sel = sel[sel.categoria == categoria]
    assert len(sel) == 1, sel
    return sel.iloc[0]


# ── Numerador, denominador, percentual ───────────────────────────────────────

def test_participacao_feminina_geral_exclui_sexo_nao_declarado(saida):
    r = pega(saida, ind.PARTICIPACAO, recorte="geral")
    assert (r.numerador, r.denominador, r.percentual) == (9, 15, 60.0)
    assert r.raca == ind.TODAS


def test_participacao_feminina_stem(saida):
    r = pega(saida, ind.PARTICIPACAO)
    assert (r.numerador, r.denominador, r.percentual) == (8, 13, round(100 * 8 / 13, 2))


def test_participacao_no_grupo_racial(saida):
    parda = pega(saida, ind.GRUPO_RACIAL, raca="Parda")
    assert (parda.numerador, parda.denominador, parda.percentual) == (3, 4, 75.0)
    # Preta: a pessoa com sexo não declarado não entra no denominador
    preta = pega(saida, ind.GRUPO_RACIAL, raca="Preta")
    assert (preta.numerador, preta.denominador) == (1, 1)


def test_grupo_sem_pessoas_tem_percentual_vazio(saida):
    r = pega(saida, ind.GRUPO_RACIAL, raca="Indígena")
    assert (r.numerador, r.denominador) == (0, 0) and pd.isna(r.percentual)


def test_composicao_racial_exclui_nao_declarado_do_denominador(saida):
    comp = saida[(saida.indicador == ind.COMPOSICAO) & (saida.recorte == "stem_formacao")
                 & (saida.periodo == "2023")]
    assert set(comp.denominador) == {7}  # 8 mulheres, 1 não declarou raça
    assert pega(saida, ind.COMPOSICAO, raca="Parda").numerador == 3
    assert comp[~comp.raca_agregada].numerador.sum() == 7


def test_taxa_nao_declaracao_raca_por_sexo(saida):
    f = pega(saida, ind.TAXA_ND_RACA, sexo="Feminino")
    m = pega(saida, ind.TAXA_ND_RACA, sexo="Masculino")
    todos = pega(saida, ind.TAXA_ND_RACA, sexo=ind.TODOS)
    assert (f.numerador, f.denominador) == (1, 8)
    assert (m.numerador, m.denominador) == (0, 5)
    # Todos = Feminino + Masculino (sexo não declarado fica de fora)
    assert (todos.numerador, todos.denominador) == (1, 13)


def test_conta_pessoas_e_linhas_separadamente(saida):
    r = pega(saida, ind.COMPOSICAO, raca="Parda")
    assert (r.numerador, r.n_linhas_numerador) == (3, 2)


def test_periodo_agregado(saida):
    r = pega(saida, ind.PARTICIPACAO, recorte="geral", periodo="2023-2024")
    assert (r.numerador, r.denominador) == (10, 17)


# ── Categoria Negra ──────────────────────────────────────────────────────────

def test_negra_e_preta_mais_parda(saida):
    negra = pega(saida, ind.GRUPO_RACIAL, raca="Negra")
    assert (negra.numerador, negra.denominador, negra.percentual) == (4, 5, 80.0)
    assert negra.raca_agregada
    comp = pega(saida, ind.COMPOSICAO, raca="Negra")
    assert (comp.numerador, comp.denominador) == (4, 7)


def test_saida_sem_negra_e_identica_exceto_linhas_negra(saida):
    sem = ind.gerar_indicadores(base_mini(), "2026-10-04", ANOS, agregar_negra=False)
    com = saida[saida.raca != "Negra"].reset_index(drop=True)
    pd.testing.assert_frame_equal(com, sem.reset_index(drop=True))
    assert (saida.raca == "Negra").any() and not (sem.raca == "Negra").any()


# ── Flags ────────────────────────────────────────────────────────────────────

def test_flags_seguem_a_regra_de_cada_indicador(monkeypatch):
    monkeypatch.setattr(config, "LIMITE_DENOMINADOR", 5)
    monkeypatch.setattr(config, "LIMITE_NUMERADOR", 3)
    s = ind.gerar_indicadores(base_mini(), "2026-10-04", ANOS)

    geral = pega(s, ind.PARTICIPACAO, recorte="geral")          # den 15
    parda = pega(s, ind.GRUPO_RACIAL, raca="Parda")             # den 4
    assert not geral.flag_denominador_pequeno and parda.flag_denominador_pequeno
    assert not geral.flag_numerador_pequeno and not parda.flag_numerador_pequeno

    comp_parda = pega(s, ind.COMPOSICAO, raca="Parda")          # num 3
    comp_preta = pega(s, ind.COMPOSICAO, raca="Preta")          # num 1
    assert not comp_parda.flag_numerador_pequeno and comp_preta.flag_numerador_pequeno
    assert not s[s.indicador == ind.COMPOSICAO].flag_denominador_pequeno.any()


def test_indigena_anual_prefere_agregado(saida):
    assert pega(saida, ind.COMPOSICAO, recorte="geral", raca="Indígena").flag_preferir_agregado
    assert not pega(saida, ind.COMPOSICAO, recorte="geral", periodo="2023-2024",
                    raca="Indígena").flag_preferir_agregado
    assert not pega(saida, ind.COMPOSICAO, recorte="geral", raca="Branca").flag_preferir_agregado


# ── Bases temporais e recortes ───────────────────────────────────────────────

def test_situacao_atual_so_no_agregado(saida):
    situacao = saida[saida.base == ind.BASE_SITUACAO]
    assert set(situacao.periodo) == {"2023-2024"}
    assert set(situacao.recorte) == {"stem_atuacao", "computacao_atuacao", "computacao_regiao_atuacao"}
    r = pega(saida, ind.PARTICIPACAO, recorte="stem_atuacao", periodo="2023-2024")
    assert (r.numerador, r.denominador) == (8, 14)


def test_regiao_nao_informado_fica_fora_das_categorias(saida):
    regioes = saida[saida.recorte == "computacao_regiao_atuacao"]
    assert set(regioes.categoria) == {"Nordeste", "Sudeste"}
    sudeste = pega(saida, ind.PARTICIPACAO, recorte="computacao_regiao_atuacao",
                   periodo="2023-2024", categoria="Sudeste")
    assert (sudeste.numerador, sudeste.denominador) == (1, 1)


def test_recortes_sem_raca(saida):
    for recorte in ("grande_area_formacao", "computacao_atuacao", "computacao_regiao_atuacao"):
        assert set(saida[saida.recorte == recorte].indicador) == {ind.PARTICIPACAO}


# ── Domínios ─────────────────────────────────────────────────────────────────

def test_raca_desconhecida_interrompe():
    df = base_mini()
    df.loc[0, "Cor ou Raça"] = "Morena"
    with pytest.raises(ind.ErroDominio, match="Morena"):
        ind.gerar_indicadores(df, "2026-10-04", ANOS)


def test_grande_area_stem_ausente_interrompe():
    df = base_mini().replace({EXATAS: "Ciencias Exatas"})
    with pytest.raises(ind.ErroDominio, match="STEM"):
        ind.gerar_indicadores(df, "2026-10-04", ANOS)


def test_ano_fora_da_lista_interrompe():
    with pytest.raises(ind.ErroDominio, match="Ano"):
        ind.gerar_indicadores(base_mini(), "2026-10-04", [2023])


# ── Qualidade e dicionário ───────────────────────────────────────────────────

def test_qualidade_taxa_nao_informado_e_sexo_nao_declarado():
    q = ind.gerar_qualidade(base_mini(), ANOS)
    ga = q[(q.verificacao == "taxa_nao_informado") & (q.campo == "Grande Área (Atuação)")
           & (q.recorte == "geral") & (q.periodo == "2023")]
    assert ga.set_index("sexo")[["numerador", "denominador"]].to_dict("index") == {
        "Feminino": {"numerador": 1, "denominador": 9},
        "Masculino": {"numerador": 1, "denominador": 6},
        "Todos": {"numerador": 2, "denominador": 15},
    }
    nd = q[(q.verificacao == "sexo_nao_declarado") & (q.periodo == "2023")].iloc[0]
    assert (nd.numerador, nd.denominador) == (1, 16)
    preta_nd = q[(q.verificacao == "raca_no_sexo_nao_declarado") & (q.periodo == "2023")
                 & (q.categoria == "Preta")].iloc[0]
    assert (preta_nd.numerador, preta_nd.denominador) == (1, 1)


def test_qualidade_distribuicao_de_grande_area():
    q = ind.gerar_qualidade(base_mini(), ANOS)
    dist = q[(q.verificacao == "distribuicao_grande_area") & (q.campo == "Grande Área (Formação)")]
    # 17 pessoas com sexo declarado: Engenharias 13, Exatas 1, Humanas 3
    assert dist.set_index("categoria").numerador.to_dict() == {ENG: 13, EXATAS: 1, HUM: 3}
    assert set(dist.denominador) == {17}


def test_qualidade_bolsas_ja_recebidas():
    bolsas = base_mini()
    for coluna in config.COLUNAS_BOLSAS_QUALIDADE:
        bolsas[coluna] = "Não"
    bolsas.loc[0, "Bolsista - Iniciação Científica"] = "Sim"   # F Parda, p=2, Doutorado
    bolsas.loc[5, "Bolsista - Iniciação Científica"] = ""      # vazio (bruto antigo) conta como não
    q = ind.gerar_qualidade(base_mini(), ANOS, bolsas=bolsas)
    ic = q[(q.verificacao == "bolsa_ja_recebida") & (q.campo == "Bolsista - Iniciação Científica")
           & (q.recorte == "nivel_formacao") & (q.categoria == "Doutorado")]
    assert ic.set_index("sexo")[["numerador", "denominador"]].to_dict("index") == {
        "Feminino": {"numerador": 2, "denominador": 10},
        "Masculino": {"numerador": 0, "denominador": 7},
        "Todos": {"numerador": 2, "denominador": 17},
    }
    sem_bolsas = ind.gerar_qualidade(base_mini(), ANOS)
    assert not (sem_bolsas.verificacao == "bolsa_ja_recebida").any()


def test_dicionario_monta_ressalvas_com_os_dados():
    q = ind.gerar_qualidade(base_mini(), ANOS)
    d = ind.gerar_dicionario(q, "2026-10-04", ANOS).set_index("codigo")
    # Grande Área de atuação "Não informado" em 2023-2024: F 2 de 10, M 1 de 7
    assert "20,0% das mulheres e 14,3% dos homens" in d.loc["stem_atuacao", "ressalva"]
    assert d.loc[ind.BASE_SITUACAO, "nome"] == "Situação em out/2026 das pessoas tituladas de 2023 a 2024"
    assert "vínculo de atuação registrado" in d.loc["computacao_regiao_atuacao", "descricao"]
    assert set(d.index) >= {ind.PARTICIPACAO, ind.GRUPO_RACIAL, ind.COMPOSICAO, ind.TAXA_ND_RACA}
