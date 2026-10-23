# Origem dos números da metodologia V1

Cada número citado em [metodologia_lattes.md](metodologia_lattes.md), com o arquivo de onde saiu e o filtro usado. Extração de referência: 2026-10-04. Caminhos relativos à raiz do projeto.

Abreviações dos arquivos:
- **MAN**: `data/raw/2026-10-04/manifest.json`
- **CMETA**: `data/processed/lattes_consolidado.meta.json`
- **IMETA**: `data/processed/indicadores/indicadores_v1.meta.json`
- **IND**: `data/processed/indicadores/indicadores_v1.csv`
- **QUAL**: `data/processed/indicadores/qualidade_v1.csv`
- **NT**: Nota Técnica 01/2024 (`docs/nota_tecnica_painel_lattes.pdf`)

Em IND e QUAL, "agregado" é `periodo = 2020-2025`, e "Todos" é `sexo = Todos` (Feminino + Masculino).

## Caracterização

| Número no documento | Onde aparece | Origem |
| --- | --- | --- |
| 4/10/2026 (4 de outubro de 2026) | cabeçalho, seções 1, 5 e 3.1 | MAN `data_extracao` = `2026-10-04` (`data_extracao_original` = `10/4/2026`) |
| 18 colunas (16 + 2) | "O que mudou" 9, seções 1 e 3.1 | CMETA `colunas` (18 itens); `config.COLUNAS_ANALITICAS` (16) + `COLUNAS_CONTROLE` (2) |
| 2020 a 2025 | várias | IMETA `anos` e CMETA `anos` |
| 60 meses | seções 1, 2 e 4.4 | NT, "Período de coleta dos dados" |
| 1948 | seções 1 e 4.4 | NT, "Evolução por ano" |
| Pessoas por ano: 53.178; 62.739; 71.359; 82.976; 81.923; 78.130; 45.434 (2026) | tabela "Volume" e seção 5 | MAN `anos.{ano}.n_pessoas` (2020 a 2025 iguais em CMETA `por_ano`) |
| Linhas por ano: 52.691; 61.910; 70.264; 81.473; 80.170; 76.065; 44.414 (2026) | tabela "Volume" | MAN `anos.{ano}.n_linhas` |
| Tamanho: 20,9; 24,6; 27,9; 32,3; 31,7; 30,1; 17,5 MB | tabela "Volume" | MAN `anos.{ano}.tamanho_bytes` / 10⁶, uma casa |
| 430.305 pessoas; 422.573 linhas | tabela "Volume" | CMETA `n_pessoas`, `n_linhas` |

## Limitações (seção 2)

| Número | Limitação | Origem |
| --- | --- | --- |
| 5,60% | 8 e 9 | IND `taxa_nao_declaracao_raca`, `recorte = geral`, agregado, Todos (23.884 / 426.186) |
| 5,17% (mulheres); 6,17% (homens) | 8 | IND idem, `sexo = Feminino` (12.431 / 240.486) e `Masculino` (11.453 / 185.700) |
| 6,67% (2020); 4,77% (2025) | 8 | IND idem, `periodo = 2020` (3.523 / 52.800) e `2025` (3.686 / 77.212), Todos |
| 4.119 pessoas; 0,96% | 9 | QUAL `sexo_nao_declarado`, agregado (4.119 / 430.305) |
| 0,71% (2020); 1,17% (2025) | 9 | QUAL `sexo_nao_declarado`, `periodo = 2020` (378 / 53.178) e `2025` (918 / 78.130) |
| 35,81% (Preta no sexo não declarado) | 9 | QUAL `raca_no_sexo_nao_declarado`, agregado, `categoria = Preta` (1.475 / 4.119) |
| 8,23% (Preta no sexo declarado) | 9 | QUAL `raca_no_sexo_declarado`, agregado, `categoria = Preta` (35.080 / 426.186) |
| 22,87% (não declara raça, sexo não declarado) | 9 | QUAL `raca_no_sexo_nao_declarado`, agregado, `categoria = Não desejo declarar` (942 / 4.119) |
| 5,60% (não declara raça, sexo declarado) | 9 | QUAL `raca_no_sexo_declarado`, agregado, `categoria = Não desejo declarar` (23.884 / 426.186) |
| 17,50% (Grande Área Atuação) | 10 | QUAL `taxa_nao_informado`, `campo = Grande Área (Atuação)`, `recorte = geral`, agregado, Todos (74.579 / 426.186) |
| 5,55% (Grande Área Formação) | 10 | QUAL idem, `campo = Grande Área (Formação)` (23.634 / 426.186) |
| 26,45% (Região Atuação) | 10 | QUAL idem, `campo = Região (Atuação)` (112.712 / 426.186) |
| 18,31% (mulheres); 16,44% (homens) | 10 | QUAL `campo = Grande Área (Atuação)`, `recorte = geral`, agregado, `sexo = Feminino` (44.044 / 240.486) e `Masculino` (30.535 / 185.700) |
| 20,98% (mulheres); 18,33% (homens), formados em STEM | 10 | QUAL idem, `recorte = stem_formacao` (4.584 / 21.845 e 7.547 / 41.181) |
| 23,08% (mulheres); 24,06% (homens), Computação | 10 | QUAL `campo = Região (Atuação)`, `recorte = computacao_atuacao`, agregado (390 / 1.690 e 1.825 / 7.586) |
| 47,07% (Setor) | 11 e 4.3 | QUAL `campo = Setor de Atividade (Atuação)`, `recorte = geral`, agregado, Todos (200.587 / 426.186) |
| 23,11% (Enquadramento) | 11 e 4.3 | QUAL `campo = Enquadramento (Atuação)`, idem (98.508 / 426.186) |
| 8,23% ("Outra" na formação) | 12 | QUAL `distribuicao_grande_area`, `campo = Grande Área (Formação)`, `categoria = Outra` (35.069 / 426.186) |
| 1,16% ("Outra" na atuação) | 12 | QUAL idem, `campo = Grande Área (Atuação)` (4.937 / 426.186) |
| 2 pessoas ("Tecnologias", formação) | 12 | QUAL `distribuicao_grande_area`, `Grande Área (Formação)`, `categoria = Tecnologias` |
| 40 pessoas ("Tecnologias", atuação) | 12 | QUAL idem, `Grande Área (Atuação)` |
| 1 pessoa ("Serviço Social", atuação) | 12 | QUAL idem, `categoria = Serviço Social` |
| 19,88% (IC entre doutores) | 14 | QUAL `bolsa_ja_recebida`, `campo = Bolsista - Iniciação Científica`, `recorte = nivel_formacao`, `categoria = Doutorado`, Todos (27.913 / 140.397) |
| 11,53% (bolsa de mestrado entre doutores) | 14 | QUAL idem, `campo = Bolsista - Mestrado` (16.191 / 140.397) |
| 10,20% (bolsa de doutorado entre doutores) | 14 | QUAL idem, `campo = Bolsista - Doutorado` (14.320 / 140.397) |
| 39 pessoas (Indígena, STEM formação 2023) | 18 | IND `participacao_feminina_no_grupo_racial`, `recorte = stem_formacao`, `periodo = 2023`, `raca = Indígena`, `denominador` |
| 178 pessoas (Indígena, STEM formação agregado) | 18 | IND idem, agregado, `denominador` |

## Matriz de indicadores (seção 4)

| Número | Onde | Origem |
| --- | --- | --- |
| 30 (limite do denominador) | 4.1 | IMETA `limite_denominador` |
| 10 (limite do numerador) | 4.1 | IMETA `limite_numerador` |
| 34,66% (STEM formação, agregado) | 4.2 | IND `participacao_feminina`, `recorte = stem_formacao`, agregado (21.845 / 63.026) |
| 351 pessoas com PQ; 76 mulheres | 4.3 | QUAL `bolsa_ja_recebida`, `campo = Bolsista - PQ`, `recorte = geral`, agregado, `sexo = Todos` e `Feminino` |
| 68 pessoas com DT; 21 mulheres | 4.3 | QUAL idem, `campo = Bolsista - DT` |
| Níveis 1A, 1B, 1C, 1D e 2 | 3.2 e 4.4 | NT, "Bolsas do CNPq" |
| Grupos de 5 anos (faixa etária) | 3.2 | NT, "Sexo, Cor/Raça, Faixa Etária e País de Nascimento" |

## Nota sobre 2026 (seção 5)

| Número | Origem |
| --- | --- |
| 45.434 pessoas (2026) | MAN `anos.2026.n_pessoas` |
| 78.130 pessoas (2025) | MAN `anos.2025.n_pessoas` (igual em CMETA `por_ano.2025`) |

## Números que não vêm das saídas

Nenhum valor numérico de resultado vem de fora das saídas atuais. Os únicos números que não são resultados do pipeline são as regras da fonte (60 meses, 1948, níveis de bolsa, grupos de faixa etária), todos da NT, e os parâmetros de configuração (anos, limites das flags).
