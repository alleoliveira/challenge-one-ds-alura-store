# 📘 **Alura Store: Uma Análise Completa para Tomada de Decisão**

## 🏪 **Introdução**

Seu João, proprietário da rede fictícia **Alura Store**, está prestes a realizar uma mudança importante: vender uma de suas quatro lojas para investir em um novo empreendimento. Porém, antes de tomar essa decisão, ele precisa enxergar com clareza qual loja apresenta **menor eficiência**, considerando fatores como faturamento, avaliações, categorias vendidas, frete e até padrões geográficos.

Este projeto foi desenvolvido como parte do **Challenge de Data Science (Oracle One + Alura)**, aplicando técnicas reais de análise de dados para resolver um problema de negócio.  
A seguir, você acompanha a jornada — tanto técnica quanto estratégica — que guiou a recomendação final.

---

# 🎯 **Objetivo do Projeto**

Realizar uma análise exploratória de dados (EDA) sobre as quatro lojas da Alura Store com o propósito de:

- Identificar padrões de vendas e desempenho
- Comparar as lojas em múltiplas métricas
- Destacar pontos fortes e fracos de cada unidade
- Recomendar, com base em evidências, **qual loja deve ser vendida**

---

# 🧰 **Tecnologias e Ferramentas Utilizadas**

- **Python 3.13.5**
- **Pandas** — Manipulação e limpeza de dados
- **Matplotlib** — Visualizações estáticas
- **NumPy** — Suporte matemático e vetorial
- Estrutura modular de funções para ETL e análises


---

# 🔍 **Metodologia da Análise**

A seguir, apresento cada etapa da exploração de dados, explicando tanto o raciocínio de negócio quanto a abordagem técnica.

---

## 1. 🔧 **Carregamento e Pré-Processamento**

### Processos automatizados incluídos no código:

- Leitura dos 4 CSVs diretamente do GitHub
- Conversão das datas com validação (`pd.to_datetime`)
- Tratamento de nulos e conversão de tipos
- Empilhamento das lojas com `pd.concat` usando MultiIndex

![PREVIEW DOS DADOS](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/01_preview_dados.png?raw=true "PREVIEW DOS DADOS")

---

## 2. 💰 **Análise de Faturamento**

A análise de vendas gerou:

- Faturamento total por loja
- Vendas anuais
- Vendas mensais consolidadas por período
- Comparativos entre todas as lojas

Métodos aplicados:

- `groupby()` por ano e período (`to_period("M")`)
- Gráficos de linha e barra (Matplotlib)
- Anotações automáticas nos gráficos usando `ax.text()`

![COMPARATIVO VENDAS ANUAIS - TODAS LOJAS](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/02_comparativo_vendas_anuais_todas_lojas.png?raw=true "COMPARATIVO VENDAS ANUAIS - TODAS LOJAS")

![COMPARATIVO VENDAS MENSAIS - TODAS LOJAS](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/03_comparativo_vendas_mensais_todas_lojas.png?raw=true "COMPARATIVO VENDAS MENSAIS - TODAS LOJAS")

![COMPARATIVO VENDAS MENSAIS - TODAS LOJAS (COM MÉDIA)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/03_comparativo_vendas_mensais_todas_lojas_com_media.png?raw=true "COMPARATIVO VENDAS MENSAIS - TODAS LOJAS (COM MÉDIA")


---

## 3. 🏷️ **Categorias de Produto**

O script analisa:

- Total vendido por categoria
- Evolução das categorias ao longo dos anos
- Comparações entre lojas
- Identificação das categorias mais fortes e mais fracas

Ferramentas utilizadas:

- `groupby(["Categoria do Produto"])`
- Visualizações:
    - Barras horizontais
    - Barras agrupadas por ano
    - Linhas para identificar a movimentação das categorias ao decorrer dos anos

![COMPARATIVO DE VENDAS POR CATEGORIA E LOJA](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_categoria_todas_lojas.png?raw=true "COMPARATIVO DE VENDAS POR CATEGORIA E LOJA")

![COMPARATIVO VENDAS ELETRÔNICOS (TODAS LOJAS)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_eletronicos_todas_lojas.png?raw=true "COMPARATIVO VENDAS ELETRÔNICOS (TODAS LOJAS)")

![COMPARATIVO VENDAS ELETRODOMÉSTICOS (TODAS LOJAS)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_eletrodomesticos_todas_lojas.png?raw=true "COMPARATIVO VENDAS ELETRODOMÉSTICOS (TODAS LOJAS)")

![COMPARATIVO VENDAS MÓVEIS (TODAS LOJAS)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_moveis_todas_lojas.png?raw=true "COMPARATIVO VENDAS MÓVEIS (TODAS LOJAS)")

![COMPARATIVO VENDAS INSTRUMENTOS MUSICAIS (TODAS LOJAS)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_instr_musicais_todas_lojas.png?raw=true "COMPARATIVO VENDAS INSTRUMENTOS MUSICAIS (TODAS LOJAS)")

---

## 4. ⭐ **Avaliação das Lojas e Produtos**

KPI extraídos:

- Média geral de avaliação por loja

Visualizações sugeridas:

- Barras verticais com anotações

![MÉDIA DE AVALIAÇÃO GERAL DE TODAS LOJAS](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/05_media_avaliacao_geral_todas_lojas.png?raw=true "MÉDIA DE AVALIAÇÃO GERAL DE TODAS LOJAS")



---

## 5. 🚚 **Frete Médio por Loja**

Aqui avaliamos:

- Custo médio de frete por loja
- Impacto logístico no resultado
- Comparação direta entre unidades

Ferramentas:

- `groupby()`
- Barras verticais com valores formatados em R$

![COMPARATIVO DE CUSTO MÉDIO DO FRETE DE TODAS AS LOJAS](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/07_frete_medio_todas_lojas.png?raw=true "COMPARATIVO DE CUSTO MÉDIO DO FRETE DE TODAS AS LOJAS")

---

## 6. 🌍 **Análise Geográfica (Scatter Plot)**

Embora as coordenadas sejam simuladas quando ausentes, a análise demonstra:

- Densidade de pedidos
- Concentração de vendas por região
- Comparação visual entre filiais
- Representação percentual por tamanho dos pontos no scatter plot

![DISTRIBUIÇÃO GEOGRÁFICA (DADOS)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/06_distribuicao_geografica_dados.jpg?raw=true "DISTRIBUIÇÃO GEOGRÁFICA (DADOS)")

![DISTRIBUIÇÃO GEOGRÁFICA (GRÁFICO DE DISPERSÃO)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/06_distribuicao_geografica_grafico.png?raw=true "DISTRIBUIÇÃO GEOGRÁFICA (GRÁFICO DE DISPERSÃO)")


---

# 🧾 **Recomendação Final**

Após consolidar todos os indicadores — faturamento, avaliações, categorias, frete, produtos e geolocalização — conclui-se que a loja com performance mais fraca e, portanto, **a mais indicada para venda** é:

---

# 🔥 **➡️ Loja 4 - Recomendação de Venda

### Justificativa :

A partir da consolidação de todos os indicadores analisados, a **Loja 4** se destaca de forma consistente como a unidade com **menor desempenho global**. Ao observarmos a série histórica de faturamento, percebemos que essa loja ficou abaixo das demais em **três dos quatro anos avaliados**, revelando um padrão persistente de baixa performance. Essa tendência também se confirma na análise mensal: em **26 dos 38 meses analisados**, suas vendas ficaram abaixo da média geral das lojas, reforçando a falta de tração comercial ao longo do tempo.

Ao aprofundar a investigação por categorias — principal motor de receita da Alura Store — a situação se torna ainda mais clara. Entre as quatro categorias mais relevantes (Eletrônicos, Eletrodomésticos, Móveis e Instrumentos Musicais), a Loja 4 apresentou desempenho significativamente inferior em quase todas elas. A **única exceção foi a categoria de Móveis**, onde conseguiu acompanhar o ritmo das demais; porém, sua fraqueza nas outras linhas críticas impede que esse ponto isolado compense a defasagem geral.

Outros indicadores operacionais, como **avaliação média**, **custo de frete** e **distribuição geográfica de pedidos**, foram avaliados cuidadosamente. Entretanto, como esses fatores **não apresentaram discrepâncias significativas entre as lojas**, eles não foram decisivos para a escolha final. Isso reforça ainda mais que o problema da Loja 4 não é pontual nem operacional — é estruturalmente ligado ao seu **baixo poder de conversão e volume de vendas**.

>Dessa forma, considerando o desempenho historicamente inferior, a consistência do baixo faturamento, o enfraquecimento nas principais categorias e a falta de indicadores compensatórios, a **Loja 4 se apresenta como a opção mais estratégica para desinvestimento**. Essa decisão permite que seu João direcione recursos para unidades mais robustas ou para o novo empreendimento com maior segurança e potencial de retorno.


---

# 🚀 **Como Executar o Projeto**

1. Clone o repositório:
    
    `git clone https://github.com/alleoliveira/challenge-one-ds-alura-store.git`
    
2. Instale as dependências:
    
    `pip install pandas matplotlib numpy`
    
3. Execute o script principal:
    
    `python challenge_alura_store.py`

---

# 👤 **Autor**

**Alexandre Oliveira**  
Desenvolvedor em formação em Ciência de Dados, com foco em análises claras, narrativas significativas e soluções guiadas por evidências.