# Registro de decisões da V1 da base Lattes

Decisões metodológicas da V1, todas **aprovadas pela coordenação do projeto em 23/10/2026**. A base de referência é a extração de 4/10/2026 do Painel de Formação e Atuação do Lattes (CNPq). Os detalhes e números estão na [metodologia V1](metodologia_lattes.md).

| # | Tema | Decisão | Data | Aprovação | Motivo |
| --- | --- | --- | --- | --- | --- |
| 1 | Extração de referência | A extração de 4/10/2026 é a base da V1. A metodologia de julho/2026 fica só como histórico (`docs/historico/`). | 23/10/2026 | Aprovada pela coordenação do projeto | Os brutos antigos não existem mais, e o painel só serve a extração vigente. A de 4/10/2026 é a única que pode ser baixada de novo e auditada. |
| 2 | Unidade de contagem | Os indicadores contam pessoas (soma de `Totalpessoas`), com o número de linhas junto para auditoria. | 23/10/2026 | Aprovada pela coordenação do projeto | Cada linha do arquivo agrega pessoas com os mesmos atributos, e cada pessoa entra uma vez, pela última titulação (Nota Técnica 01/2024). |
| 3 | Período | A série vai de 2020 a 2025. Ampliar para coortes anteriores fica como proposta de V2. | 23/10/2026 | Aprovada pela coordenação do projeto | As coortes antigas sofrem viés de sobrevivência (só currículos atualizados nos últimos 60 meses) e devem ter mais "não declarado" em raça. |
| 4 | Coorte de 2026 | 2026 fica fora da V1, inclusive dos percentuais. | 23/10/2026 | Aprovada pela coordenação do projeto | É uma coorte de titulação incompleta, e o atraso de atualização do Lattes não é aleatório, o que enviesa até as proporções. |
| 5 | Categoria Negra | A categoria Negra (Preta + Parda) é publicada ao lado das categorias desagregadas, nunca no lugar delas (`config.AGREGAR_NEGRA = True`). | 23/10/2026 | Aprovada pela coordenação do projeto | É a convenção do IBGE nas estatísticas oficiais, e dá volume a comparações que, separadas, ficam pequenas em alguns recortes. |
| 6 | Bolsas PQ e DT | PQ e DT ficam fora da V1. Na V2, entram calculadas sobre todas as coortes e interpretadas como "já recebeu a bolsa". | 23/10/2026 | Aprovada pela coordenação do projeto | O volume nas coortes de 2020 a 2025 é muito baixo, e as bolsas são histórico de concessões (Plataforma Carlos Chagas), não situação vigente. |
| 7 | Setor e enquadramento | Ficam fora da V1 e aparecem só no relatório de qualidade. | 23/10/2026 | Aprovada pela coordenação do projeto | O preenchimento "Não informado" é muito alto e pode indicar desemprego ou currículo desatualizado (Nota Técnica), então excluir esses casos não seria neutro. |
| 8 | "Tecnologias" e STEM | "Tecnologias" fica fora da definição de STEM, que continua sendo Grande Área ∈ {Ciências Exatas e da Terra, Engenharias}. | 23/10/2026 | Aprovada pela coordenação do projeto | A categoria não existe na Árvore do Conhecimento do CNPq e tem volume desprezível. |
| 9 | Indicadores de situação atual | STEM atuação, atuação em Computação e Computação por região ficam agregados em 2020 a 2025, rotulados como perfil de início de carreira ("situação em out/2026 das pessoas tituladas de 2020 a 2025"). | 23/10/2026 | Aprovada pela coordenação do projeto | A atuação reflete a data da extração; por coorte recente, mediria sobretudo o tempo desde o título. |
| 10 | Amostras pequenas | Flag quando o denominador é menor que 30 (participação feminina dentro do grupo racial), flag quando o numerador é menor que 10 (composição racial das mulheres) e agregado 2020 a 2025 como número principal para Indígena. | 23/10/2026 | Aprovada pela coordenação do projeto | Evita que o front exiba percentuais instáveis, ou variações anuais aparentes, sem aviso. |

## Itens resolvidos pela recomendação registrada

Estes pontos estavam no documento de decisões pendentes (`docs/decisoes_professora.md`, agora este registro) e não constavam da lista aprovada. Foram resolvidos aplicando a recomendação registrada lá. **Aguardam confirmação da coordenação.**

| # | Tema | Decisão aplicada | Motivo |
| --- | --- | --- | --- |
| 11 | Perguntas ao CNPq | Enviar as perguntas sobre sexo "Não declarado", "Serviço Social" como grande área, "ano de início" na Nota Técnica e calendário de extrações (`docs/perguntas_cnpq.md`). Nenhuma bloqueia a V1. | Os indicadores exigem sexo declarado, e "Serviço Social" tem volume desprezível. |
| 12 | Uma extração por versão | Cada versão publicada fixa uma extração, com brutos e manifest guardados fora do repositório. | O painel muda todo mês e só serve a extração mais recente; sem os brutos, a versão não pode ser reproduzida. |
| 13 | Ordem da ampliação na V2 | Na V2, a série longa começa pelos indicadores de formação sem raça, com ressalva de sobrevivência; raça e bolsas entram depois de checar a não declaração por coorte. | Os riscos da série longa são maiores no recorte racial e nas bolsas. |
| 14 | Reavaliar 2026 | 2026 é reavaliado com uma extração feita depois do fim do ano. | Só então a coorte deixa de estar incompleta por construção. |
| 15 | Volta de setor e enquadramento | Os dois podem voltar numa versão futura, se o preenchimento melhorar. A taxa de "Não informado" segue no relatório de qualidade para acompanhamento. | A exclusão é por qualidade do dado, não por falta de interesse no indicador. |
| 16 | Exibição das flags | O front não exibe percentual com flag sem um aviso visível e mostra o agregado como número principal para Indígena (regras em `docs/integracao_observatorio.md`). | Complementa a decisão 10 no lado da exibição. |
