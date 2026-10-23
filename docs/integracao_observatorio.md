# Integração da base Lattes ao KatieNet / Observatório de Mulheres na Ciência

Guia para quem vai integrar a base Lattes ao observatório. Não é preciso conhecer o histórico do projeto: as definições estão na [metodologia V1](metodologia_lattes.md) e as decisões, no [registro de decisões](registro_decisoes_v1.md).

**Situação:** V1 fechada, extração de referência de 4/10/2026, coortes de titulação de 2020 a 2025.

---

## 1. O que a base entrega

Os quatro arquivos ficam em `data/processed/indicadores/` e são gerados por `python scripts/gerar_indicadores.py`.

| Arquivo | Papel | Público? |
| --- | --- | --- |
| `indicadores_v1.csv` | Os indicadores, em formato longo: uma linha por indicador, base temporal, período, recorte, categoria, sexo e raça, com numerador, denominador, percentual e flags. **É o arquivo que o front consome.** | Sim |
| `indicadores_dicionario.csv` | Nome legível, descrição, numerador, denominador, flag recomendada e ressalva de cada indicador, base temporal e recorte. **É a fonte dos rótulos e textos do front.** | Sim (os textos) |
| `indicadores_v1.meta.json` | Proveniência: extração, anos, parâmetros (categoria Negra, limites das flags, definição de STEM), SHA-256 do consolidado e número de linhas por indicador. | Para a equipe |
| `qualidade_v1.csv` | Taxas de "Não informado", sexo não declarado, distribuição de grandes áreas e bolsas já recebidas. Serve à metodologia. | **Não** |

O consolidado (`data/processed/lattes_consolidado.csv`) é um insumo intermediário, com dados por combinação de atributos. Não deve ir para o front.

Formato dos CSVs: UTF-8 sem BOM, separador vírgula, cabeçalho na primeira linha. Valores booleanos são escritos como `True` e `False`. Percentual vazio significa denominador zero.

---

## 2. Contrato de dados do `indicadores_v1.csv`

### 2.1 Colunas

| Coluna | Tipo | Valores possíveis | Significado |
| --- | --- | --- | --- |
| `indicador` | texto | `participacao_feminina`, `participacao_feminina_no_grupo_racial`, `composicao_racial_das_mulheres`, `taxa_nao_declaracao_raca` | Qual indicador. Ver a seção 4.2 da metodologia. |
| `base` | texto | `coorte_titulacao`, `situacao_na_extracao` | Base temporal. `coorte_titulacao`: pessoas tituladas no período. `situacao_na_extracao`: situação de atuação na data da extração das pessoas tituladas no período. |
| `periodo` | texto | `2020`, `2021`, `2022`, `2023`, `2024`, `2025`, `2020-2025` | Ano de titulação ou agregado. Na base `situacao_na_extracao`, só `2020-2025`. Ler como texto, não como número. |
| `recorte` | texto | `geral`, `stem_formacao`, `nivel_formacao`, `grande_area_formacao` (base `coorte_titulacao`); `stem_atuacao`, `computacao_atuacao`, `computacao_regiao_atuacao` (base `situacao_na_extracao`) | Dimensão do recorte. |
| `categoria` | texto | `geral`: `Todas as áreas`. `stem_formacao` e `stem_atuacao`: `STEM`. `nivel_formacao`: `Mestrado`, `Mestrado Profissional`, `Doutorado`. `grande_area_formacao`: as grandes áreas de formação da base, exceto "Não informado". `computacao_atuacao`: `Ciência da Computação`. `computacao_regiao_atuacao`: `Centro-Oeste`, `Nordeste`, `Norte`, `Sudeste`, `Sul`. | Valor do recorte. As grandes áreas vêm dos dados (ver os domínios em `tests/referencias/2026-10-04.json`). |
| `sexo` | texto | `Todos`, `Feminino`, `Masculino` | Sexo da população do denominador. `participacao_feminina` e `participacao_feminina_no_grupo_racial`: `Todos`. `composicao_racial_das_mulheres`: `Feminino`. `taxa_nao_declaracao_raca`: os três. `Todos` é sempre Feminino + Masculino. |
| `raca` | texto | `Todas`, `Branca`, `Parda`, `Preta`, `Amarela`, `Indígena`, `Negra`, `Não desejo declarar` | Grupo racial. `Todas` = sem recorte racial. `Não desejo declarar` só aparece em `taxa_nao_declaracao_raca`. |
| `raca_agregada` | booleano | `True`, `False` | `True` só na linha `Negra` (Preta + Parda). Linhas agregadas não podem ser somadas com as desagregadas. |
| `numerador` | inteiro | ≥ 0 | Pessoas no numerador (soma de `Totalpessoas`). |
| `denominador` | inteiro | ≥ 0 | Pessoas no denominador. |
| `percentual` | decimal ou vazio | 0 a 100, duas casas | `100 × numerador / denominador`. Vazio quando o denominador é zero. |
| `n_linhas_numerador` | inteiro | ≥ 0 | Linhas do consolidado somadas no numerador. Só para auditoria. |
| `n_linhas_denominador` | inteiro | ≥ 0 | Idem, para o denominador. |
| `flag_denominador_pequeno` | booleano | `True`, `False` | Denominador abaixo do limite (`limite_denominador` no meta). Aplica-se a `participacao_feminina`, `participacao_feminina_no_grupo_racial` e `taxa_nao_declaracao_raca`. |
| `flag_numerador_pequeno` | booleano | `True`, `False` | Numerador abaixo do limite (`limite_numerador` no meta). Aplica-se a `composicao_racial_das_mulheres`. |
| `flag_preferir_agregado` | booleano | `True`, `False` | `True` nas linhas anuais dos grupos de `racas_preferir_agregado` no meta (hoje, Indígena). |
| `extracao` | texto (data ISO) | ex.: `2026-10-04` | Extração de origem. Todas as linhas de um arquivo têm a mesma extração. |

### 2.2 Chave única

Dentro de um arquivo, cada linha é identificada por:

`indicador`, `base`, `periodo`, `recorte`, `categoria`, `sexo`, `raca`

Ao guardar várias extrações juntas, acrescente `extracao` à chave. A chave está no código (`CHAVE_INDICADORES` em `src/lattes/indicadores.py`) e há testes, na base de teste e nos dados reais, que confirmam que ela não tem duplicatas.

### 2.3 Combinações que existem

- Os indicadores raciais (`participacao_feminina_no_grupo_racial`, `composicao_racial_das_mulheres`, `taxa_nao_declaracao_raca`) só existem nos recortes `geral`, `stem_formacao`, `nivel_formacao` e `stem_atuacao`.
- Os recortes `grande_area_formacao`, `computacao_atuacao` e `computacao_regiao_atuacao` só têm `participacao_feminina`.
- A base `situacao_na_extracao` só tem o período `2020-2025`.

### 2.4 Ligação com o dicionário

`indicadores_dicionario.csv` tem as colunas `tipo`, `codigo`, `nome`, `descricao`, `numerador`, `denominador`, `flag_recomendada` e `ressalva`. Cada linha de indicadores se liga a três linhas do dicionário:

- `indicador` → linha com `tipo = indicador` e `codigo` igual;
- `base` → linha com `tipo = base`;
- `recorte` → linha com `tipo = recorte`.

---

## 3. Regras de exibição para o front

### 3.1 Flags

| Flag | O que fazer |
| --- | --- |
| `flag_denominador_pequeno = True` | Não exibir o percentual sem um aviso visível de amostra pequena, mostrando o denominador (n). Em gráficos, marcar o ponto de forma diferente ou omiti-lo com nota. |
| `flag_numerador_pequeno = True` | Exibir com aviso. Em séries por ano, não destacar variações entre anos: com poucas pessoas, a diferença parece grande mesmo que o percentual seja preciso. |
| `flag_preferir_agregado = True` | Mostrar como número principal a linha do mesmo recorte com `periodo = 2020-2025`. Os valores anuais só aparecem sob demanda (por exemplo, num detalhamento), com aviso. |

As flags são independentes: uma linha pode ter mais de uma.

### 3.2 Outras regras

- **Categoria Negra:** sempre ao lado das categorias desagregadas, nunca no lugar delas. Nunca somar a linha `Negra` com `Preta` ou `Parda` (usar `raca_agregada` para filtrar).
- **Participação × composição:** `participacao_feminina_no_grupo_racial` ("entre as pessoas pretas, quantas são mulheres") e `composicao_racial_das_mulheres` ("entre as mulheres, quantas são pretas") respondem perguntas diferentes. Usar os nomes do dicionário e nunca os apresentar como a mesma medida.
- **Bases temporais:** não colocar no mesmo eixo ou série valores de `coorte_titulacao` e de `situacao_na_extracao`.
- **Percentual vazio:** exibir "sem dados", nunca zero.
- **2026 não existe na saída**, e não deve ser apresentado como "ano em andamento" a partir de outra fonte.

### 3.3 Textos obrigatórios junto de cada indicador

Todos os textos vêm de `indicadores_dicionario.csv`; o front não deve reescrevê-los.

1. **Nome do indicador** (`nome` da linha `tipo = indicador`).
2. **Base temporal** (`nome` da linha `tipo = base`). Para `situacao_na_extracao`, o rótulo "Situação em out/2026 das pessoas tituladas de 2020 a 2025" é obrigatório, e a descrição deixa claro que é um perfil de início de carreira.
3. **Ressalvas não vazias** do indicador e do recorte (`ressalva`). Exemplos: a de STEM atuação (pessoas sem grande área de atuação ficam fora) e a de Computação por região (só pessoas com vínculo de atuação registrado).
4. **Fonte e extração:** "CNPq, Painel de Formação e Atuação do Lattes, extração de {extracao}", com a data no formato do site.
5. **Definição de STEM**, quando o recorte for STEM: descrição do recorte no dicionário.

---

## 4. Atualização

O painel do CNPq é atualizado com uma extração nova prevista **todo mês** e só serve a extração mais recente. Cada versão do observatório deve fixar uma extração.

### 4.1 Como gerar uma nova extração

1. `python scripts/baixar_lattes.py --anos 2020-2026 --force`: os brutos vão para uma pasta nova, `data/raw/{nova_data}/`, com o manifest.
2. Guardar a pasta da extração (brutos e `manifest.json`) **fora do repositório**: sem ela, a versão não pode ser reproduzida depois.
3. Mudar `EXTRACAO` em `src/lattes/config.py` para a nova data.
4. `python scripts/consolidar_lattes.py` e `python scripts/gerar_indicadores.py`.

### 4.2 O que muda e o que precisa ser conferido de novo

| Item | O que fazer |
| --- | --- |
| **Números** (todas as contagens e percentuais) | Mudam a cada extração. As ressalvas do dicionário são recalculadas automaticamente. |
| **Referência** (`tests/referencias/{nova_data}.json`) | Criar a partir do manifest novo (linhas e pessoas por ano) e dos domínios do consolidado, conferir contra o painel e preencher `conferido_por` e `conferido_em`. Sem ela, os testes de dados falham. |
| **Domínios** | `pytest -m dados` falha se aparecer ou sumir uma categoria em sexo, raça, grandes áreas, nível, setor ou regiões. Além disso, a consolidação para se aparecer um nível de formação novo, e a geração de indicadores para se aparecer sexo, raça, nível ou ano fora do domínio conhecido. Uma categoria nova precisa de decisão antes de entrar nos indicadores. |
| **Números da metodologia** | O teste `test_documentacao.py` (dados) lista os números citados que deixaram de bater. Atualizar `docs/metodologia_lattes.md` e `docs/numeros_metodologia_v1.md`, ou publicar a metodologia como da extração anterior. |
| **Decisões** | Reavaliar as que dependem de volume (amostras pequenas, PQ). Setor e enquadramento só voltam se, no `qualidade_v1.csv`, a taxa de "Não informado" ficar abaixo de 20% e a diferença entre os sexos for de até 3 pontos percentuais. Para 2026, comparar o crescimento da coorte de 2025 com o da extração anterior (registro de decisões, itens 14 e 15). |

Depois de tudo: `pytest`, `pytest -m dados` e `pytest -m rede`.

### 4.3 Versionamento pela coluna `extracao`

- Cada arquivo `indicadores_v1.csv` vem de uma única extração, registrada em cada linha (`extracao`) e no meta.
- Para manter histórico, guardar as extrações lado a lado, com a chave `indicador, base, periodo, recorte, categoria, sexo, raca, extracao`.
- O front deve exibir uma única extração por vez, por padrão a mais recente aprovada, e nunca misturar linhas de extrações diferentes no mesmo gráfico.
- O nome `indicadores_v1` indica a versão da estrutura (colunas e regras), não a extração. Uma mudança de colunas ou de regras gera `indicadores_v2`.

---

## 5. Pontos em aberto para a integração

Perguntas para a equipe do observatório. Este projeto não tem informação sobre elas, e nada aqui assume uma resposta.

1. **Consumo dos dados:** qual é o stack do front, e em que formato ele lê os dados (CSV, JSON, API, banco)? É preciso converter `indicadores_v1.csv`?
2. **Armazenamento:** existe banco de dados no observatório? Onde ficam as versões por extração e quem guarda os brutos com o manifest?
3. **Convenção de nomes:** qual é a convenção de nomes de colunas, códigos e categorias das outras três fontes (Censo Escolar, Censo da Educação Superior, PNADC)? Os códigos desta base (`participacao_feminina`, `stem_formacao` etc.) precisam ser renomeados?
4. **Definição de STEM entre as bases:** aqui, STEM é por Grande Área do CNPq (Ciências Exatas e da Terra ou Engenharias). Que classificação de área (de curso, de ocupação ou outra) as outras fontes usam, e como alinhar as definições para que os números sejam comparáveis entre bases?
5. **Categorias de raça entre as bases:** as outras fontes usam as mesmas cinco categorias, a mesma agregação Negra (Preta + Parda) e o mesmo tratamento para quem não declarou (fora do denominador, com taxa própria)?
6. **Sexo:** como as outras fontes tratam valores ausentes ou não declarados de sexo?
7. **Unidade e período:** esta base conta pessoas por ano da última titulação (coorte), e a situação de atuação é a da data da extração. Como apresentar isso ao lado de fontes com outro tipo de período de referência, sem sugerir comparação direta entre anos?
8. **Amostras pequenas:** o observatório terá uma regra comum entre as fontes? Os limites desta base (denominador menor que 30, numerador menor que 10) são compatíveis?
9. **Atualização:** com que frequência o observatório quer atualizar a base Lattes, e quem fica responsável por gerar e conferir cada nova extração?
10. **Citação:** qual é o formato padrão de citação da fonte no site?
