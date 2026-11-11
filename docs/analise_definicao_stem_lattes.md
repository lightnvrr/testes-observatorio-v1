# Análise da definição de STEM da base Lattes: V1 × alinhada à PNADC

Documento de apoio para a reunião com a professora e a Evellyn. **É uma proposta**: a V1 (tag `v1.0-lattes`) não muda, e nada aqui altera `config.py`, os indicadores ou as saídas publicadas.

- O documento para o Notion, só com a lista, é o [dicionário de áreas STEM](dicionario_stem_lattes.md).
- A fonte única da classificação é `data/referencias/stem_areas_lattes.csv`, com uma linha por área: classificação, justificativa, correspondência com a COD e código na Tabela de Áreas do Conhecimento.
- Todos os números vêm de `python scripts/analisar_definicao_stem.py` (extração de 4/10/2026, pessoas com sexo declarado, 2020 a 2025), com as mesmas contagens e flags da V1.

---

## 1. As duas definições

| | STEM estrito (V1) | STEM alinhado (proposta) |
| --- | --- | --- |
| Critério | Grande Área ∈ {Ciências Exatas e da Terra, Engenharias} | Área classificada como STEM pelo mesmo critério das ocupações da PNADC (documento da Evellyn) |
| Nível usado | Grande Área | Área, o nível mais específico da base |
| Área "Não informado" | Entra se a Grande Área for STEM | Entra só se a Grande Área for uniformemente STEM |
| Ciências biológicas e agrárias | Fora | Dentro (exceto Medicina Veterinária) |
| Robótica, Microeletrônica, TIC em "Tecnologias" | Fora | Dentro |

A classificação por Área segue a Evellyn, que classifica pelo grupo de base da COD (o nível mais específico), não pelo subgrupo, porque alguns subgrupos misturam ocupações STEM e não STEM.

---

## 2. Classificação

Das 110 áreas da base (formação e atuação juntas, contando "Não informado"):

| Classificação | Áreas |
| --- | --- |
| STEM | 51 |
| não STEM | 57 |
| ambígua (pendente) | 1 |
| não informado (regra própria) | 1 |

### 2.1 Casos ambíguos: decisões e volumes

Volumes em pessoas com sexo declarado, 2020 a 2025. A última coluna mostra a participação feminina em STEM formação (agregado) **se a área tivesse a classificação oposta**; com a classificação proposta, ela é 45,46%.

| Área | Decisão | Formação (F / M) | Atuação (F / M) | Se invertida (formação) | Motivo |
| --- | --- | --- | --- | --- | --- |
| Multidisciplinar | não STEM | 15.777 / 10.176 | 3 / 3 | 48,36% | Área de avaliação interdisciplinar, sem disciplina; o conteúdo não pode ser verificado. |
| Medicina Veterinária | não STEM | 3.762 / 1.960 | 3.336 / 1.719 | 46,59% | Na COD, veterinários são profissionais da saúde (`2250`), que a Evellyn exclui. No CNPq, a área fica em Ciências Agrárias. |
| Ciências Ambientais | não STEM | 2.528 / 1.962 | 1.522 / 968 | 45,88% | Equivalente à proteção do meio ambiente (`2133`), que a Evellyn exclui. Engenharia Sanitária continua STEM, como os engenheiros de meio ambiente (`2143`). |
| Meio Ambiente e Sustentabilidade | não STEM | 0 / 0 | 1 / 4 | 45,46% | Segue Ciências Ambientais. |
| Tecnologias para o Desenvolvimento Sustentável | não STEM | 0 / 0 | 1 / 0 | 45,46% | Segue Ciências Ambientais. |
| Ciências | não STEM | 209 / 125 | 2 / 0 | 45,51% | Nome genérico, que pode ser ensino de ciências. |
| Biomedicina | não STEM | 11 / 8 | 1 / 0 | 45,46% | No Brasil é profissão de saúde. |
| Segurança Contra Incêndio | não STEM | 0 / 9 | 39 / 74 | 45,45% | Pode ser segurança e defesa civil, sem correspondência na lista. |
| Tecnologia e Inovação | não STEM | 0 / 1 | 5 / 5 | 45,45% | Nome genérico, que pode ser gestão da inovação. |
| Engenharia Cartografica | STEM | 0 / 0 | 0 / 1 | 45,46% | É engenharia no Brasil, embora na COD cartógrafos fiquem em `2165`, fora da lista. |
| **Demografia** | **pendente** | 148 / 102 | 59 / 43 | 45,49% | Depende de onde a COD põe o demógrafo (ver seção 3). Hoje fica fora. |

Os três casos com volume relevante são Multidisciplinar, Medicina Veterinária e Ciências Ambientais. Só Multidisciplinar muda o resultado em mais de 1 ponto, e ela não pode ser classificada pelo conteúdo.

### 2.2 Regra para área "Não informado"

Usa-se a Grande Área só quando todas as suas áreas têm a mesma classificação. Com as decisões acima, as grandes áreas **uniformes STEM** são Ciências Exatas e da Terra, Ciências Biológicas e Engenharias. As **uniformes não STEM** são Ciências Humanas, Ciências da Saúde e Lingüística, Letras e Artes (além de "Serviço Social", que aparece como grande área em 1 registro de atuação). As **mistas** são Ciências Agrárias (por causa de Medicina Veterinária), Ciências Sociais Aplicadas (por causa de Demografia), Outra e Tecnologias.

| Tratamento | Formação | Atuação |
| --- | --- | --- |
| Entra: grande área uniforme STEM | 1.199 | 284 |
| Fora: grande área uniforme não STEM | 1.827 | 415 |
| Fora: grande área mista | 4.242 | 203 |
| Fora: grande área também "Não informado" | 23.634 | 74.579 |

Se Demografia for decidida como não STEM, Ciências Sociais Aplicadas passa a ser uniforme não STEM, e isso não muda quem entra.

---

## 3. Correspondência com a COD

A estrutura da COD foi conferida no arquivo público `Estrutura_Ocupacao_COD.xls` da documentação da PNADC Contínua (IBGE), o mesmo citado pela Evellyn. Correspondência das áreas STEM:

| Código COD | Áreas do Lattes |
| --- | --- |
| `2111` | Astronomia, Física |
| `2112; 2114` | Geociências |
| `2113` | Química, Química Industrial |
| `2113; 2146` | Nanotecnologia e Novos Materiais |
| `2114` | Oceanografia |
| `2120` | Ciências Atuarias, Matemática, Probabilidade e Estatística |
| `2131` | Biofísica, Biologia Geral, Bioquímica, Biotecnologia, Botânica, Ecologia, Farmacologia, Fisiologia, Genética, Imunologia, Microbiologia, Morfologia, Parasitologia, Zoologia |
| `2132` | Agronomia, Recursos Florestais e Engenharia Florestal, Recursos Pesqueiros e Engenharia de Pesca, Zootecnia |
| `2132; 2145` | Ciência e Tecnologia de Alimentos |
| `2141` | Engenharia de Produção |
| `2142` | Engenharia Civil |
| `2142; ou 2164 (fora da lista)` | Engenharia de Transportes |
| `2143` | Engenharia Sanitária |
| `2144` | Engenharia Aeroespacial, Engenharia Mecânica, Engenharia Naval e Oceânica |
| `2144; 2152` | Engenharia Mecatrônica, Robótica, Mecatrônica e Automação |
| `2145` | Engenharia Química |
| `2146` | Engenharia de Materiais e Metalúrgica, Engenharia de Minas |
| `2149` | Engenharia Agrícola, Engenharia Biomédica, Engenharia Nuclear, Engenharia de Energia, Fontes Alternativas de Energia |
| `2151; 2152; 2153` | Engenharia Elétrica |
| `2152` | Microeletrônica |
| `2165 (fora da lista)` | Engenharia Cartografica |
| `2511 a 2529` | Ciência da Computação, Tecnologia da Informação e Comunicação |

**Códigos conferidos na COD:**
- `2250` Veterinários, no subgrupo `22` (profissionais da saúde);
- `2133` Profissionais da proteção do meio ambiente;
- `2165` Cartógrafos e agrimensores, no subgrupo `216` (arquitetos, urbanistas, agrimensores e desenhistas), que não está na lista da Evellyn.

**Achado novo:** o mesmo subgrupo `216` inclui `2164` (Urbanistas e engenheiros de trânsito). Engenharia de Transportes fica STEM, pela regra de que todas as engenharias entram e por coerência com a decisão de Engenharia Cartografica. Mas, na COD, engenheiros de trânsito ficam fora da lista da Evellyn. Vale confirmar com ela se o subgrupo `216` foi deixado de fora de propósito.

**Não confirmado:** o arquivo da COD só traz as denominações, sem notas de inclusão. `2120` chama-se "Matemáticos, atuários e estatísticos" e `2632` "Sociólogos, antropólogos e afins", e nenhum dos dois cita demógrafos. **Demografia continua pendente** até alguém ver as notas da COD ou o índice de ocupações.

Áreas não STEM ficam "sem correspondência na lista STEM" no CSV. A lista da Evellyn só define o que entra.

---

## 4. Não-aninhagem entre área e grande área

A mesma área aparece em mais de uma grande área com frequência, mas com poucas pessoas fora da grande área predominante:

| Lado | Pessoas fora da grande área predominante da sua área |
| --- | --- |
| Formação | 2.884 de 395.284 (0,73%) |
| Atuação | 84 de 350.705 (0,02%) |

Os maiores casos na formação são Biotecnologia em "Outra" (1.077 pessoas), Educação em Ciências Sociais Aplicadas (307), Ciências Ambientais em Ciências Agrárias (118) e Ciência da Computação em Engenharias (57). Como a definição alinhada classifica pela área, esses casos são tratados pelo conteúdo, qualquer que seja a grande área registrada. Pela V1, ao contrário, as 1.077 pessoas de Biotecnologia em "Outra" ficam fora do STEM, e as 57 de Ciência da Computação em Engenharias ficam dentro.

---

## 5. Impacto

### 5.1 Participação feminina

| Recorte | Período | STEM estrito (V1) | STEM alinhado |
| --- | --- | --- | --- |
| STEM formação | 2020 | 34,42% (2.810 / 8.163) | 44,53% (6.341 / 14.240) |
| STEM formação | 2021 | 33,74% (3.269 / 9.690) | 44,83% (7.420 / 16.553) |
| STEM formação | 2022 | 36,35% (3.964 / 10.906) | 46,94% (9.039 / 19.257) |
| STEM formação | 2023 | 35,03% (4.233 / 12.085) | 45,58% (9.724 / 21.334) |
| STEM formação | 2024 | 33,80% (3.873 / 11.459) | 45,39% (9.331 / 20.558) |
| STEM formação | 2025 | 34,47% (3.696 / 10.723) | 45,13% (8.724 / 19.330) |
| **STEM formação** | **2020 a 2025** | **34,66%** (21.845 / 63.026) | **45,46%** (50.579 / 111.272) |
| **STEM atuação** (situação em out/2026) | **2020 a 2025** | **35,02%** (22.823 / 65.164) | **44,69%** (49.164 / 110.001) |

A troca aumenta o recorte em cerca de três quartos e a participação feminina em 10,80 pontos na formação e 9,67 na atuação. A diferença é estável entre os anos, então a definição muda o nível do indicador, não a tendência.

### 5.2 Quem entra e quem sai

| Lado | Movimento | Pessoas | Mulheres |
| --- | --- | --- | --- |
| Formação | Entram | 48.361 | 28.795 |
| Formação | Saem | 115 | 61 |
| Atuação | Entram | 44.843 | 26.343 |
| Atuação | Saem | 6 | 2 |

Quase ninguém sai: só as poucas pessoas com área não STEM registradas numa grande área STEM (por exemplo, Educação em Engenharias). A diferença vem de quem entra.

**Áreas que mais explicam a diferença.** A contribuição de cada área é o quanto ela desloca a participação feminina em relação à V1; a soma de todas é a diferença total, a menos de arredondamento.

| Formação | Pessoas | % feminino | Contribuição |
| --- | --- | --- | --- |
| Agronomia | 10.857 | 53,05% | +1,79 ponto |
| Ciência e Tecnologia de Alimentos | 3.343 | 74,69% | +1,20 ponto |
| Biologia Geral | 4.314 | 64,63% | +1,16 ponto |
| Ecologia | 3.988 | 59,38% | +0,89 ponto |
| Biotecnologia | 2.782 | 60,46% | +0,65 ponto |

| Atuação | Pessoas | % feminino | Contribuição |
| --- | --- | --- | --- |
| Biologia Geral | 5.625 | 67,09% | +1,64 ponto |
| Agronomia | 7.687 | 47,96% | +0,90 ponto |
| Ciência e Tecnologia de Alimentos | 2.549 | 73,44% | +0,89 ponto |
| Microbiologia | 2.493 | 68,95% | +0,77 ponto |
| Ecologia | 3.333 | 58,39% | +0,71 ponto |

Agronomia não é majoritariamente feminina, mas pesa pelo volume: tem 53,05% de mulheres, bem acima dos 34,66% da V1, e é a maior área que entra.

### 5.3 Participação feminina por grande área, dentro da definição alinhada

| Grande área | Formação | Atuação |
| --- | --- | --- |
| Ciências Exatas e da Terra | 34,07% (10.262 / 30.121) | 36,34% (13.884 / 38.203) |
| Engenharias | 35,14% (11.522 / 32.790) | 33,16% (8.937 / 26.955) |
| Ciências Biológicas | 62,08% (16.018 / 25.803) | 62,76% (17.613 / 28.062) |
| Ciências Agrárias | 56,68% (12.037 / 21.237) | 53,84% (8.601 / 15.976) |
| Outra | 56,95% (684 / 1.201) | 15,54% (119 / 766) |
| Tecnologias | 1 pessoa (flag) | 16,67% (5 / 30) |
| Demais grandes áreas (registros de áreas STEM fora da grande área predominante) | 119 pessoas | 9 pessoas (flag) |

Exatas e Engenharias continuam perto dos 35% da V1. A diferença vem inteira das Ciências Biológicas e Agrárias, majoritariamente femininas. Em "Outra", formação e atuação divergem: na formação, o grupo é dominado por Biotecnologia; na atuação, por Robótica, Mecatrônica e Automação e por Microeletrônica, majoritariamente masculinas.

### 5.4 Composição racial das mulheres (agregado 2020 a 2025)

| Raça | Formação V1 | Formação alinhada | Atuação V1 | Atuação alinhada |
| --- | --- | --- | --- | --- |
| Branca | 63,23% | 61,25% | 62,54% | 60,89% |
| Parda | 28,10% | 29,70% | 28,77% | 29,77% |
| Preta | 6,45% | 7,03% | 6,67% | 7,37% |
| Amarela | 1,93% | 1,76% | 1,75% | 1,68% |
| Indígena | 0,29% | 0,26% | 0,27% | 0,29% |
| Negra (Preta + Parda) | 34,55% | 36,73% | 35,44% | 37,14% |
| Mulheres com raça declarada | 20.600 | 47.686 | 21.613 | 46.408 |
| Não declaração de raça (mulheres) | 5,70% | 5,72% | 5,30% | 5,61% |

A definição alinhada aumenta um pouco a participação de mulheres negras (cerca de 2 pontos). A não declaração quase não muda. Com o recorte maior, os valores anuais da definição alinhada não têm nenhuma flag de amostra pequena. Na V1, os valores de Indígena em STEM formação de 2020, 2021 e 2022 têm flag (denominador e numerador pequenos).

---

## 6. Sugestão: publicar as duas definições, se não houver consenso

As duas definições respondem perguntas diferentes:
- **STEM estrito** (V1): ciências exatas e engenharias, a leitura mais comum de STEM em estudos de gênero. É comparável com a V1 já publicada.
- **STEM alinhado**: o mesmo critério das ocupações da PNADC, comparável entre as fontes do observatório.

Se não houver consenso, a proposta é publicar as duas, com nomes distintos e a definição sempre ao lado do número, nunca misturadas no mesmo gráfico. No pipeline, isso viraria uma V2: novos recortes (por exemplo `stem_estrito_formacao` e `stem_alinhado_formacao`), com a classificação lida de `data/referencias/stem_areas_lattes.csv`.

---

## 7. Para decidir na reunião

1. **Adotar a definição alinhada** como definição do observatório, manter a da V1 ou publicar as duas (seção 6).
2. **Demografia:** STEM ou não, depois de conferir onde a COD põe o demógrafo (`2120` ou `2632`).
3. **Subgrupo `216` da COD** (arquitetos, urbanistas, engenheiros de trânsito, cartógrafos): confirmar com a Evellyn se ficou fora de propósito. Isso afeta Engenharia de Transportes e Engenharia Cartografica, hoje STEM aqui.
4. **As três decisões de maior volume** (Multidisciplinar, Medicina Veterinária, Ciências Ambientais), já tomadas como não STEM: confirmar com a Evellyn, porque Medicina Veterinária e Ciências Ambientais seguem a COD e não o CNPq.

---

## 8. Como reproduzir

```powershell
python scripts/consolidar_lattes.py          # se o consolidado não existir
python scripts/analisar_definicao_stem.py    # tabelas em data/processed/analise_stem/
python scripts/gerar_dicionario_stem.py      # regenera o documento do Notion a partir do CSV
pytest tests/test_stem_alinhado.py
pytest tests/test_stem_alinhado.py -m dados
```
