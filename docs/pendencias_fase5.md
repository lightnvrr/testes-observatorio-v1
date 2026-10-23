# Pendências para a Fase 5 (atualização da metodologia)

Notas de trabalho acumuladas nas fases 1 a 4. Cada item vira uma alteração em `docs/metodologia_lattes.md` na Fase 5.

Fontes citadas:
- **[NT]**: CNPq, *Painel de Formação e Atuação do Lattes, Nota Técnica 01/2024* (`docs/nota_tecnica_painel_lattes.pdf`).
- **[WB]**: workbook `PainelLattes-FormaoeAtuao` no Tableau Public (arquivo .twbx: fórmulas do .twb e extratos .hyper), publicado em 2026-10-09.

## Fonte e download

- A página `bi.cnpq.br` apenas embute um workbook do **Tableau Public** [WB]. Os brutos vêm da aba "Painel - Download", exportada por URL (`Painel-Download.csv?:showVizHome=no&.Ano={ano}&.Nível (Formação)=`).
- A exportação por URL vem em **UTF-8 com vírgula**. O formato antigo (UTF-16 com tabulação) era o da "Tabela de referência cruzada" da interface. Os dois são aceitos e o bruto é guardado como veio. A [NT] cita download em .xlsx e .csv.
- Brutos organizados por extração: `data/raw/{data_extracao}/lattes_{ano}.csv` + `manifest.json`.
- Seção 1, "Formato dos arquivos", "Volume de dados (bruto)" e "Periodicidade": atualizar. A [NT] prevê extração **mensal**; cada extração pode mudar os resultados, por isso a base da V1 fica fixada na extração 2026-10-04.

## Universo e unidade de análise

- **Universo (nova limitação):** só entram CVs **atualizados nos últimos 60 meses**, mesma regra da Busca de Currículos do Lattes [NT]. Quem não atualiza o currículo há mais de 5 anos some da base, e isso não é aleatório (afeta mais quem saiu da academia).
- **Limitação 2 reescrita:** **não há dupla contagem.** Cada pessoa é contada uma vez, pela **última titulação** registrada; doutores não entram na contagem de mestres, mesmo com o mestrado registrado no CV [NT]. `Nível (Formação)` = maior (última) titulação. Fica resolvida a dúvida anterior sobre mestrado + doutorado.
- Registros sem ano de titulação ficam fora do painel [NT]. Obs.: a [NT] fala em "ano de início da titulação" nesse trecho, mas no resto do texto e no [WB] o campo é o ano de obtenção do título; tratar como ano de obtenção.
- **Nova limitação: coortes de mestrado encolhem com o tempo.** Quem é mestre em 2020 e vira doutor em 2024 sai da coorte "Mestrado 2020" e entra em "Doutorado 2024" [NT]. Coortes de mestrado antigas ficam só com quem não fez doutorado (ainda). Se a progressão para o doutorado difere por sexo (ou raça), a participação feminina no mestrado fica enviesada e o viés cresce com a idade da coorte. Comparações de mestrado entre anos devem trazer essa ressalva.
- Cada linha do bruto é uma combinação de atributos com `Totalpessoas` (1 a 9 no extrato). A contagem de linhas depende das colunas da view; a soma de `Totalpessoas` é invariante (conferido contra o extrato .hyper [WB]).
- Decisão: indicadores contam **pessoas** (soma de `Totalpessoas`); `n_linhas` vai junto na saída para auditoria.
- No [WB], as medidas do painel dividem `TOTALPESSOAS` por 2 porque a fonte dos gráficos é duplicada (coluna `Path`, 0 e 200, usada no diagrama "De Para"). A fonte da aba de download **não** é duplicada; não dividir.
- Não se sabe se os brutos antigos (UTF-16) tinham `Totalpessoas`: os arquivos não existem mais. Registrar como incerteza sobre os números antigos (415.920, 34,7%, 26,9%, 17,4%, 5,6%), que não são reproduzíveis.

## Significado de `Ano`

- `Ano` = **ano de obtenção da última titulação** (`.Ano = [ANOOBTENCAOTITULO]` [WB]; "Ano de Formação" [NT]), não ano de extrato. A doc diz "Ano de referência do extrato" (dicionário 2.1) e "extrato anual" (seção 1). Corrigir.
- A base é **um retrato único** (uma extração, `DATAEXTRACAO` = 2026-10-04) de pessoas tituladas de 1948 a 2026, recortado por ano de titulação. A [NT] chama a série de "estoque por ano". Indicadores "por ano" são **por coorte de titulação**.
- Seção 4 (2026), **decidido: 2026 fica fora da V1, inclusive dos percentuais.** Substituir o motivo antigo ("extrato parcial") por: a coorte de titulação de 2026 está incompleta (títulos só até 4/10/2026) e o atraso de atualização do Lattes não é aleatório; varia por área, nível e perfil de quem atualiza o currículo. Por isso a coorte incompleta enviesa até as proporções, não só os volumes absolutos.
- **Decidido: V1 cobre 2020 a 2025.** Ampliar é só mudar `config.ANOS`.

## Indicadores de formação × situação atual

- Consequência de `Ano` = ano de titulação: indicadores de situação atual por coorte recente medem sobretudo **tempo desde o título**, não desigualdade (ex.: PQ cai de 106 pessoas na coorte 2020 para 15 em 2025).
- **Decidido:**
  - indicadores de **formação** (sexo, raça, grande área e área de formação, nível) continuam **por ano de titulação**;
  - indicadores de **situação atual** (área de atuação, setor, enquadramento, atuação em Computação, distribuição regional da atuação) são calculados sobre **2020 a 2025 agregado**. Nome e texto devem dizer o que são: **"situação em out/2026 das pessoas tituladas de 2020 a 2025"**, um perfil de início de carreira, não de todas as pesquisadoras.
- **Decidido: PQ fica fora da V1**, inclusive o agregado 2020 a 2025 (351 pessoas PQ, 76 mulheres; recorte racial quase todo abaixo de n = 30; quem se titulou há até 6 anos e já é PQ é uma fatia atípica do total de bolsistas PQ). Na metodologia, PQ estava como "indicador implementado" (3.1): mover para proposta de V2.

## Dimensões (a partir da [NT])

- **Formação × Atuação:** Atuação é a área indicada como **principal** no módulo Áreas de Atuação do CV; pode divergir da formação (ex.: formação em Humanas, atuação em Saúde) [NT].
- **Área de formação** vem da tabela de programas da CAPES; sem programa CAPES, usa o campo livre do CV, que não é obrigatório ("Não informado") [NT].
- **Grande Área:** "Não informado" = dado indisponível; "Outra" = divergente da Árvore do Conhecimento; **"Tecnologias" não existe na Árvore do CNPq** e abarca sobretudo especialidades próximas das Engenharias [NT]. No consolidado: 40 pessoas em Atuação (29 em "Tecnologia da Informação e Comunicação"; 8 mulheres) e 2 em Formação. **Decidido: "Tecnologias" fica fora do STEM** (formação e atuação). Registrar como limitação conhecida, com esses volumes.
- **Instituição de atuação** = vínculo vigente (início preenchido, fim em branco), com precedência: dedicação exclusiva/integral, maior carga horária, vínculo formal, início mais recente. **"Não informado" pode indicar desemprego ou CV desatualizado** [NT]. Vale também para Região/UF/Setor de atuação, que derivam da instituição.
- **Enquadramento funcional** é campo aberto, agrupado pelo CNPq a partir dos termos digitados [NT]. Categorias podem misturar situações distintas.
- **Setor de atividade** segue a classificação do **Manual Frascati (OCDE)** [NT].
- **Instituições** (formação e atuação) podem vir de texto livre, com erros de grafia e variações [NT].
- **Sexo:** a [NT] lista só "feminino" e "masculino", mas o consolidado tem **"Não declarado" em 4.119 pessoas (0,96%)**, crescendo nas coortes recentes (378 em 2020; 918 em 2025). Documentar o valor e manter a exclusão do denominador.
- **Nota de qualidade (sexo "Não declarado"):** nesse grupo, "Preta" é a maior categoria de raça (1.475 de 4.119 pessoas, 35,8%, contra 8,5% na base toda), e "Não desejo declarar" chega a 22,9% (5,8% na base). Junto com o crescimento do grupo nas coortes recentes, sugere problema de preenchimento ou de codificação, não um retrato real. Sem tratamento no pipeline: os indicadores raciais exigem sexo declarado, então esse grupo não entra neles. Entra só na taxa de não declaração de raça da população total, com ressalva.
- **Pergunta para o CNPq:** como surge `Sexo = "Não declarado"`, se o campo do CV só oferece feminino e masculino [NT]? Por que, nesse grupo, "Preta" é a cor/raça mais frequente? O grupo cresce nas coortes recentes por alguma mudança no formulário ou na extração?
- **Cor ou raça:** opções amarela, branca, indígena, parda, preta e "não desejo declarar" [NT], iguais às do consolidado.

## Bolsas (limitação 6 reescrita)

- Bolsas vêm da **Plataforma Integrada Carlos Chagas** (concessões do CNPq), **não são autodeclaradas** [NT]. Doutorado e pós-doutorado incluem concessões no país e no exterior.
- **São histórico ("já recebeu"), não vigentes.** Evidência no consolidado: **19,7% dos doutores** (2020 a 2025) têm `Bolsista - Iniciação Científica = "Sim"` (bolsa de graduação), 11,5% têm bolsa de mestrado e 10,1% de doutorado. A limitação 6 ("snapshot no momento da extração") está errada: reescrever como "indica se a pessoa já recebeu a bolsa do CNPq até a data da extração".
- Consequência para a V2: "PQ" = já foi bolsista PQ em algum momento, o que favorece coortes antigas.

## Dicionário (seção 2)

- Consolidado passa a ter **18 colunas**: as 16 de análise + `Totalpessoas` + `Data Extração BD Lattes`. Atualizar seção 1 ("Volume de dados (consolidado)": 422.573 linhas, 430.305 pessoas na extração 2026-10-04) e a nota do dicionário.
- Marcar `Ano` como [Consolidado].
- Incluir `Totalpessoas` (pessoas na combinação) e corrigir `Data Extração BD Lattes` (formato no CSV: mês/dia/ano, ex.: `10/4/2026` = 4 de outubro de 2026; evidência: extrato .hyper com tipo data [WB]).
- `Nível (Formação)`: "última titulação" [NT]; confirmados só os três níveis no extrato atual.
- `UF`: vem com o nome do estado por extenso, não sigla. Criar coluna derivada `uf_sigla`.
- `Região` e `UF`: têm "Não informado".
- `Setor de Atividade (Atuação)`: 7 valores; faltam na doc "Não informado", "Ensino Técnico/Prof. e de 2º Grau", "Setor Privado sem Fins Lucrativos".
- Bolsas: valores "Sim"/"Não" (não "Sim"/vazio). O código aceita vazio também.
- Campos que existem no extrato [WB] mas não na aba de download: faixa etária (grupos de 5 anos, padrão IBGE [NT]), vínculo, regime de trabalho, natureza da atividade.

## Escopo da V1 (Fase 3)

- **Setor e enquadramento ficam fora da V1** (estavam como sugeridos). Motivo: em 2020 a 2025, 47,1% das pessoas têm Setor "Não informado" e, em Enquadramento, 23,1% são "Não informado" e cerca de 27% são "Outro"; pela [NT], "Não informado" pode ser desemprego ou CV desatualizado (não aleatório).
- `Enquadramento (Atuação)` tem 31 valores no consolidado (a doc lista 7). Corrigir o dicionário.
- **Relatório de qualidade** (`data/processed/indicadores/qualidade_v1.csv`, para a metodologia, não para o público): taxas de "Não informado" por campo, sexo e período; sexo "Não declarado" por período; distribuição de raça no grupo de sexo não declarado comparada à do sexo declarado. Levar uma tabela-resumo dele para a seção de limitações.
- Taxas de "Não informado" na extração 2026-10-04 (2020 a 2025, F + M): Grande Área (Atuação) 17,50%, Grande Área (Formação) 5,55%. Ficaram muito perto dos valores antigos da doc (17,4% e 5,6%), apesar da mudança de universo e unidade.
- Diferença por sexo no "Não informado" (2020 a 2025): Grande Área (Atuação) 18,3% F × 16,4% M (formados em STEM: 21,0% × 18,3%); Região (Atuação) em Computação 23,1% F × 24,1% M. Ressalva curta no dicionário para STEM atuação e Computação por região (números gerados a partir do relatório de qualidade).
- Computação por região: só pessoas com vínculo de atuação registrado; "Não informado" fora do denominador (regra D).

## Regras de denominador

- "Não informado" em Região, UF e Setor sai do denominador; a taxa de não informado vira indicador próprio (mesma regra de raça).

## Decisões para levar à professora

1. **PQ saiu da V1.** Estava documentado como indicador implementado (3.1). Motivos: volume (351 pessoas), coortes recentes medem tempo de carreira e as bolsas são histórico. Proposta: V2, sobre todas as coortes.
2. **Proposta de V2: ampliar a série para coortes anteriores a 2020** (o painel tem títulos desde 1948; a fonte no [WB] se chama "Ds-1998-2023"). Riscos:
   - viés de sobrevivência: a Plataforma Lattes existe desde 1999 e o universo só tem CVs atualizados em 60 meses, então coortes antigas só contêm quem segue ativo no Lattes (quem saiu da carreira, se aposentou ou faleceu tende a sumir);
   - coortes antigas de mestrado ficam só com quem não fez doutorado;
   - provável aumento de "Não desejo declarar" em raça nas coortes antigas (campo de preenchimento posterior), o que pioraria a comparabilidade do recorte racial.
3. Indicadores de situação atual passaram a ser um perfil de início de carreira (tituladas de 2020 a 2025, situação em out/2026).
4. 2026 fora da V1 (coorte incompleta com atraso de atualização não aleatório).
5. Agregação Negra = Preta + Parda: implementada como opção (`config.AGREGAR_NEGRA`, ligada por padrão). Confirmar se entra.
6. Setor e enquadramento fora da V1 (qualidade do preenchimento).
7. Regras de amostra pequena: denominador < 30 (participação no grupo racial), numerador < 10 (composição racial das mulheres), Indígena pelo agregado 2020 a 2025.
