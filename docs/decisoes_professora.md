# Decisões pendentes para a V1 da base Lattes

Lista para revisão com a professora. Cada item traz o contexto, o que está implementado hoje e a recomendação. Detalhes e números na [metodologia V1](metodologia_lattes.md). Extração de referência: 4/10/2026.

---

## 1. Categoria Negra (Preta + Parda)

**Contexto.** A convenção do IBGE agrega Preta e Parda como Negra. Os grupos desagregados (Branca, Parda, Preta, Amarela, Indígena) são publicados de qualquer forma.

**Hoje.** A categoria está implementada como opção (`config.AGREGAR_NEGRA`), ligada por padrão. Ligada, gera linhas extras marcadas como agregadas; desligada, o resto da saída é idêntico.

**Recomendação.** Incluir. É a convenção usada nas estatísticas oficiais e dá volume a comparações que, separadas, ficam pequenas em alguns recortes. O front deve exibir a categoria Negra sempre ao lado dos grupos desagregados, nunca no lugar deles.

## 2. Bolsa PQ fora da V1

**Contexto.** Na metodologia de julho/2026, a proporção de mulheres entre bolsistas PQ estava como indicador **implementado**. Com a nova leitura da base, só 351 pessoas tituladas de 2020 a 2025 já receberam PQ (76 mulheres). PQ é bolsa de meio e fim de carreira, e as bolsas da base são histórico ("já recebeu"), não situação vigente.

**Hoje.** PQ e DT ficam fora da V1.

**Recomendação.** Confirmar a retirada e levar PQ para a V2, calculado sobre todas as coortes, junto com a ampliação da série (item 3).

## 3. Ampliar a série para coortes anteriores a 2020 (V2)

**Contexto.** O painel cobre de 1948 ao ano atual (Nota Técnica 01/2024). No código, ampliar é só mudar `config.ANOS`. Há três riscos:
- viés de sobrevivência: só entram currículos atualizados nos últimos 60 meses, então as coortes antigas só têm quem continua ativo no Lattes;
- as coortes antigas de mestrado ficam só com quem não fez doutorado;
- a não declaração de raça deve ser maior nas coortes antigas.

**Recomendação.** Ampliar na V2, mas com cautela. Primeiro, publicar a série longa só para os indicadores de formação sem raça, com a ressalva de sobrevivência. Depois, incluir raça e PQ após checar a não declaração de raça por coorte. Tratar a série antiga como "quem segue ativo no Lattes", não como "quem se titulou".

## 4. Indicadores de situação atual como perfil de início de carreira

**Contexto.** `Ano` é o ano da última titulação, e área e região de atuação são a situação na data da extração. Por coorte recente, esses indicadores mediriam o tempo desde o título.

**Hoje.** STEM de atuação, atuação em Computação e Computação por região são calculados só no agregado 2020 a 2025, com o rótulo "situação em out/2026 das pessoas tituladas de 2020 a 2025".

**Recomendação.** Aprovar. Na comunicação pública, deixar explícito que é um perfil de início de carreira, não de todas as pesquisadoras.

## 5. Coorte de 2026 fora da V1

**Contexto.** A coorte de 2026 só tem títulos até a data da extração, e o atraso de atualização do Lattes não é aleatório (varia por área, nível e perfil). Por isso ela enviesa até as proporções.

**Hoje.** 2026 é baixado e guardado, mas fica fora dos indicadores, inclusive dos percentuais.

**Recomendação.** Aprovar. Reavaliar com uma extração feita depois do fim de 2026.

## 6. Setor de atividade e enquadramento fora da V1

**Contexto.** Os dois estavam como indicadores sugeridos. Setor tem 47,07% de "Não informado" e Enquadramento, 23,11%, além de uma categoria "Outro" grande. Pela Nota Técnica, "Não informado" pode indicar desemprego ou currículo desatualizado, então excluir esses casos não é neutro.

**Recomendação.** Aprovar a retirada. As taxas ficam registradas no relatório de qualidade, e os dois indicadores podem voltar se o preenchimento melhorar.

## 7. Regras de amostra pequena

**Contexto.** Alguns grupos raciais têm poucas pessoas em recortes anuais, principalmente Indígena em STEM e no Mestrado Profissional.

**Hoje.**
- Participação feminina dentro do grupo racial: flag quando o denominador é menor que 30.
- Composição racial das mulheres: flag quando o numerador é menor que 10.
- Indígena: o número principal é o agregado 2020 a 2025, e os valores anuais saem com flag.
- As flags são colunas separadas, para o front decidir como exibir.

**Recomendação.** Aprovar. Sugestão para o front: não exibir percentual com flag sem um aviso visível, e mostrar o agregado como número principal para Indígena.

## 8. "Tecnologias" fora do STEM

**Contexto.** "Tecnologias" não existe na Árvore do Conhecimento do CNPq e abarca sobretudo especialidades próximas das Engenharias (Nota Técnica). São só 2 pessoas na formação e 40 na atuação.

**Recomendação.** Aprovar a exclusão (impacto desprezível) e registrar como limitação, o que já está feito.

## 9. Perguntas a enviar ao CNPq

**Contexto.** Há quatro pontos que só o CNPq pode esclarecer:
- **Sexo "Não declarado":** são 4.119 pessoas (0,96%), mas o currículo só oferece feminino e masculino (Nota Técnica). Nesse grupo, "Preta" é a maior categoria de raça (35,81%, contra 8,23% entre quem declarou sexo), e o grupo cresce nas coortes recentes.
- **"Serviço Social" como grande área de atuação** (1 pessoa), embora na Árvore ele seja uma área.
- **"Ano de início" ou ano de obtenção:** um trecho da Nota Técnica fala em "ano de início da titulação" para os registros excluídos; o resto do texto fala em ano de obtenção.
- **Data das próximas extrações** e se há histórico de extrações anteriores disponível.

**Recomendação.** Enviar as perguntas. Nenhuma delas bloqueia a V1: os indicadores exigem sexo declarado, e "Serviço Social" tem volume desprezível.

## 10. Base da V1 e números da versão anterior

**Contexto.** Os brutos antigos não existem mais, e o painel só oferece a extração vigente, que é mensal. Os números da metodologia de julho/2026 (contagens e percentuais) não são reproduzíveis e foram substituídos pelos da extração de 4/10/2026.

**Hoje.** A versão anterior fica preservada em `docs/historico/`.

**Recomendação.** Aprovar a extração de 4/10/2026 como base da V1 e adotar a regra de fixar uma extração por versão publicada, com os brutos e o manifest guardados.
