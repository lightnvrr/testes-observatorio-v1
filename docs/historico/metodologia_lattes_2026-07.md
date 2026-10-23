# Lattes

# Período 03 - Estrutura Metodológica da Base de Dados Lattes

**Período:** 03 (Dias 31 a 45)

**Data:** Julho/2026

---

## 1. Caracterização da Base de Dados

| Campo | Descrição |
| --- | --- |
| **Nome da base** | Plataforma Lattes — Extrato de Currículos de Pesquisadores (recorte de Pós-Graduação) |
| **Instituição responsável** | CNPq — Conselho Nacional de Desenvolvimento Científico e Tecnológico |
| **Objetivo** | Registrar e organizar a produção científica, tecnológica e de inovação de pesquisadores brasileiros. A base Lattes é o padrão nacional de currículo acadêmico e é utilizada em processos de avaliação e fomento à pesquisa (bolsas, projetos, etc.). |
| **Origem dos dados** | Painel de Formação e Atuação Lattes, disponibilizado pelo CNPq em formato de Business Intelligence (BI) interativo. Os dados são exportados a partir do painel em [http://bi.cnpq.br/painel/formacao-atuacao-lattes/](http://bi.cnpq.br/painel/formacao-atuacao-lattes/) e cobrem pesquisadores com vínculo à pós-graduação (Mestrado, Doutorado, Mestrado Profissional). |
| **Periodicidade de atualização** | Anual (extrato disponibilizado uma vez por ano com dados do ciclo vigente). A data exata de extração consta na variável `Data Extração BD Lattes`. |
| **Formato dos arquivos** | CSV, codificação UTF-16, separador de campo: tabulação (`\t`). Um arquivo por ano. Após consolidação pelo pipeline do projeto, o arquivo resultante é UTF-8 com separador vírgula. |
| **Cobertura temporal disponível** | 2020 a 2026 (7 anos). O arquivo de 2026 é tratado como potencialmente parcial — ver seção de Limitações. |
| **Volume de dados (bruto)** | ~312 MB total; entre 16 MB e 57 MB por arquivo anual. Registros: **438.344** no total (incluindo 2026): 2020=58.584 · 2021=66.559 · 2022=71.596 · 2023=79.937 · 2024=76.655 · 2025=62.589 · 2026=22.424. |
| **Volume de dados (consolidado)** | **415.920** registros (2020–2025; 2026 excluído explicitamente pela lista `ANOS` no script `consolidar_lattes.py`). 16 colunas selecionadas para análise. Nenhum registro é removido durante a consolidação — a diferença é inteiramente a exclusão intencional do extrato de 2026. |
| **Link para acesso à fonte** | [http://bi.cnpq.br/painel/formacao-atuacao-lattes/](http://bi.cnpq.br/painel/formacao-atuacao-lattes/) (Painel BI — fonte efetivamente utilizada para exportar os arquivos brutos).  |

### Limitações conhecidas

| # | Limitação | Impacto |
| --- | --- | --- |
| 1 | **Arquivo 2026 possivelmente incompleto** — tamanho de 16 MB contra 45–57 MB dos anos anteriores, com apenas 22.424 registros vs. média de ~72.000 nos anos completos. Provavelmente extrato parcial (meio de ano ou janela de extração menor). | Não deve ser usado em comparações de volume absoluto com anos anteriores. Pode ser incluído com ressalva explícita. |
| 2 | **Unidade de análise é o registro (vínculo), não a pesquisadora** — uma mesma pesquisadora pode aparecer em múltiplos anos e/ou ter múltiplos vínculos no mesmo ano, gerando dupla contagem. | Percentuais de participação são sobre registros, não sobre indivíduos únicos. |
| 3 | **Subdeclaração de gênero e raça** — parcela dos registros contém `Sexo = "Não declarado"` e `Cor ou Raça = "Não desejo declarar"`. | Exclui automaticamente parte da população da análise; pode enviesar grupos específicos. |
| 4 | **`Grande Área` e `Área` são autodeclaradas de forma semi-independente** — a taxonomia de áreas é controlada (verificado: nenhuma variação de grafia relevante nos 99 valores distintos de `Área (Formação)`), mas grande área e área específica não aninham 100% (~2% dos registros STEM têm área específica incompatível, ex.: `Grande Área = Engenharias` / `Área = Educação`). | Baixo impacto; recomenda-se ancorar recortes disciplinares em `Grande Área`. |
| 5 | **Recorte limitado à pós-graduação** — a base não cobre pesquisadores de graduação ou técnicos sem vínculo formal de pós-graduação. | O perfil da base é enviesado para pesquisadores com formação avançada; não representa a totalidade do mercado de trabalho em ciência e tecnologia. |
| 6 | **Bolsas registradas como snapshot** — as variáveis de bolsa (`Bolsista - PQ`, `Bolsista - DT`, etc.) refletem o status no momento da extração, não o histórico acumulado de bolsas. | Não permite análise de trajetória de bolsas ao longo do tempo para um mesmo pesquisador. |
| 7 | **Ausência de identificador único** — não há ID de pesquisador na base exportada; a deduplicação ou rastreamento longitudinal não é possível com as colunas disponíveis. | Impossibilita análises de painel individual (entrada, saída, progressão de carreira). |
| 8 | **Assimetria de completude entre Formação e Atuação** — `Grande Área (Atuação)` tem 17,4% de "Não informado" (~72 mil registros) contra 5,6% em Formação. | Subconta recortes disciplinares de atuação e prejudica comparações formação × atuação; restringir tais comparações a registros com ambas as grandes áreas preenchidas. |
| 9 | **A definição de recorte STEM afeta o indicador de gênero** — trocar uma lista fixa de áreas por grande área eleva a participação feminina medida de 26,9% para 34,7% (formação), pois listas restritas concentram as subáreas mais masculinizadas. | Reportar sempre a definição adotada e, de preferência, o indicador desagregado por grande área/área. |

---

## 2. Dicionário das Variáveis Relevantes

> As variáveis marcadas com **[Consolidado]** são as 16 retidas na consolidação do pipeline atual. As demais pertencem aos arquivos brutos e podem ser reincorporadas conforme necessidade.
> 

### 2.1 Identificação e Dados Pessoais

| Variável | Descrição | Tipo | Valores possíveis / Observações |
| --- | --- | --- | --- |
| `Ano` | Ano de referência do extrato | int | 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| `Sexo` **[Consolidado]** | Gênero autodeclarado da pesquisadora | enum | `Feminino`, `Masculino`, `Não declarado` |
| `Cor ou Raça` **[Consolidado]** | Raça/cor autodeclarada | enum | `Branca`, `Preta`, `Parda`, `Amarela`, `Indígena`, `Não desejo declarar` |
| `Data Extração BD Lattes` | Data em que os dados foram extraídos da Plataforma Lattes | string/date | Ex: `2024-03-15`. Útil para verificar a janela de coleta do extrato anual. |
| `País de Nascimento` | País de nascimento da pesquisadora | string | Ex: `Brasil`, `Estados Unidos`. Maioria dos registros: Brasil. |

### 2.2 Formação Acadêmica

| Variável | Descrição | Tipo | Valores possíveis / Observações |
| --- | --- | --- | --- |
| `País (Formação)` | País onde ocorreu a formação acadêmica | string | Ex: `Brasil`, `Estados Unidos`, `França` |
| `Região (Formação)` **[Consolidado]** | Região brasileira da instituição de formação | enum | `Norte`, `Nordeste`, `Centro-Oeste`, `Sudeste`, `Sul`. Vazio para formação no exterior. |
| `UF (Formação)` **[Consolidado]** | Unidade Federativa (estado) da instituição de formação | string | Siglas estaduais brasileiras (SP, RJ, MG, etc.) |
| `Cidade (Formação)` | Município da instituição de formação | string | Alta cardinalidade (centenas de municípios); não utilizada nos indicadores atuais, que agregam por Região/UF. |
| `Grande Área (Formação)` **[Consolidado]** | Grande área do conhecimento do CNPq referente à formação | enum | `Ciências Exatas e da Terra`, `Ciências Biológicas`, `Engenharias`, `Ciências da Saúde`, `Ciências Agrárias`, `Ciências Sociais Aplicadas`, `Ciências Humanas`, `Lingüística, Letras e Artes`, `Outra`, `Tecnologias`, `Não informado`. Obs.: "Tecnologias" tem volume desprezível (3 registros em Formação). |
| `Área (Formação)` **[Consolidado]** | Área específica dentro da grande área de formação | string | 99 valores distintos. Ex.: `Ciência da Computação`, `Matemática`, `Física`, `Química`, `Engenharia Elétrica`, `Probabilidade e Estatística`. Obs.: os nomes seguem exatamente a tabela de áreas do CNPq — usar `Probabilidade e Estatística` (não "Estatística"); subespecialidades de computação (Ciência de Dados, IA, Sistemas de Informação) **não existem** como área separada nessa base. |
| `Instituição (Formação)` | Nome da instituição de ensino onde ocorreu a formação | string | Ex: `Universidade de São Paulo`, `UNICAMP` |
| `Nível (Formação)` **[Consolidado]** | Nível de pós-graduação do vínculo registrado | enum | `Mestrado`, `Doutorado`, `Mestrado Profissional` |

### 2.3 Atuação Profissional

| Variável | Descrição | Tipo | Valores possíveis / Observações |
| --- | --- | --- | --- |
| `País (Atuação)` | País onde a pesquisadora atua profissionalmente | string | Ex: `Brasil` |
| `Região (Atuação)` **[Consolidado]** | Região brasileira da instituição de atuação | enum | `Norte`, `Nordeste`, `Centro-Oeste`, `Sudeste`, `Sul` |
| `UF (Atuação)` **[Consolidado]** | Unidade Federativa da instituição de atuação | string | Siglas estaduais |
| `Cidade (Atuação)` | Município da instituição de atuação | string | Alta cardinalidade; não utilizada nos indicadores atuais, que agregam por Região/UF. |
| `Grande Área (Atuação)` **[Consolidado]** | Grande área do conhecimento da atividade profissional atual | enum | Mesmos valores de `Grande Área (Formação)`. **Atenção:** 17,4% dos registros = `Não informado` (~72 mil) — ver Limitação 8. |
| `Área (Atuação)` **[Consolidado]** | Área específica da atividade profissional | string | Ex: `Ciência da Computação`, `Engenharia Elétrica` |
| `Instituição (Atuação)` | Instituição onde a pesquisadora atua | string | Nome da instituição empregadora, sem padronização de grafia (a mesma instituição pode aparecer com nomes distintos); não utilizada nos indicadores atuais. |
| `Setor de Atividade (Atuação)` **[Consolidado]** | Setor de atuação profissional | enum | `Ensino Superior`, `Setor Empresarial`, `Setor Governamental`, `Setor Exterior` |
| `Enquadramento (Atuação)` **[Consolidado]** | Enquadramento ou cargo na atividade | enum | `Professor`, `Professor Assistente`, `Pesquisador`, `Assistente de Pesquisa`, `Engenheiro`, `Pós-doutorando`, `Outro` |

### 2.4 Bolsas e Fomentos

> Todas as variáveis de bolsa são do tipo **booleano/string**: indicam se a pesquisadora possui aquele tipo de bolsa ativa no momento da extração. Valores: `Sim` / (vazio ou ausente = Não).
> 

| Variável | Descrição | Tipo | Observações |
| --- | --- | --- | --- |
| `Bolsista - Iniciação Científica` | Bolsa de iniciação científica (IC) | bool/string | Voltada para graduação; presença nesta base indica vínculo com pós-graduação concomitante. |
| `Bolsista - Graduação Sanduiche` | Bolsa de graduação sanduíche (intercâmbio) | bool/string | Voltada para intercâmbio de graduação; presença nesta base indica vínculo de pós-graduação concomitante, assim como a IC. |
| `Bolsista - Mestrado` | Bolsa de mestrado CNPq | bool/string | Fomento individual concedido durante o próprio mestrado; não indica nível de excelência, apenas vínculo de financiamento. |
| `Bolsista - Doutorado` | Bolsa de doutorado CNPq | bool/string | Fomento individual concedido durante o próprio doutorado; análogo à bolsa de mestrado. |
| `Bolsista - Pós-doutorado` | Bolsa de pós-doutorado CNPq | bool/string | Concedida após a conclusão do doutorado, antes da consolidação em bolsas PQ/DT. |
| `Bolsista - PQ` **[Consolidado]** | Bolsa de Produtividade em Pesquisa (PQ) CNPq | bool/string | Principal indicador de consolidação da carreira de pesquisa. Agrupa todos os níveis de PQ. |
| `Bolsista - PQ 1A` | Nível mais alto da bolsa PQ | bool/string | Hierarquia: 1A > 1B > 1C > 1D > 2/1E |
| `Bolsista - PQ 1B` | Nível PQ 1B | bool/string | Segundo nível mais alto da hierarquia PQ, abaixo de 1A. |
| `Bolsista - PQ 1C` | Nível PQ 1C | bool/string | Nível intermediário da hierarquia PQ, entre 1B e 1D. |
| `Bolsista - PQ 1D` | Nível PQ 1D | bool/string | Nível mais baixo da faixa PQ 1, acima apenas do PQ 2/1E. |
| `Bolsista - PQ 2 ou 1E` | Nível de entrada da bolsa PQ | bool/string | Nível mais acessível entre os PQ. |
| `Bolsista - DT` **[Consolidado]** | Bolsa de Desenvolvimento Tecnológico e Extensão Inovadora (DT) CNPq | bool/string | Foco em inovação e transferência tecnológica; menos comum que PQ. |
| `Bolsista - DT 1A` | Nível mais alto da bolsa DT | bool/string | Hierarquia: 1A > 1B > 1C > 1D > 2/1E, mesma estrutura da bolsa PQ. |
| `Bolsista - DT 1B` | Nível DT 1B | bool/string | Segundo nível mais alto da hierarquia DT, abaixo de 1A. |
| `Bolsista - DT 1C` | Nível DT 1C | bool/string | Nível intermediário da hierarquia DT, entre 1B e 1D. |
| `Bolsista - DT 1D` | Nível DT 1D | bool/string | Nível mais baixo da faixa DT 1, acima apenas do DT 2/1E. |
| `Bolsista - DT 2 ou 1E` | Nível de entrada da bolsa DT | bool/string | Nível mais acessível entre os DT, análogo ao PQ 2/1E. |

---

## 3. Matriz de Indicadores

### 3.1 Indicadores já implementados no pipeline atual

| Indicador | Explicação | Fórmula | Variáveis utilizadas | Agregação | Limitação |
| --- | --- | --- | --- | --- | --- |
| **Participação feminina geral** | Proporção de registros femininos sobre o total de registros com gênero declarado, por ano. Indica a presença global de mulheres na base. | `(# Sexo = "Feminino") / (# Sexo ≠ "Não declarado") × 100` | `Sexo`, `Ano` | Por ano | Conta registros, não indivíduos. Exclui "Não declarado". |
| **Participação feminina por grande área de formação** | Proporção de mulheres em cada uma das grandes áreas do conhecimento CNPq (Engenharias, Ciências Exatas, etc.). Revela disparidades por campo disciplinar. | `(# Sexo = "Feminino" e Grande Área = X) / (# Grande Área = X e Sexo declarado) × 100` | `Sexo`, `Grande Área (Formação)`, `Ano` | Por grande área e ano | Não captura heterogeneidade interna das grandes áreas. |
| **Participação feminina em STEM** | Proporção de mulheres em registros cuja **Grande Área** seja `"Ciências Exatas e da Terra"` ou `"Engenharias"`. Strings verificadas contra os valores distintos reais da base. Inclui: Ciência da Computação, Química, Matemática, Física, Geociências, Probabilidade e Estatística, Oceanografia, Astronomia (Ciências Exatas) e todas as Engenharias cadastradas (Elétrica, Civil, Mecânica, Materiais, Química, Produção, Sanitária, Biomédica, Nuclear, Aeroespacial, Transportes, Energia, Naval, Minas). **Subespecialidades de Computação** (Ciência de Dados, IA, Engenharia de Software, Redes de Computadores, Sistemas de Informação) não existem como categoria separada — ficam em "Ciência da Computação". **Robótica, Mecatrônica e Automação** e **Microeletrônica** ficam fora porque o CNPq as classifica em "Outra" grande área, não em "Engenharias". | `(# Sexo = "Feminino" e Grande Área ∈ {"Ciências Exatas e da Terra","Engenharias"}) / (# Grande Área ∈ {...} e Sexo declarado) × 100` | `Sexo`, `Grande Área (Formação)`, `Grande Área (Atuação)`, `Ano` | Por área específica e ano (detalhado); por Grande Área e ano (agregado) | Grande Área (Atuação) tem 17,4% de registros "Não informado" — esse subconjunto não entra no STEM de Atuação mesmo que a área específica seja STEM. |
| **Participação feminina por nível de formação** | Proporção de mulheres em cada nível de pós-graduação (Mestrado, Doutorado, Mestrado Profissional). Indica em qual estágio da carreira acadêmica a disparidade é mais acentuada. | `(# Sexo = "Feminino" e Nível = X) / (# Nível = X e Sexo declarado) × 100` | `Sexo`, `Nível (Formação)`, `Ano` | Por nível e ano | Cobre apenas pós-graduação; não rastreia transição de nível para um mesmo indivíduo. |
| **Proporção de bolsistas PQ por gênero** | Proporção de mulheres entre os detentores de bolsa de Produtividade em Pesquisa (PQ) CNPq por ano. Indica acesso feminino ao nível mais alto de fomento individual à pesquisa. | `(# Sexo = "Feminino" e Bolsista-PQ = "Sim") / (# Bolsista-PQ = "Sim" e Sexo declarado) × 100` | `Sexo`, `Bolsista - PQ`, `Ano` | Por ano | Reflete snapshot do momento de extração; não histórico acumulado. |
| **Participação feminina na atuação em Computação** | Proporção de mulheres entre profissionais com atuação em Ciência da Computação por ano. Compara formação vs. atuação profissional efetiva na área. | `(# Sexo = "Feminino" e Área (Atuação) = "Ciência da Computação") / (# Área (Atuação) = "Ciência da Computação" e Sexo declarado) × 100` | `Sexo`, `Área (Atuação)`, `Ano` | Por ano | Sensível à grafia exata do nome da área. |
| **Distribuição regional de profissionais de Computação por gênero** | Proporção de mulheres em Computação por região do Brasil. Revela desigualdades geográficas sobrepostas à desigualdade de gênero. | `(# Sexo = "Feminino" e Área(Atuação) = "Ciência da Computação" e Região = R) / (# Área(Atuação) = "Ciência da Computação" e Região = R e Sexo declarado) × 100` | `Sexo`, `Área (Atuação)`, `Região (Atuação)`, `Ano` | Por região e ano | Agrupamento por região oculta variações entre estados da mesma região. |

### 3.2 Indicadores sugeridos (a implementar)

| Indicador | Explicação | Fórmula | Variáveis utilizadas | Agregação | Limitação |
| --- | --- | --- | --- | --- | --- |
| **Razão de gênero (M:F) em bolsas PQ por nível** | Detalha a desigualdade dentro dos níveis hierárquicos da bolsa PQ (1A, 1B, 1C, 1D, 2/1E). Pode revelar que a sub-representação é ainda mais severa nos níveis superiores. | `# Bolsista-PQ-Nível = X e Sexo = "Masculino" / # Bolsista-PQ-Nível = X e Sexo = "Feminino"` | `Sexo`, `Bolsista - PQ 1A/1B/1C/1D/2 ou 1E`, `Ano` | Por nível PQ e ano | Cada nível é variável separada; requer unpivot dos dados. |
| **Participação feminina em bolsas DT por nível** | Análogo ao PQ, mas para bolsas de Desenvolvimento Tecnológico. Avalia presença feminina em inovação aplicada vs. pesquisa acadêmica pura. | `(# Sexo = "Feminino" e Bolsista-DT-Nível = X) / (# Bolsista-DT-Nível = X) × 100` | `Sexo`, `Bolsista - DT 1A/1B/1C/1D/2 ou 1E`, `Ano` | Por nível DT e ano | Volumes pequenos por nível podem tornar percentuais instáveis. |
| **Interseccionalidade gênero × raça em STEM** | Proporção de mulheres de cada grupo racial/cor em áreas STEM. Revela desigualdades compostas — a sub-representação é diferente para mulheres negras, brancas, indígenas, etc. | `(# Sexo = "Feminino" e Cor = C e Área ∈ STEM) / (# Área ∈ STEM e Sexo = "Feminino") × 100` | `Sexo`, `Cor ou Raça`, `Área (Formação)`, `Ano` | Por grupo racial, área e ano | Alta taxa de "Não desejo declarar" pode subestimar grupos minorizados. |
| **Participação feminina por UF (nível estado)** | Granularidade estadual para a distribuição geográfica, permitindo identificar estados com desempenho destacado ou deficiente além da análise por região. | `(# Sexo = "Feminino" e UF = U) / (# UF = U e Sexo declarado) × 100` | `Sexo`, `UF (Atuação)`, `Ano` | Por UF e ano | UFs com poucos registros produzem percentuais instáveis (denominador pequeno). |
| **Participação feminina por setor de atividade** | Proporção de mulheres em cada setor (Ensino Superior, Setor Empresarial, Setor Governamental, Exterior). Indica se a sub-representação difere entre academia e mercado. | `(# Sexo = "Feminino" e Setor = S) / (# Setor = S e Sexo declarado) × 100` | `Sexo`, `Setor de Atividade (Atuação)`, `Ano` | Por setor e ano | Não distingue porte ou natureza dentro de cada setor (ex.: empresas grandes vs. pequenas). |
| **Participação feminina por enquadramento (cargo)** | Proporção de mulheres em cada tipo de enquadramento (Professor, Pesquisador, Pós-doutorando, etc.). Permite verificar se há concentração feminina em posições de menor prestígio ou estabilidade. | `(# Sexo = "Feminino" e Enquadramento = E) / (# Enquadramento = E e Sexo declarado) × 100` | `Sexo`, `Enquadramento (Atuação)`, `Ano` | Por enquadramento e ano | Nomenclatura de cargos pode variar entre instituições sob o mesmo enquadramento CNPq. |
| **Taxa de crescimento anual de pesquisadoras** | Variação percentual no número absoluto de registros femininos ano a ano. Indica aceleração ou desaceleração do ingresso de mulheres na pós-graduação. | `(# Feminino Ano t - # Feminino Ano t-1) / # Feminino Ano t-1 × 100` | `Sexo`, `Ano` | Por ano (série temporal) | Afetado pela variação no volume total da base a cada extrato anual. |
| **Participação feminina em formação vs. atuação (gap)** | Diferença entre a proporção de mulheres formadas em uma área e a proporção que atua nessa mesma área profissionalmente. Mede retenção ou evasão feminina do campo. | `% Feminino (Formação, Área X) − % Feminino (Atuação, Área X)` | `Sexo`, `Área (Formação)`, `Área (Atuação)`, `Ano` | Por área e ano | Requer que `Área (Formação)` e `Área (Atuação)` usem nomenclatura compatível. |
| **Concentração regional de formação vs. atuação** | Compara onde as pesquisadoras se formaram vs. onde atuam, por região. Indica fluxos migratórios da força de trabalho científica feminina. | Diferença de distribuição regional entre `Região (Formação)` e `Região (Atuação)` para Sexo = "Feminino" | `Sexo`, `Região (Formação)`, `Região (Atuação)`, `Ano` | Por par de regiões e ano | Registro único não informa se a pesquisadora migrou; pode ser formação anterior à atuação. |

---

## 4. Nota sobre o Arquivo de 2026

O extrato de 2026 possui **22.424 registros e 16 MB**, enquanto anos completos anteriores têm entre 58.584 e 79.937 registros e 42–57 MB. A proporção é de aproximadamente 1:3, sugerindo que o arquivo representa apenas parte do ano (extrato parcial).

No pipeline atual, 2026 é **excluído da consolidação** (lista `ANOS` em `consolidar_lattes.py`), por isso o consolidado tem 415.920 registros (2020–2025).

**Recomendação** caso 2026 volte a ser incorporado:

- Excluir 2026 de qualquer comparação de **volume absoluto** entre anos.
- Utilizar 2026 apenas para indicadores de **proporção/percentual**.
- Acrescentar nota metodológica explícita sempre que 2026 aparecer em gráficos ou tabelas.
- Verificar a data de extração contida na variável `Data Extração BD Lattes` para confirmar a janela de coleta.

---

## 5. Link para Acesso à Fonte de Dados

| Recurso | URL |
| --- | --- |
| **Painel Formação e Atuação Lattes — fonte efetivamente utilizada** | [http://bi.cnpq.br/painel/formacao-atuacao-lattes/](http://bi.cnpq.br/painel/formacao-atuacao-lattes/) |

## 6. Limitações

- A definição de STEM afeta diretamente o indicador de gênero: adotar "Grande Área ∈ {Ciências Exatas e da Terra, Engenharias}" eleva a participação feminina medida de 26,9% para 34,7% (formação), pois a lista anterior concentrava
as subáreas mais masculinizadas. Reportar o indicador desagregado por grande área/área, além do agregado.
- Assimetria de completude: Grande Área (Atuação) tem 17,4% de "Não informado" (72 mil reg.) vs. 5,6% em Formação. Comparações formação × atuação devem restringir-se a registros com ambas preenchidas, ou trazer ressalva.
- Grande Área e Área são autodeclaradas de forma semi-independente e não aninham perfeitamente (~2% dos registros STEM com área incompatível ou não informada).
- Áreas STEM emergentes (Robótica/Mecatrônica, Microeletrônica) são classificadas em "Outra" pelo CNPq e ficam fora; a grande área "Tecnologias" existe mas é desprezível (3 reg.).