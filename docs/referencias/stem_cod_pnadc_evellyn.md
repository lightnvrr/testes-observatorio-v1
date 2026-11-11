# PNADC - Dicionário de ocupações STEM

No PNADC a ocupação é mapeada a partir do Classificação de Ocupações para Pesquisas Domiciliares (COD). Para o observatório de dados é necessário definir quais códigos serão considerados STEM. Este documento se propõe a fazer isso.

## 1. Contexto

A COD possui 4 níveis hierárquicos (Grande Grupo, Subgrupo principal, Subgrupo e grupo de base). Destes, os únicos Subgrupos Principais cujo conteúdo é STEM por definição são:

| Código | Nome |
| --- | --- |
| 21 | Profissionais das Ciências e da Engenharia |
| 25 | Profissionais de Tecnologias da Informação e Comunicações |
| 31 | Profissionais de Nível Médio das Ciências e da Engenharia |
| 35 | Técnicos de Nível Médio da Tecnologia da Informação e das Comunicações |

Dessa forma, ficaram de fora por não serem STEM: Saúde, Ensino, Administração, Direito/Ciências Sociais, Saúde nível médio, operações financeiras/administrativas, Serviços jurídicos/sociais.

Para a classificação do que é STEM será usado apenas o Grupo de Base, pois ele corresponde a forma mais especificada das áreas. Além disso, há dois subgrupos que englobam áreas que não são consideradas STEM:

| Subgrupo (3 dígitos) | Mistura | Problema |
| --- | --- | --- |
| `213` — Profissionais em ciências biológicas | `2131` Biólogos + `2132` Agrônomos (manter) **e** `2133` Profissionais da proteção do meio ambiente (excluir) | Os três dividem o mesmo código de subgrupo |
| `352` — Técnicos em telecomunicações e radiodifusão | `3522` Técnicos de engenharia de telecomunicações (manter) **e** `3521` Técnicos de radiodifusão e gravação audiovisual (excluir) | Os dois dividem o mesmo código de subgrupo |

## 2. Lista proposta

Essa lista conta com 43 códigos de ocupações.

### 2.1 Ciências Físicas, químicas, geociências e astronomia

| Código | Denominação |
| --- | --- |
| 2111 | Físicos e astrônomos |
| 2112 | Meteorologistas |
| 2113 | Químicos |
| 2114 | Geólogos e geofísicos |

### 2.2 Matemática e estatística

| Código | Denominação |
| --- | --- |
| 2120 | Matemáticos, atuários e estatísticos |

### 2.3 Ciências biológicas e agrárias

| Código | Denominação |
| --- | --- |
| 2131 | Biólogos, botânicos, zoólogos e afins |
| 2132 | Agrônomos e afins |

### 2.4 Engenharias

| Código | Denominação |
| --- | --- |
| 2141 | Engenheiros industriais e de produção |
| 2142 | Engenheiros civis |
| 2143 | Engenheiros de meio ambiente |
| 2144 | Engenheiros mecânicos |
| 2145 | Engenheiros químicos |
| 2146 | Engenheiros de minas, metalúrgicos e afins |
| 2149 | Engenheiros não classificados anteriormente |
| 2151 | Engenheiros eletricistas |
| 2152 | Engenheiros eletrônicos |
| 2153 | Engenheiros em telecomunicações |

### 2.5 Tecnologia da Informação (nível superior)

| Código | Denominação |
| --- | --- |
| 2511 | Analistas de sistemas |
| 2512 | Desenvolvedores de programas e aplicativos (software) |
| 2513 | Desenvolvedores de páginas de internet (web) e multimídia |
| 2514 | Programadores de aplicações |
| 2519 | Desenvolvedores e analistas de programas e aplicativos não classificados anteriormente |
| 2521 | Desenhistas e administradores de bases de dados |
| 2522 | Administradores de sistemas |
| 2523 | Profissionais em rede de computadores |
| 2529 | Especialistas em base de dados e em redes de computadores não classificados anteriormente |

### 2.6 Técnicos de nível médio — ciências e engenharia

| Código | Denominação |
| --- | --- |
| 3111 | Técnicos em ciências físicas e químicas |
| 3112 | Técnicos em engenharia civil |
| 3113 | Eletrotécnicos |
| 3114 | Técnicos em eletrônica |
| 3115 | Técnicos em engenharia mecânica |
| 3116 | Técnicos em química industrial |
| 3117 | Técnicos em engenharia de minas e metalurgia |
| 3118 | Desenhistas e projetistas técnicos |
| 3119 | Técnicos em ciências físicas e da engenharia não classificados anteriormente |
| 3141 | Técnicos e profissionais de nível médio em ciências biológicas |
| 3142 | Técnicos agropecuários |
| 3143 | Técnicos florestais |

### 2.7 Técnicos de nível médio — TIC

| Código | Denominação |
| --- | --- |
| 3511 | Técnicos em operações de TIC |
| 3512 | Técnicos em assistência ao usuário de TIC |
| 3513 | Técnicos de redes e sistemas de computadores |
| 3514 | Técnicos da web |
| 3522 | Técnicos de engenharia de telecomunicações |

## 3. Link de acesso à fonte

| Recurso | Origem |
| --- | --- |
| Estrutura da COD (Classificação de Ocupações para Pesquisas Domiciliares) | Arquivo `Estrutura_Ocupacao_COD.xls`, fornecido pelo IBGE junto ao dicionário da PNADC |