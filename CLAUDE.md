# CLAUDE.md

Projeto da base Lattes do **KatieNet / Observatório de Mulheres na Ciência** (UFAL). O observatório publica dados públicos sobre a presença feminina em STEM; a Lattes é uma das fontes. Estamos fechando a **V1** desta parte.

## Como trabalhar neste projeto

- Responder e escrever comentários, docstrings e documentação em **português**. Evitar travessões nos textos.
- Trabalhar em fases, com resumo curto no fim de cada uma e esperar o ok antes de seguir.
- **Nunca inventar nomes de categorias.** Toda string de filtro (grande área, raça, setor etc.) deve ser conferida contra os valores distintos reais da base.
- Não mudar a definição de STEM, não remover registros e não alterar a lista de anos sem perguntar.
- Números esperados (contagens, percentuais) só nos **testes**, nunca fixos no código do pipeline.
- Inconsistência entre documentação e dados: avisar e propor correção, não decidir sozinho.
- Ambiente: Python 3.11+ (máquina tem 3.14), pandas, pytest, `.venv` + `requirements.txt` (instala o pacote `src/lattes` em modo editável). No Windows o comando é `py`, não `python`, fora da venv.

## Fonte e formato

- Painel Formação e Atuação Lattes do CNPq: `http://bi.cnpq.br/painel/formacao-atuacao-lattes/` (**http**, não https). A página só embute o workbook `PainelLattes-FormaoeAtuao` do **Tableau Public**; os brutos vêm da exportação CSV da aba "Painel - Download" (detalhes em `src/lattes/config.py`).
- **`Ano` = ano de obtenção da última titulação** (campo `ANOOBTENCAOTITULO`), não ano de extrato. Todos os anos vêm de uma única extração (`Data Extração BD Lattes`). Cada pessoa aparece uma vez, pela última titulação (`Nível` = maior título). Universo: CVs atualizados nos últimos 60 meses. Fonte: `docs/nota_tecnica_painel_lattes.pdf` (Nota Técnica 01/2024 do CNPq).
- Indicadores de formação são por ano de titulação. Indicadores de situação atual (atuação, setor, enquadramento, Computação, região de atuação) usam 2020 a 2025 agregado, rotulados como "situação em out/2026 das pessoas tituladas de 2020 a 2025". **PQ fora da V1.**
- Bolsas vêm da Plataforma Carlos Chagas e são **histórico** ("já recebeu"), não vigentes.
- Brutos guardados como vieram em `data/raw/{data_extracao}/lattes_{ano}.csv`, com `manifest.json` por extração. Formatos aceitos: UTF-8 com vírgula (exportação por URL) e UTF-16 com tabulação (interface).
- Cada linha tem `Totalpessoas`: **indicadores somam pessoas**, e `n_linhas` vai junto para auditoria.
- Data de extração no CSV está em mês/dia/ano (`10/4/2026` = 2026-10-04, confirmado pelo extrato .hyper do workbook).
- **Base da V1: extração de 2026-10-04.** Os brutos antigos (UTF-16) não existem mais; as contagens e percentuais antigos da documentação (415.920, 34,7%, 26,9%, 17,4%, 5,6%) não são reproduzíveis e servem só como histórico.
- Números de referência ficam em `tests/referencias/{data_extracao}.json`, conferidos uma vez pela usuária; nunca no código.
- Consolidação: anos de `config.ANOS` (2020 a 2025; 2026 fora da V1, decidido), **18 colunas** (16 de análise + `Totalpessoas` + `Data Extração BD Lattes`), UTF-8, vírgula. Nenhum registro é removido. Extração base em `config.EXTRACAO`.
- Pendências para a metodologia acumuladas em `docs/pendencias_fase5.md`.

## Definições

- **STEM**: `Grande Área ∈ {"Ciências Exatas e da Terra", "Engenharias"}`. Na extração antiga, a participação feminina em STEM (formação) era 34,7% (26,9% com a lista antiga de áreas); valor histórico, não reproduzível.
- Na extração antiga, `Grande Área (Atuação)` tinha 17,4% de "Não informado" e Formação 5,6% (histórico; recalcular na extração atual).
- "Não informado" em Região, UF e Setor e "Não desejo declarar" em raça saem do denominador; as taxas de não informado / não declarado são indicadores próprios.
- **Recorte de raça (`Cor ou Raça`) entra na V1** (confirmado pela professora). Dois indicadores distintos, que não podem ser confundidos:
  - *Participação feminina dentro do grupo racial*: entre os registros da raça R, % de mulheres (denominador: raça R com sexo declarado).
  - *Composição racial das mulheres*: entre as mulheres, % da raça R (denominador: mulheres com raça declarada).

## Estrutura

- `src/lattes/config.py`: anos, caminhos, colunas consolidadas, definição de STEM.
- `src/lattes/`: funções reutilizáveis. `scripts/`: pontos de entrada (baixar, consolidar, gerar indicadores).
- `docs/metodologia_lattes.md`: documentação metodológica (fonte de verdade das definições).
- `tests/`: `pytest` roda só unitários; `pytest -m dados` exige `data/raw/` preenchido; `pytest -m rede` acessa o painel.
