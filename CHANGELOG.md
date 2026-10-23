# Changelog

## V1 fechada (2026-10-23), tag `v1.0-lattes`

- Decisões metodológicas aprovadas pela coordenação do projeto em 23/10/2026: `docs/registro_decisoes_v1.md` (substitui `docs/decisoes_professora.md`). A categoria Negra deixa de ser padrão provisório e passa a ser decisão.
- Metodologia final: sem linguagem de pendência, com as seções "Decisões metodológicas da V1" e "Perguntas em aberto ao CNPq", em Markdown simples para importar no Notion.
- Novos documentos: `docs/integracao_observatorio.md` (contrato de dados, chave única, regras de exibição, atualização e perguntas para a equipe do observatório) e `docs/perguntas_cnpq.md` (texto para o Fala.BR).
- Removido `docs/pendencias_fase5.md`; cada item foi para a metodologia, o registro de decisões, as perguntas ao CNPq ou a integração.
- Testes novos: decisões da V1 no `config`, chave única de `indicadores_v1.csv`, coerência da documentação (números mapeados e iguais às saídas, links, ausência de travessões).
- `tests/referencias/2026-10-04.json` conferido por Jamily Barbosa de Oliveira em 2026-10-23.
- README com a seção "Como reproduzir a V1".
- Leitura das bolsas dos brutos movida para `lattes.consolidacao.ler_bolsas`.

## V1, desenvolvimento (2026-10-23)

Primeira versão do pipeline da base Lattes do KatieNet / Observatório de Mulheres na Ciência. A base de referência é a extração de 4/10/2026 do Painel de Formação e Atuação do Lattes (CNPq).

### Pipeline
- **Download automatizado** (`scripts/baixar_lattes.py`): usa a exportação CSV do workbook do CNPq no Tableau Public, um ano por vez, com retentativas e pausa entre anos. Os brutos ficam em `data/raw/{data_extracao}/` com `manifest.json` (SHA-256, linhas, pessoas, data de extração). Há fallback para download manual.
- **Leitura e validação** dos dois formatos do painel: UTF-8 com vírgula (exportação por URL) e UTF-16 com tabulação (interface).
- **Consolidação** (`scripts/consolidar_lattes.py`): coortes de 2020 a 2025 em 18 colunas (16 de análise + `Totalpessoas` + `Data Extração BD Lattes`), sem remover registros. Para se um bruto foi alterado depois do download ou se aparece categoria nova.
- **Indicadores** (`scripts/gerar_indicadores.py`): formato longo para o front, contando pessoas. Inclui o recorte de raça: participação feminina dentro do grupo racial, composição racial das mulheres e taxa de não declaração de raça. Traz flags de amostra pequena e a categoria Negra opcional. A saída vem acompanhada de dicionário, meta e relatório de qualidade.

### Metodologia
- Nova `docs/metodologia_lattes.md`; a versão de julho/2026 está preservada em `docs/historico/`.
- `Ano` passa a ser o ano da última titulação, e a unidade, a pessoa (Nota Técnica 01/2024).
- Os indicadores de situação atual passam a valer só para o agregado 2020 a 2025.
- PQ, DT, setor e enquadramento ficam fora da V1.
- 2026 continua fora, agora porque a coorte de titulação está incompleta.
- `docs/decisoes_professora.md`: decisões pendentes, com recomendação (depois `docs/registro_decisoes_v1.md`).
- `docs/numeros_metodologia_v1.md`: origem de cada número da metodologia.

### Testes
- `pytest`: unitários com uma base montada à mão (leitura, validação, consolidação, indicadores, flags, categoria Negra, qualidade, dicionário).
- `pytest -m dados`: contagens contra `tests/referencias/2026-10-04.json`, domínios das categorias e identidades entre indicadores.
- `pytest -m rede`: acesso ao painel e à exportação.
