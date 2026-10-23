# Lattes

# Estrutura Metodológica da Base de Dados Lattes (V1)

**Versão:** V1 (final)

**Data:** Outubro/2026

**Aprovação:** decisões metodológicas aprovadas pela coordenação do projeto em 23/10/2026

**Extração de referência:** 4 de outubro de 2026

**Versão anterior:** [historico/metodologia_lattes_2026-07.md](historico/metodologia_lattes_2026-07.md)

Fontes citadas ao longo do texto:

- **[NT]**: CNPq, *Painel de Formação e Atuação do Lattes, Nota Técnica 01/2024* ([nota_tecnica_painel_lattes.pdf](nota_tecnica_painel_lattes.pdf)).
- **[WB]**: workbook `PainelLattes-FormaoeAtuao` publicado pelo CNPq no Tableau Public (fórmulas do arquivo .twb e extratos .hyper).
- **[Saídas]**: arquivos gerados pelo pipeline deste projeto a partir da extração de referência (`manifest.json`, `lattes_consolidado.meta.json`, `indicadores_v1.csv`, `qualidade_v1.csv`, `indicadores_v1.meta.json`).

Todos os números deste documento vêm das [Saídas] da extração de 4 de outubro de 2026, salvo quando a fonte indicada é a [NT].

---

## O que mudou em relação à versão de julho/2026

| # | Mudança | Motivo |
| --- | --- | --- |
| 1 | **Nova base: extração de 4/10/2026**, baixada de novo pelo pipeline. Os números da versão anterior (contagens e percentuais) não são reproduzíveis e foram substituídos. | Os arquivos brutos antigos não existem mais, e o painel só oferece a extração vigente. A extração atual é a única que qualquer pessoa consegue baixar de novo na fonte. |
| 2 | **`Ano` passa a ser o ano de obtenção da última titulação**, não o ano de um extrato. Os indicadores "por ano" são por coorte de titulação. | O campo `.Ano` do painel é o campo `ANOOBTENCAOTITULO` [WB], e a [NT] o descreve como "Ano de Formação". Todos os anos vêm de uma única extração. |
| 3 | **A unidade de análise é a pessoa**, contada uma vez pela última titulação. Os indicadores somam a coluna `Totalpessoas`. A limitação de dupla contagem foi retirada. | A [NT] informa que cada pessoa entra uma vez, pela última titulação. Cada linha do arquivo exportado agrega pessoas com os mesmos atributos, por isso a contagem certa é a soma de `Totalpessoas`, não o número de linhas. Não se sabe se os arquivos antigos traziam essa coluna, o que é mais uma razão para não comparar com os números de julho/2026. |
| 4 | **Indicadores de situação atual** (área e região de atuação) são calculados só sobre o agregado de 2020 a 2025 e descritos como "situação em out/2026 das pessoas tituladas de 2020 a 2025". | Atuação e bolsas refletem a data da extração, não o ano da titulação. Por coorte recente, mediriam sobretudo o tempo desde o título. |
| 5 | **Recorte de raça implementado**, com dois indicadores distintos (participação feminina dentro do grupo racial e composição racial das mulheres), taxa de não declaração própria, flags de amostra pequena e categoria Negra (Preta + Parda) ao lado das categorias desagregadas. | Decisão de incluir raça na V1. A fórmula de interseccionalidade da versão anterior foi corrigida: passa a usar Grande Área, e não Área, e exclui "Não desejo declarar" do denominador. |
| 6 | **Bolsa PQ, bolsa DT, setor de atividade e enquadramento ficam fora da V1.** | PQ e DT têm volume muito baixo e as bolsas são histórico de concessões. Setor e enquadramento têm alto preenchimento "Não informado". Ver a seção 4.3. |
| 7 | **Bolsas são tratadas como histórico** ("já recebeu"), não como situação vigente. | As bolsas vêm da Plataforma Integrada Carlos Chagas [NT], e parte relevante dos doutores tem bolsa de iniciação científica registrada (limitação 14). |
| 8 | **2026 continua fora, com outro motivo**: coorte de titulação incompleta, com atraso de atualização não aleatório. | O motivo antigo ("extrato parcial") deixou de valer com o item 2. |
| 9 | **O consolidado passa a ter 18 colunas** (16 de análise + `Totalpessoas` + `Data Extração BD Lattes`), e o dicionário foi corrigido contra os valores reais. | Os indicadores precisam do peso de cada linha, e a data de extração garante a proveniência. Vários domínios documentados não batiam com a base (UF, setor, bolsas, sexo). |
| 10 | **O download é automatizado e auditável** (manifest com SHA-256 por arquivo). | Reprodutibilidade (seção 6). |
| 11 | **As limitações foram unificadas numa só seção**, e a [NT] passou a ser citada como fonte. | A versão anterior repetia limitações em duas seções. |

---

## Decisões metodológicas da V1

Aprovadas pela coordenação do projeto em 23/10/2026. Registro completo, com o motivo de cada uma, em [registro_decisoes_v1.md](registro_decisoes_v1.md).

1. **Extração:** a base da V1 é a extração de 4/10/2026; a versão de julho/2026 fica só como histórico.
2. **Unidade:** os indicadores contam pessoas (soma de `Totalpessoas`), com o número de linhas junto para auditoria.
3. **Período:** a série vai de 2020 a 2025; coortes anteriores ficam para a V2 (seção 4.4).
4. **2026:** fica fora da V1, inclusive dos percentuais, por ser uma coorte de titulação incompleta.
5. **Categoria Negra:** Preta + Parda é publicada ao lado das categorias desagregadas, nunca no lugar delas.
6. **PQ e DT:** ficam fora da V1; na V2, entram sobre todas as coortes, como "já recebeu a bolsa".
7. **Setor e enquadramento:** ficam fora da V1 e aparecem só no relatório de qualidade.
8. **STEM:** Grande Área ∈ {Ciências Exatas e da Terra, Engenharias}; "Tecnologias" fica fora.
9. **Situação atual:** STEM atuação, atuação em Computação e Computação por região são calculados só no agregado 2020 a 2025, como perfil de início de carreira.
10. **Amostras pequenas:** flag para denominador menor que 30 e para numerador menor que 10, e o agregado 2020 a 2025 como número principal para Indígena.

---

## 1. Caracterização da Base de Dados

| Campo | Descrição |
| --- | --- |
| **Nome da base** | Painel de Formação e Atuação do Lattes: pessoas com mestrado, mestrado profissional ou doutorado registrados no Currículo Lattes. |
| **Instituição responsável** | CNPq (Conselho Nacional de Desenvolvimento Científico e Tecnológico). |
| **Origem dos dados** | Base de Currículos da Plataforma Lattes [NT]. As bolsas vêm da Plataforma Integrada Carlos Chagas [NT]. O painel em [http://bi.cnpq.br/painel/formacao-atuacao-lattes/](http://bi.cnpq.br/painel/formacao-atuacao-lattes/) embute um workbook do Tableau Public [WB]. Os arquivos brutos são exportados da aba "Painel - Download" desse workbook. |
| **Universo** | Currículos atualizados nos últimos 60 meses, pela mesma regra da Busca de Currículos do Lattes [NT]. Só entram pessoas com titulação de mestrado ou doutorado preenchida [NT]. |
| **Unidade de análise** | Pessoa, contada uma única vez pela **última titulação** registrada: doutores não entram na contagem de mestres, mesmo que tenham registrado o mestrado [NT]. Registros sem ano de titulação ficam fora do painel [NT]. |
| **Recorte temporal (`Ano`)** | Ano de obtenção da última titulação [NT][WB]. O painel cobre de 1948 ao ano atual, como "estoque por ano" [NT]. A V1 usa as coortes de **2020 a 2025**. |
| **Periodicidade** | A extração prevista é mensal [NT]. Cada nova extração pode alterar os resultados [NT], por isso a V1 fica fixada na extração de **4/10/2026** (`Data Extração BD Lattes`). |
| **Formato dos arquivos brutos** | Um CSV por ano de titulação, guardado exatamente como veio. A exportação por URL vem em UTF-8 com vírgula. O formato da interface ("Tabela de referência cruzada") vem em UTF-16 com tabulação. O pipeline aceita os dois. |
| **Formato do consolidado** | UTF-8, separador vírgula, 18 colunas. Nenhum registro é removido na consolidação. |

### Volume da extração de referência

| Ano de titulação | Pessoas | Linhas do arquivo | Tamanho do bruto |
| --- | --- | --- | --- |
| 2020 | 53.178 | 52.691 | 20,9 MB |
| 2021 | 62.739 | 61.910 | 24,6 MB |
| 2022 | 71.359 | 70.264 | 27,9 MB |
| 2023 | 82.976 | 81.473 | 32,3 MB |
| 2024 | 81.923 | 80.170 | 31,7 MB |
| 2025 | 78.130 | 76.065 | 30,1 MB |
| **Consolidado (2020 a 2025)** | **430.305** | **422.573** | |
| 2026 (fora da V1) | 45.434 | 44.414 | 17,5 MB |

Cada linha do arquivo é uma combinação de atributos, e a coluna `Totalpessoas` diz quantas pessoas têm aquela combinação. O número de linhas depende das colunas exportadas; o número de pessoas não. Todos os indicadores contam pessoas.

### Bases temporais dos indicadores

| Base | O que mede | Períodos |
| --- | --- | --- |
| **Por ano de titulação** (`coorte_titulacao`) | Atributos de formação (sexo, raça, grande área, nível) das pessoas tituladas em cada ano. | Cada ano de 2020 a 2025 e o agregado 2020 a 2025. |
| **Situação na extração** (`situacao_na_extracao`) | Situação em out/2026 (área e região de atuação) das pessoas tituladas de 2020 a 2025: um perfil de início de carreira, não de todas as pesquisadoras. | Só o agregado 2020 a 2025. |

---

## 2. Limitações conhecidas

| # | Limitação | Impacto e tratamento |
| --- | --- | --- |
| 1 | **Universo restrito a currículos atualizados nos últimos 60 meses** [NT]. | Quem não atualiza o currículo há mais de 60 meses some da base. Isso não é aleatório: afeta mais quem saiu da academia ou da pesquisa. A base não representa todas as pessoas tituladas. |
| 2 | **Retrato de uma única extração.** A extração é prevista mensalmente e cada nova extração pode alterar os resultados [NT]. | Os números valem para a extração de 4/10/2026. Para comparar com versões futuras, é preciso fixar a extração (o pipeline guarda os brutos por data de extração). |
| 3 | **Cada pessoa entra uma vez, pela última titulação** [NT]. `Nível (Formação)` é o maior título, e `Ano` é o ano desse título. | Não há dupla contagem. Em compensação, a base não permite estudar trajetórias (mestrado seguido de doutorado). |
| 4 | **Coortes de mestrado encolhem com o tempo.** Quem é mestre numa coorte e depois vira doutor passa para a coorte do doutorado [NT]. | As coortes de mestrado mais antigas ficam só com quem (ainda) não fez doutorado. Se a progressão para o doutorado for diferente entre mulheres e homens (ou entre grupos raciais), a participação feminina no mestrado fica enviesada, e o viés cresce com a idade da coorte. Comparações de mestrado entre anos levam ressalva. |
| 5 | **Atraso de atualização dos currículos.** Títulos recentes demoram a ser registrados, e o atraso varia por área, nível e perfil de quem atualiza o currículo. | A coorte do ano corrente é incompleta e enviesada até nas proporções. Por isso 2026 fica fora da V1 (seção 5). |
| 6 | **Atuação e bolsas refletem a data da extração**, não o ano da titulação. | Indicadores de situação atual só são calculados no agregado 2020 a 2025 e descrevem um perfil de início de carreira. |
| 7 | **Dados autodeclarados** [NT]. Há certificação em alguns módulos (artigos, dados pessoais, formação no país) e um termo de veracidade [NT]. | Sexo, raça e áreas dependem do que a pessoa informou. |
| 8 | **Não declaração de raça.** Em 2020 a 2025, 5,60% das pessoas com sexo declarado escolheram "Não desejo declarar" (5,17% das mulheres e 6,17% dos homens). A taxa cai entre as coortes: 6,67% em 2020 e 4,77% em 2025. | Essas pessoas saem dos denominadores dos indicadores raciais. Se a não declaração variar entre grupos, as composições podem ficar enviesadas. A taxa é publicada como indicador próprio. |
| 9 | **Sexo "Não declarado"**, que não está entre as opções descritas na [NT] (feminino e masculino). São 4.119 pessoas em 2020 a 2025 (0,96%), com crescimento entre as coortes (0,71% em 2020 e 1,17% em 2025). Nesse grupo, "Preta" é a maior categoria de raça (35,81%, contra 8,23% entre quem declarou sexo) e "Não desejo declarar" chega a 22,87% (5,60% entre quem declarou sexo). | O padrão sugere problema de preenchimento ou de codificação. Essas pessoas saem de todos os indicadores, que exigem sexo declarado, e ficam registradas no relatório de qualidade. Pergunta em aberto ao CNPq (seção 7). |
| 10 | **Assimetria de completude entre formação e atuação.** "Não informado" atinge 17,50% em Grande Área (Atuação) e 5,55% em Grande Área (Formação). Em Região (Atuação), chega a 26,45%. A instituição de atuação é a do vínculo vigente (início preenchido e fim em branco); com mais de um vínculo, vale a de dedicação exclusiva ou integral, depois a de maior carga horária, a de vínculo formal e a de início mais recente [NT]. "Não informado" pode indicar desemprego ou currículo desatualizado [NT]. | Recortes de atuação cobrem só quem tem atuação informada. A ausência é um pouco maior entre mulheres em Grande Área (Atuação): 18,31%, contra 16,44% dos homens (entre formados em STEM, 20,98% contra 18,33%). Em Computação, a região de atuação falta para 23,08% das mulheres e 24,06% dos homens. Ressalvas no dicionário de indicadores. |
| 11 | **Setor e enquadramento com preenchimento muito baixo.** "Não informado" atinge 47,07% em Setor de Atividade e 23,11% em Enquadramento. O enquadramento é um campo aberto, agrupado pelo CNPq a partir dos termos digitados [NT]. | Os dois ficam fora da V1 (seção 4.3). |
| 12 | **Classificação de áreas.** Grande área e área são classificadas pela Árvore do Conhecimento do CNPq. Quando o dado diverge da Árvore, a grande área vira "Outra"; quando falta, "Não informado" [NT]. "Outra" reúne 8,23% das pessoas em Grande Área (Formação) e 1,16% em Grande Área (Atuação). "Tecnologias" não existe na Árvore e abarca sobretudo especialidades próximas das Engenharias [NT]: são 2 pessoas na formação e 40 na atuação. Em Grande Área (Atuação) aparece ainda "Serviço Social" (1 pessoa), que na Árvore é uma área, não uma grande área. | "Tecnologias" e "Outra" ficam fora do STEM. Áreas emergentes classificadas em "Outra" (como robótica e microeletrônica) não entram no STEM. |
| 13 | **A definição de STEM afeta o indicador de gênero.** | Listas restritas de áreas concentram as subáreas mais masculinizadas e reduzem a participação feminina medida. A V1 usa Grande Área (Ciências Exatas e da Terra ou Engenharias) e informa sempre a definição. |
| 14 | **Bolsas são histórico de concessões, não situação vigente.** Os dados vêm da Plataforma Integrada Carlos Chagas, não da autodeclaração [NT]. Evidência: 19,88% dos doutores titulados de 2020 a 2025 têm bolsa de iniciação científica (bolsa de graduação) registrada, 11,53% têm bolsa de mestrado e 10,20%, bolsa de doutorado. | "Sim" significa "já recebeu a bolsa do CNPq até a data da extração". Isso favorece coortes antigas nas bolsas de fim de carreira (PQ, DT). |
| 15 | **Recorte limitado à pós-graduação.** Só entram pessoas com mestrado ou doutorado [NT]. | A base não representa toda a força de trabalho em ciência e tecnologia. |
| 16 | **Ausência de identificador individual** na exportação. | Não há como acompanhar a mesma pessoa entre extrações. |
| 17 | **Instituições podem vir de texto livre**, com erros de grafia e variações de nome [NT]. | Instituição não é usada nos indicadores da V1. |
| 18 | **Grupos pequenos.** O grupo Indígena tem poucas pessoas em vários recortes anuais (por exemplo, 39 pessoas com sexo declarado em STEM formação em 2023, contra 178 no agregado 2020 a 2025). | Flags de amostra pequena e uso do agregado como número principal para Indígena (seção 4.1). |

---

## 3. Dicionário das Variáveis

### 3.1 Colunas do consolidado

O consolidado tem 18 colunas: 16 de análise e 2 de controle. Os valores listados são os valores distintos reais da extração de referência (2020 a 2025), conferidos por teste automático, que falha se surgir categoria nova.

| Variável | Descrição | Valores na extração de referência |
| --- | --- | --- |
| `Ano` | Ano de obtenção da última titulação [NT][WB]. | 2020 a 2025 no consolidado. |
| `Sexo` | Sexo registrado no currículo [NT]. | `Feminino`, `Masculino`, `Não declarado` (este último não aparece na [NT]; ver limitação 9). |
| `Cor ou Raça` | Cor ou raça registrada no currículo [NT]. | `Amarela`, `Branca`, `Indígena`, `Parda`, `Preta`, `Não desejo declarar`. |
| `Nível (Formação)` | Última titulação registrada no módulo de formação [NT]. | `Mestrado`, `Mestrado Profissional`, `Doutorado`. |
| `Grande Área (Formação)` | Primeiro nível da Árvore do Conhecimento do CNPq [NT]. | `Ciências Agrárias`, `Ciências Biológicas`, `Ciências da Saúde`, `Ciências Exatas e da Terra`, `Ciências Humanas`, `Ciências Sociais Aplicadas`, `Engenharias`, `Lingüística, Letras e Artes`, `Outra`, `Tecnologias`, `Não informado`. |
| `Área (Formação)` | Segundo nível da Árvore, vinculado à tabela de programas da CAPES. Sem programa CAPES, vem do campo livre do currículo, que não é obrigatório [NT]. | Nomes da tabela de áreas do CNPq (ex.: `Ciência da Computação`, `Probabilidade e Estatística`) e `Não informado`. |
| `Região (Formação)` | Região da instituição de titulação [NT]. | `Centro-Oeste`, `Nordeste`, `Norte`, `Sudeste`, `Sul`, `Não informado`. |
| `UF (Formação)` | Unidade da Federação da instituição de titulação [NT]. | **Nome do estado por extenso** (ex.: `São Paulo`), não a sigla, e `Não informado`. |
| `Grande Área (Atuação)` | Grande área da área indicada como **principal** no módulo Áreas de Atuação do currículo [NT]. Pode divergir da formação [NT]. | Os mesmos valores de Formação e também `Serviço Social` (limitação 12). |
| `Área (Atuação)` | Área de atuação principal declarada [NT]. | Nomes da Árvore (ex.: `Ciência da Computação`) e `Não informado`. |
| `Região (Atuação)` | Região da instituição de atuação, que é a do vínculo vigente [NT]. | `Centro-Oeste`, `Nordeste`, `Norte`, `Sudeste`, `Sul`, `Não informado`. |
| `UF (Atuação)` | Unidade da Federação da instituição de atuação [NT]. | Nome do estado por extenso e `Não informado`. |
| `Setor de Atividade (Atuação)` | Setor da instituição principal de atuação, pela classificação do Manual Frascati da OCDE [NT]. | `Ensino Superior`, `Ensino Técnico/Prof. e de 2º Grau`, `Setor Empresarial`, `Setor Exterior`, `Setor Governamental`, `Setor Privado sem Fins Lucrativos`, `Não informado`. |
| `Enquadramento (Atuação)` | Enquadramento funcional no vínculo principal. Campo aberto, agrupado pelo CNPq [NT]. | Dezenas de categorias agrupadas (ex.: `Professor`, `Pesquisador`, `Analista`, `Bolsista`), além de `Outro` e `Não informado`. |
| `Bolsista - PQ` | Já recebeu bolsa de Produtividade em Pesquisa do CNPq (histórico) [NT]. | `Sim`, `Não`. O pipeline também aceita vazio como "não", para compatibilidade com arquivos antigos. |
| `Bolsista - DT` | Já recebeu bolsa de Produtividade em Desenvolvimento Tecnológico e Extensão Inovadora (histórico) [NT]. | `Sim`, `Não`. |
| `Totalpessoas` | **Controle.** Número de pessoas com a combinação de atributos da linha. | Inteiro positivo. |
| `Data Extração BD Lattes` | **Controle.** Data da extração. No CSV exportado vem no formato mês/dia/ano: `10/4/2026` é 4 de outubro de 2026, confirmado pelo extrato do workbook, que guarda o campo como data [WB]. | `10/4/2026` em todos os registros. |

### 3.2 Variáveis dos brutos fora do consolidado

Os brutos trazem também `País de Nascimento`, `País`, `Cidade` e `Instituição` (de formação e de atuação) e as bolsas de iniciação científica, graduação sanduíche, mestrado, doutorado e pós-doutorado, além dos níveis de PQ e DT (1A, 1B, 1C, 1D e 2) [NT]. As bolsas de doutorado e pós-doutorado incluem concessões no país e no exterior [NT]. As colunas de bolsa são lidas dos brutos só para o relatório de qualidade.

O workbook tem ainda campos que não estão na aba de download, como faixa etária (grupos de 5 anos no padrão do IBGE [NT]), vínculo, regime de trabalho e natureza da atividade [WB].

---

## 4. Matriz de Indicadores

### 4.1 Regras gerais

- **Contagem:** numerador e denominador são somas de `Totalpessoas` (pessoas). A saída traz também o número de linhas de cada um, para auditoria.
- **Sexo declarado:** os denominadores consideram só Feminino e Masculino. Nos indicadores com recorte de sexo, "Todos" é Feminino + Masculino.
- **Raça declarada:** "Não desejo declarar" sai dos denominadores dos indicadores raciais, e a taxa de não declaração é publicada como indicador próprio, por ano e sexo.
- **"Não informado"** em grande área ou região de atuação sai das categorias e dos denominadores. As taxas de "Não informado" vão para o relatório de qualidade (`qualidade_v1.csv`), que serve à metodologia e não é publicado.
- **STEM:** Grande Área ∈ {`Ciências Exatas e da Terra`, `Engenharias`}, tanto na formação quanto na atuação. "Tecnologias" fica fora.
- **Categoria Negra:** soma de Preta e Parda (convenção do IBGE), publicada como linha adicional, ao lado dos grupos desagregados, e marcada como agregada (`raca_agregada`). Ela nunca entra em somas junto com os grupos desagregados. No código, `config.AGREGAR_NEGRA = True`; desligar a opção remove só as linhas Negra, sem alterar o resto da saída.
- **Flags de amostra pequena** (colunas separadas, para o front decidir como exibir):
  - `flag_denominador_pequeno`: denominador menor que 30, nos indicadores de participação e na taxa de não declaração;
  - `flag_numerador_pequeno`: numerador menor que 10, na composição racial das mulheres. Com poucas pessoas, variações entre anos parecem grandes mesmo que o percentual seja preciso;
  - `flag_preferir_agregado`: valores anuais do grupo Indígena, cujo número principal é o agregado 2020 a 2025.

### 4.2 Indicadores implementados na V1

**Indicadores de base**

| Indicador | Base | Recortes | Fórmula | Limitação principal |
| --- | --- | --- | --- | --- |
| **Participação feminina geral** | Por ano de titulação | Todas as áreas | `pessoas Feminino / pessoas com sexo declarado × 100` | Limitações 1, 3 e 9. |
| **Participação feminina em STEM (formação)** | Por ano de titulação | Grande Área (Formação) ∈ STEM | `pessoas Feminino em STEM / pessoas em STEM com sexo declarado × 100` | Limitações 12 e 13. Na extração de referência, o agregado 2020 a 2025 é 34,66%. |
| **Participação feminina por nível de formação** | Por ano de titulação | Mestrado, Mestrado Profissional, Doutorado | `pessoas Feminino no nível X / pessoas no nível X com sexo declarado × 100` | Limitação 4 (encolhimento das coortes de mestrado). |
| **Participação feminina por grande área de formação** | Por ano de titulação | Cada grande área de formação, exceto "Não informado" | `pessoas Feminino na grande área X / pessoas na grande área X com sexo declarado × 100` | Grandes áreas não captam a heterogeneidade interna. |
| **Participação feminina em STEM (atuação)** | Situação em out/2026 das pessoas tituladas de 2020 a 2025 | Grande Área (Atuação) ∈ STEM | `pessoas Feminino com atuação STEM / pessoas com atuação STEM e sexo declarado × 100` | Limitações 6 e 10: quem não tem grande área de atuação informada fica fora. |
| **Participação feminina na atuação em Computação** | Situação em out/2026 das pessoas tituladas de 2020 a 2025 | `Área (Atuação)` = `Ciência da Computação` | `pessoas Feminino com atuação em Computação / pessoas com atuação em Computação e sexo declarado × 100` | Área de atuação principal declarada [NT]. Subespecialidades de computação não existem como área separada. |
| **Participação feminina na atuação em Computação por região** | Situação em out/2026 das pessoas tituladas de 2020 a 2025 | Região (Atuação), exceto "Não informado" | `pessoas Feminino com atuação em Computação na região R / pessoas com atuação em Computação na região R e sexo declarado × 100` | Cobre só pessoas com vínculo de atuação registrado (limitação 10). |

**Indicadores do recorte de raça** (interseccionalidade gênero × raça), aplicados à participação geral, à de STEM (formação e atuação) e à de nível de formação. Os dois primeiros não podem ser confundidos:

| Indicador | O que responde | Numerador | Denominador | Flag |
| --- | --- | --- | --- | --- |
| **Participação feminina dentro do grupo racial** (`participacao_feminina_no_grupo_racial`) | Entre as pessoas do grupo racial R, qual % é mulher? | mulheres da raça R | pessoas da raça R com sexo declarado | denominador < 30 |
| **Composição racial das mulheres** (`composicao_racial_das_mulheres`) | Entre as mulheres, qual % é do grupo racial R? | mulheres da raça R | mulheres com raça declarada | numerador < 10 |
| **Taxa de não declaração de raça** (`taxa_nao_declaracao_raca`) | Qual % não declarou raça? | pessoas com "Não desejo declarar" | pessoas com sexo declarado (no sexo indicado) | denominador < 30 |

Grupos raciais: Branca, Parda, Preta, Amarela, Indígena e Negra (Preta + Parda).

Correções em relação à fórmula de interseccionalidade da versão anterior: o recorte STEM passa a usar **Grande Área**, de acordo com a definição oficial de STEM, e o denominador da composição **exclui "Não desejo declarar"**, de acordo com a regra dos demais indicadores. O indicador passou de "sugerido" a "implementado".

### 4.3 Indicadores fora da V1, com motivo

| Indicador | Situação na versão anterior | Motivo |
| --- | --- | --- |
| **Proporção de mulheres entre bolsistas PQ** | Implementado | Volume muito baixo: 351 pessoas tituladas de 2020 a 2025 já receberam PQ, das quais 76 mulheres, e o recorte racial ficaria quase todo abaixo dos limites de amostra. PQ é bolsa de meio e fim de carreira, então as pessoas tituladas de 2020 a 2025 que já receberam PQ são uma fatia atípica dos bolsistas. As bolsas são histórico (limitação 14). |
| **Razão de gênero em PQ por nível; participação feminina em DT por nível** | Sugeridos | Mesmos motivos. DT tem volume ainda menor: 68 pessoas, das quais 21 mulheres. |
| **Participação feminina por setor de atividade** | Sugerido | Setor "Não informado" para 47,07% das pessoas (limitação 11). "Não informado" pode indicar desemprego ou currículo desatualizado [NT], então a exclusão não é neutra. |
| **Participação feminina por enquadramento** | Sugerido | Enquadramento "Não informado" para 23,11%, e o campo é aberto e agrupado pelo CNPq [NT], com uma categoria "Outro" grande. |
| **Participação feminina por UF** | Sugerido | Não priorizado na V1. A UF vem por extenso; para o front, será criada uma coluna derivada com a sigla quando o indicador entrar. |
| **Taxa de crescimento anual de pesquisadoras** | Sugerido | Com `Ano` = ano de titulação, coortes de uma única extração e coortes de mestrado que encolhem (limitações 1, 4 e 5), a variação entre anos mistura entrada na pós-graduação, atraso de atualização e progressão para o doutorado. |
| **Gap formação × atuação; concentração regional de formação × atuação** | Sugeridos | A completude da atuação é muito menor que a da formação (limitação 10). Exigem restringir aos registros com os dois lados informados. |

### 4.4 Propostas para a V2

| Proposta | Condições e riscos |
| --- | --- |
| **Ampliar a série para coortes anteriores a 2020** (o painel cobre de 1948 ao ano atual [NT]). Basta mudar `config.ANOS`. | Viés de sobrevivência: o universo só tem currículos atualizados nos últimos 60 meses [NT], então as coortes antigas só contêm quem continua ativo no Lattes (quem saiu da carreira, se aposentou ou faleceu tende a sumir). As coortes antigas de mestrado ficam só com quem não fez doutorado (limitação 4). A não declaração de raça deve ser maior nas coortes antigas, o que piora a comparabilidade do recorte racial. Ordem sugerida: primeiro os indicadores de formação sem raça, com ressalva de sobrevivência; raça e bolsas depois de checar a não declaração por coorte. |
| **Bolsas PQ e DT sobre todas as coortes**, com níveis (1A a 2). | Depende da ampliação da série. Interpretar como "já recebeu a bolsa", porque as bolsas são histórico (limitação 14). |
| **Participação feminina por UF**, com coluna `uf_sigla`. | UFs pequenas exigem as mesmas flags de amostra. |
| **Gap formação × atuação e fluxos regionais**, restritos a quem tem os dois lados informados. | Limitação 10. |
| **Setor e enquadramento**, se o preenchimento melhorar em extrações futuras. | Limitação 11. A taxa de "Não informado" segue no relatório de qualidade para acompanhamento. |
| **Coorte de 2026**, com uma extração feita depois do fim do ano. | Seção 5. |

### 4.5 Formato de saída

Os indicadores ficam em `data/processed/indicadores/indicadores_v1.csv`, em formato longo, com as colunas `indicador`, `base`, `periodo`, `recorte`, `categoria`, `sexo`, `raca`, `raca_agregada`, `numerador`, `denominador`, `percentual` (0 a 100, duas casas), `n_linhas_numerador`, `n_linhas_denominador`, `flag_denominador_pequeno`, `flag_numerador_pequeno`, `flag_preferir_agregado` e `extracao`.

Acompanham a saída:
- `indicadores_dicionario.csv`: nome, descrição, numerador, denominador, flag recomendada e ressalva de cada indicador, base e recorte. As ressalvas com números são montadas a partir do relatório de qualidade.
- `indicadores_v1.meta.json`: extração, anos, parâmetros da categoria Negra, limites das flags e SHA-256 do consolidado.
- `qualidade_v1.csv`: taxas de "Não informado", sexo não declarado, distribuição de raça nesse grupo, distribuição das grandes áreas e bolsas já recebidas.

---

## 5. Nota sobre 2026

A coorte de titulação de 2026 tem 45.434 pessoas na extração de referência, contra 78.130 em 2025. **2026 fica fora da V1, inclusive dos percentuais.**

O motivo não é mais "extrato parcial": todos os anos vêm da mesma extração. A coorte de 2026 é incompleta porque só contém títulos obtidos até a data da extração (4/10/2026) e registrados no currículo até então. O atraso de atualização do Lattes não é aleatório (limitação 5), e por isso a coorte incompleta enviesa até as proporções, não só os volumes.

O arquivo de 2026 continua sendo baixado e guardado com os demais. Ele será reavaliado com uma extração feita depois do fim de 2026; no código, basta acrescentá-lo a `config.ANOS`.

---

## 6. Processo de download e reprodutibilidade

1. `python scripts/baixar_lattes.py --anos 2020-2026` baixa a exportação CSV da aba "Painel - Download" do workbook, um ano por vez, com pausa entre anos e retentativas. O filtro de nível é passado vazio para trazer os três níveis, porque a view vem pré-filtrada.
2. Cada arquivo é validado (codificação, separador, colunas obrigatórias, um único ano, uma única data de extração, `Totalpessoas` inteiro positivo) e guardado como veio em `data/raw/{data_extracao}/lattes_{ano}.csv`.
3. O `manifest.json` de cada extração registra, por ano: URL, data e hora do download, tamanho, SHA-256, linhas, pessoas e a data de extração original.
4. Se a automação falhar, o script mostra como baixar à mão pelo painel (a [NT] cita download em .xlsx e .csv; o pipeline usa o CSV). Os arquivos manuais, nos dois formatos aceitos, vão para `data/raw/_entrada/` e são validados e organizados da mesma forma.
5. Atenção ao comparar com os totais exibidos no painel: nos gráficos, o workbook usa uma fonte de dados duplicada (para o diagrama "De Para") e divide as contagens por 2 [WB]. A fonte da aba de download não é duplicada, e o pipeline não divide nada.
6. `python scripts/consolidar_lattes.py` confere o SHA-256 de cada bruto contra o manifest e gera o consolidado. `python scripts/gerar_indicadores.py` gera os indicadores, o dicionário, o meta e o relatório de qualidade.
7. Testes: `pytest` (unitários), `pytest -m dados` (contagens contra `tests/referencias/2026-10-04.json`, domínios das categorias e identidades entre indicadores) e `pytest -m rede` (acesso ao painel e à exportação).

---

## 7. Perguntas em aberto ao CNPq

Nenhuma delas bloqueia a V1. O texto para envio pelo Fala.BR está em `docs/perguntas_cnpq.md`.

| # | Pergunta | Por que importa |
| --- | --- | --- |
| 1 | **Como surge o sexo "Não declarado"**, se o currículo só oferece feminino e masculino [NT]? Por que, nesse grupo, "Preta" é a categoria de raça mais frequente, e por que o grupo cresce nas coortes recentes? | O padrão (limitação 9) sugere problema de preenchimento ou de codificação. Os indicadores excluem esse grupo, mas o grupo cresce. |
| 2 | **Por que "Serviço Social" aparece como grande área de atuação**, se na Árvore do Conhecimento ele é uma área de Ciências Sociais Aplicadas? | Pode indicar outras classificações fora da Árvore (limitação 12). O volume atual é desprezível. |
| 3 | **"Ano de início" ou ano de obtenção do título?** A [NT] diz que registros sem "ano de início da titulação" ficam fora, mas no resto do texto e no painel o campo é o ano de obtenção do título. | Define exatamente quem fica fora do universo (limitação 3). A V1 trata como ano de obtenção. |

---

## 8. Fontes

| Recurso | Referência |
| --- | --- |
| Painel Formação e Atuação Lattes | [http://bi.cnpq.br/painel/formacao-atuacao-lattes/](http://bi.cnpq.br/painel/formacao-atuacao-lattes/) |
| Workbook no Tableau Public [WB] | `https://public.tableau.com/views/PainelLattes-FormaoeAtuao/` (aba "Painel - Download") |
| Nota Técnica 01/2024 [NT] | [nota_tecnica_painel_lattes.pdf](nota_tecnica_painel_lattes.pdf) |
| Código do pipeline | `scripts/` e `src/lattes/` deste repositório. Parâmetros em `src/lattes/config.py`. |
| Versão anterior desta metodologia | [historico/metodologia_lattes_2026-07.md](historico/metodologia_lattes_2026-07.md) |
