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

> Arquivo principal: `challenge_alura_store.py`


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

![COMPARATIVO DE VENDAS POR CATEGORIA E LOJA](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_categoria_todas_lojas.png?raw=true "COMPARATIVO DE VENDAS POR CATEGORIA E LOJA")

![COMPARATIVO VENDAS ELETRÔNICOS (TODAS LOJAS)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_eletronicos_todas_lojas.png?raw=true "COMPARATIVO VENDAS ELETRÔNICOS (TODAS LOJAS)")

![COMPARATIVO VENDAS ELETRODOMÉSTICOS (TODAS LOJAS)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_eletrodomesticos_todas_lojas.png?raw=true "COMPARATIVO VENDAS ELETRODOMÉSTICOS (TODAS LOJAS)")

![COMPARATIVO VENDAS MÓVEIS (TODAS LOJAS)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_moveis_todas_lojas.png?raw=true "COMPARATIVO VENDAS MÓVEIS (TODAS LOJAS)")

![COMPARATIVO VENDAS INSTRUMENTOS MUSICAIS (TODAS LOJAS)](https://github.com/alleoliveira/challenge-one-ds-alura-store/blob/main/images/04_comparativo_vendas_instr_musicais_todas_lojas.png?raw=true "COMPARATIVO VENDAS INSTRUMENTOS MUSICAIS (TODAS LOJAS)")

---

## 4. ⭐ **Avaliação das Lojas e Produtos**

KPIs extraídos:

- Média geral de avaliação por loja
- Avaliação por categoria
- Rankings
- Comparações estruturadas usando `unstack()`

Visualizações sugeridas:

- Barras verticais com anotações
- Agrupamentos por loja e categoria

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

# 🔥 **➡️ Loja X (substituir pela sua análise final)**

### Justificativa (modelo):

- **Faturamento inferior** e evolução mensal inconsistente
- **Avaliação média abaixo da concorrência**
- **Volume menor nas categorias líderes**
- **Maior custo médio de frete**, reduzindo margem
- **Baixa densidade geográfica de pedidos**, sugerindo alcance limitado
- **Portfólio de produtos com menor diversidade e alta concentração em poucos itens**

> Com base no conjunto completo das análises, esta loja demonstra **menor eficiência operacional**, menor resiliência e menor potential de crescimento, sendo a melhor opção para desinvestimento.

---

# 🚀 **Como Executar o Projeto**

1. Clone o repositório:
    
    `git clone https://github.com/seuusuario/alura-store-analysis.git`
    
2. Instale as dependências:
    
    `pip install pandas matplotlib numpy`
    
3. Execute o script principal:
    
    `python challenge_alura_store.py`

---

# 👤 **Autor**

**Alexandre Oliveira**  
Desenvolvedor em formação em Ciência de Dados, com foco em análises claras, narrativas significativas e soluções guiadas por evidências.