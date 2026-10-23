import pandas as pd
import os

# ── Configuração ──────────────────────────────────────────────────────────────
PASTA_RAW   = "data/raw"
PASTA_OUT   = "data/processed"
ARQUIVO_OUT = "dados_lattes_consolidado.csv"

ANOS = [2020, 2021, 2022, 2023, 2024, 2025]

# Só as colunas necessárias para a análise — ignora o resto (reduz ~90% do tamanho)
COLUNAS = [
    "Ano",
    "Sexo",
    "Cor ou Raça",
    "Região (Formação)",
    "UF (Formação)",
    "Grande Área (Formação)",
    "Área (Formação)",
    "Nível (Formação)",
    "Região (Atuação)",
    "UF (Atuação)",
    "Grande Área (Atuação)",
    "Área (Atuação)",
    "Setor de Atividade (Atuação)",
    "Enquadramento (Atuação)",
    "Bolsista - PQ",
    "Bolsista - DT",
]
# ─────────────────────────────────────────────────────────────────────────────

os.makedirs(PASTA_OUT, exist_ok=True)
saida = os.path.join(PASTA_OUT, ARQUIVO_OUT)

primeiro = True  # controla o header no CSV de saída

for ano in ANOS:
    caminho = os.path.join(PASTA_RAW, f"lattes_{ano}.csv")
    if not os.path.exists(caminho):
        print(f"[AVISO] Não encontrado: {caminho} — pulando.")
        continue

    print(f"Lendo {caminho}...", end=" ", flush=True)
    df = pd.read_csv(caminho, encoding="utf-16", sep="\t")

    # Limpa nomes de coluna (remove ponto inicial)
    df.columns = [c.lstrip(".").strip() for c in df.columns]

    # Garante coluna Ano
    if "Ano" not in df.columns:
        df["Ano"] = ano

    # Filtra só as colunas de interesse (ignora as que não existirem)
    cols_existentes = [c for c in COLUNAS if c in df.columns]
    df = df[cols_existentes]

    # Salva diretamente no CSV (append), sem acumular na memória
    df.to_csv(saida, mode="w" if primeiro else "a",
              header=primeiro, index=False, encoding="utf-8")
    primeiro = False

    print(f"{len(df):,} linhas salvas.")

print(f"\n✅ Concluído! Arquivo: {saida}")

# Mostra resumo final
resultado = pd.read_csv(saida)
print(f"   Total de linhas : {len(resultado):,}")
print(f"   Colunas         : {list(resultado.columns)}")
print(f"   Anos            : {sorted(resultado['Ano'].unique())}")
print(f"   Sexo            : {resultado['Sexo'].value_counts().to_dict()}")