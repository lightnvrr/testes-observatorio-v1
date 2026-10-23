# Lattes: dicionário de áreas STEM

No Lattes, a área de formação e a de atuação são registradas pela Tabela de Áreas do Conhecimento do CNPq. Para o observatório de dados é necessário definir quais áreas serão consideradas STEM. Este documento se propõe a fazer isso, seguindo o mesmo critério usado para as ocupações da PNADC.

## 1. Contexto

A Tabela de Áreas do Conhecimento possui 4 níveis hierárquicos (Grande Área, Área, Subárea e Especialidade). A base Lattes traz só os dois primeiros. Das grandes áreas, as únicas cujo conteúdo é STEM por definição são:

| Código | Nome |
| --- | --- |
| `1.00.00.00-3` | Ciências Exatas e da Terra |
| `2.00.00.00-6` | Ciências Biológicas |
| `3.00.00.00-9` | Engenharias |

Dessa forma, ficaram de fora por não serem STEM: **Ciências da Saúde**, **Ciências Humanas** e **Lingüística, Letras e Artes**.

Para a classificação do que é STEM será usada apenas a Área, pois ela corresponde à forma mais especificada disponível na base. Além disso, há grandes áreas que englobam áreas STEM e não STEM:

| Grande área | Mistura | Problema |
| --- | --- | --- |
| `5.00.00.00-4` Ciências Agrárias | `Agronomia`, `Ciência e Tecnologia de Alimentos`, `Engenharia Agrícola`, `Recursos Florestais e Engenharia Florestal`, `Recursos Pesqueiros e Engenharia de Pesca` e `Zootecnia` (manter); `Medicina Veterinária` (excluir) | Na COD, veterinários ficam em profissionais da saúde (`2250`), fora do STEM. |
| `6.00.00.00-7` Ciências Sociais Aplicadas | `Demografia` (a decidir); `Administração`, `Arquitetura e Urbanismo`, `Ciência da Informação`, `Ciências Contábeis`, `Comunicação`, `Desenho Industrial`, `Direito`, `Economia`, `Economia Doméstica`, `Museologia`, `Planejamento Urbano e Regional`, `Serviço Social` e `Turismo` (excluir) | Na COD, demógrafos podem estar em `2120` (STEM) ou `2632` (não STEM); a confirmar. |
| `9.00.00.00-5` Outra | `Ciências Atuarias`, `Engenharia Cartografica`, `Engenharia Mecatrônica`, `Fontes Alternativas de Energia`, `Microeletrônica`, `Química Industrial` e `Robótica, Mecatrônica e Automação` (manter); `Administração Hospitalar`, `Administração Rural`, `Biomedicina`, `Bioética`, `Carreira Militar`, `Carreira Religiosa`, `Ciências`, `Ciências Ambientais`, `Ciências Sociais`, `Defesa`, `Divulgação Científica`, `Multidisciplinar`, `Relações Internacionais`, `Relações Públicas`, `Secretariado Executivo`, `Segurança Contra Incêndio` e `Tecnologia e Inovação` (excluir) | Grande área residual do CNPq, para áreas sem lugar na Árvore; mistura engenharias novas com áreas interdisciplinares. |
| Tecnologias (sem código) | `Nanotecnologia e Novos Materiais` e `Tecnologia da Informação e Comunicação` (manter); `Meio Ambiente e Sustentabilidade`, `Tecnologias Sociais e Educacionais` e `Tecnologias para o Desenvolvimento Sustentável` (excluir) | Não existe na Tabela de Áreas do Conhecimento; abarca sobretudo especialidades próximas das Engenharias. |

- **Área "Não informado":** usa-se a Grande Área só quando todas as suas áreas têm a mesma classificação; nas grandes áreas mistas, o registro fica fora.
- **Só mestres e doutores:** o Lattes não tem equivalente aos técnicos de nível médio da COD (subgrupos `31` e `35`).
- **Nomes das áreas:** estão exatamente como na base, inclusive sem acento quando a base não tem (ex.: `Engenharia Cartografica`).

## 2. Lista proposta

Essa lista conta com 51 áreas.

### 2.1 Ciências físicas, químicas, geociências e astronomia

| Código | Área |
| --- | --- |
| `1.04.00.00-1` | Astronomia |
| `1.05.00.00-6` | Física |
| `1.06.00.00-0` | Química |
| `1.07.00.00-5` | Geociências |
| `1.08.00.00-0` | Oceanografia |
| sem código | Nanotecnologia e Novos Materiais |
| sem código | Química Industrial |

### 2.2 Matemática e estatística

| Código | Área |
| --- | --- |
| `1.01.00.00-8` | Matemática |
| `1.02.00.00-2` | Probabilidade e Estatística |
| sem código | Ciências Atuarias |

### 2.3 Ciências biológicas e agrárias

| Código | Área |
| --- | --- |
| `2.01.00.00-0` | Biologia Geral |
| `2.02.00.00-5` | Genética |
| `2.03.00.00-0` | Botânica |
| `2.04.00.00-4` | Zoologia |
| `2.05.00.00-9` | Ecologia |
| `2.06.00.00-3` | Morfologia |
| `2.07.00.00-8` | Fisiologia |
| `2.08.00.00-2` | Bioquímica |
| `2.09.00.00-7` | Biofísica |
| `2.10.00.00-0` | Farmacologia |
| `2.11.00.00-4` | Imunologia |
| `2.12.00.00-9` | Microbiologia |
| `2.13.00.00-3` | Parasitologia |
| `2.14.00.00-8` | Biotecnologia |
| `5.01.00.00-9` | Agronomia |
| `5.02.00.00-3` | Recursos Florestais e Engenharia Florestal |
| `5.04.00.00-2` | Zootecnia |
| `5.06.00.00-1` | Recursos Pesqueiros e Engenharia de Pesca |
| `5.07.00.00-6` | Ciência e Tecnologia de Alimentos |

### 2.4 Engenharias

| Código | Área |
| --- | --- |
| `3.01.00.00-3` | Engenharia Civil |
| `3.02.00.00-8` | Engenharia de Minas |
| `3.03.00.00-2` | Engenharia de Materiais e Metalúrgica |
| `3.04.00.00-7` | Engenharia Elétrica |
| `3.05.00.00-1` | Engenharia Mecânica |
| `3.06.00.00-6` | Engenharia Química |
| `3.07.00.00-0` | Engenharia Sanitária |
| `3.08.00.00-5` | Engenharia de Produção |
| `3.09.00.00-0` | Engenharia Nuclear |
| `3.10.00.00-2` | Engenharia de Transportes |
| `3.11.00.00-7` | Engenharia Naval e Oceânica |
| `3.12.00.00-1` | Engenharia Aeroespacial |
| `3.13.00.00-6` | Engenharia Biomédica |
| `3.14.00.00-0` | Engenharia de Energia |
| `5.03.00.00-8` | Engenharia Agrícola |
| `9.32.00.00-5` | Robótica, Mecatrônica e Automação |
| `9.33.00.00-0` | Microeletrônica |
| sem código | Engenharia Cartografica |
| sem código | Engenharia Mecatrônica |
| sem código | Fontes Alternativas de Energia |

### 2.5 Computação e tecnologia da informação

| Código | Área |
| --- | --- |
| `1.03.00.00-7` | Ciência da Computação |
| sem código | Tecnologia da Informação e Comunicação |

## 3. Link de acesso à fonte

| Recurso | Origem |
| --- | --- |
| Painel de Formação e Atuação do Lattes (CNPq) | [http://bi.cnpq.br/painel/formacao-atuacao-lattes/](http://bi.cnpq.br/painel/formacao-atuacao-lattes/) |
| Tabela de Áreas do Conhecimento (CNPq, relatório de 30/06/2025) | [TabeladeAreasdoConhecimento.pdf](http://lattes.cnpq.br/documents/11871/24930/TabeladeAreasdoConhecimento.pdf/d192ff6b-3e0a-4074-a74d-c280521bd5f7) |
| Dicionário de ocupações STEM da PNADC | Documento "PNADC: Dicionário de ocupações STEM", da equipe do observatório |
