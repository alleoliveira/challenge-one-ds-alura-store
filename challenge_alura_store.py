# -*- coding: utf-8 -*-
"""
Projeto de Análise de Vendas - Alura Store (Challenge Data Science)

Este script realiza uma análise exploratória completa, incluindo KPIs financeiros,
análise temporal e análise geográfica (Latitude/Longitude).

Funcionalidades:
- ETL e Limpeza de Dados (Datas, Nulos).
- Relatórios Financeiros (Vendas, Frete).
- Visualização Temporal e Categórica.
- Visualização Geográfica (Mapa de Dispersão de Clientes).

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuração de estilo
plt.style.use('ggplot') 

# ==============================================================================
# 1. FUNÇÕES DE SUPORTE E TRATAMENTO DE DADOS
# ==============================================================================

def verificar_e_converter_datas(df, nome_loja, coluna="Data da Compra"):
    """
    Limpa a coluna de data, força formato %d/%m/%Y e trata erros.
    """
    print("-" * 80)
    print(f"VERIFICADOR DE DATAS - {nome_loja}")
    print("-" * 80)

    serie_raw = df[coluna].astype(str).str.strip()

    try:
        datas = pd.to_datetime(serie_raw, format="%d/%m/%Y", errors="raise")
        print("Todas as datas foram convertidas com sucesso para datetime (%d/%m/%Y).\n")
        return datas
    except Exception as e:
        print("ERRO AO CONVERTER ALGUMAS DATAS. Tentando recuperação...")
        datas_coerce = pd.to_datetime(serie_raw, format="%d/%m/%Y", errors="coerce")
        if datas_coerce.isna().any():
            print(f"Aviso: {datas_coerce.isna().sum()} datas inválidas encontradas (transformadas em NaT).")
        return datas_coerce

def gerar_lat_lon_simulado(n_rows):
    """
    Função AUXILIAR para simular dados de GPS caso não existam no CSV original.
    Gera coordenadas próximas ao Brasil (Lat -10 a -30, Lon -40 a -60).
    """
    lat = np.random.uniform(-30.0, -10.0, n_rows)
    lon = np.random.uniform(-60.0, -40.0, n_rows)
    return lat, lon

def carregar_dados():
    """
    Carrega os dados das 4 lojas e aplica o tratamento inicial.
    """
    urls = {
        "Loja 1": "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv",
        "Loja 2": "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv",
        "Loja 3": "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv",
        "Loja 4": "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv",
    }

    lojas = {}
    print(">>> Iniciando carregamento e verificação de dados...")
    for nome_loja, url in urls.items():
        try:
            df = pd.read_csv(url)
            
            # Tratamento de Data
            df["Data da Compra"] = verificar_e_converter_datas(df, nome_loja)
            
            # Tratamento de Colunas Numéricas
            if 'Avaliação da compra' not in df.columns: df['Avaliação da compra'] = 0.0
            if 'Frete' not in df.columns: df['Frete'] = 0.0
            
            # --- TRATAMENTO GEO (LAT/LON) ---
            # Verifica se as colunas 'lat' e 'lon' existem. Se não, cria dados fictícios
            # para que o gráfico de dispersão funcione no exemplo.
            if 'lat' not in df.columns or 'lon' not in df.columns:
                print(f"Aviso: Colunas de GPS ausentes em {nome_loja}. Gerando dados simulados para demonstração.")
                df['lat'], df['lon'] = gerar_lat_lon_simulado(len(df))
            else:
                # Garante que são numéricos (caso venham como string)
                df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
                df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
                
            lojas[nome_loja] = df
        except Exception as e:
            print(f"Erro crítico ao carregar {nome_loja}: {e}")
            
    return lojas

def combinar_lojas(dict_lojas):
    lista = [df for df in dict_lojas.values()]
    nomes = list(dict_lojas.keys())
    return pd.concat(lista, keys=nomes)

# ==============================================================================
# 2. FUNÇÕES DE RELATÓRIOS (ANÁLISES FINANCEIRAS E TEMPORAIS)
# ==============================================================================

def verificar_nulos(dict_lojas):
    print("\n" + "#" * 80)
    print("VERIFICAÇÃO DE DADOS NULOS (APÓS LIMPEZA E CONVERSÃO DE DATAS)")
    print("#" * 80)
    for nome_loja, df in dict_lojas.items():
        print("-" * 50)
        print(nome_loja)
        print("-" * 50)
        print(df.isnull().sum(), "\n")

def relatorio_vendas_por_loja(dict_lojas):
    for nome_loja, df in dict_lojas.items():
        print("=" * 50)
        print(f"RELATÓRIO DE VENDAS GERAL - {nome_loja}")
        print("=" * 50)

        total_vendas_loja = df["Preço"].sum()
        vendas_ano = df.groupby(df["Data da Compra"].dt.year)["Preço"].sum()
        vendas_mes_ano = df.groupby(df["Data da Compra"].dt.to_period("M"))["Preço"].sum()

        print("-" * 50)
        print("TOTAL DE VENDAS")
        print("-" * 50)
        print(f"R$ {total_vendas_loja:,.2f}")

        # TABELA DE DADOS: VENDAS ANUAIS
        print("\n" + "-" * 50)
        print(f"TABELA DE DADOS: VENDAS ANUAIS ({nome_loja})")
        print("-" * 50)
        print(vendas_ano.apply(lambda x: f"R$ {x:,.2f}"))

        # Gráfico anual
        plt.figure(figsize=(14, 5))
        ax1 = vendas_ano.plot(kind="line", marker="o", color="#1f77b4", linewidth=3)
        ax1.set_title(f"VENDAS ANUAIS - {nome_loja}", fontsize=20)
        ax1.set_xlabel("ANO", fontsize=12)
        ax1.set_ylabel("VENDAS (R$)", fontsize=12)
        ax1.grid(axis="y", linestyle="--")
        plt.xticks(vendas_ano.index)

        for x, y in zip(vendas_ano.index, vendas_ano.values):
            ax1.text(x, y + 100, f"R$ {y:,.2f}", ha="center")

        plt.tight_layout()
        plt.show()

        # TABELA DE DADOS: VENDAS MENSAIS
        print("\n" + "-" * 50)
        print(f"TABELA DE DADOS: VENDAS MENSAIS ({nome_loja})")
        print("-" * 50)
        print(vendas_mes_ano.apply(lambda x: f"R$ {x:,.2f}"))

        # Gráfico mês/ano
        plt.figure(figsize=(14, 5))
        # Ajuste para garantir plotagem temporal correta
        ax2 = vendas_mes_ano.to_timestamp().plot(kind="line", marker="o", color="#ff7f0e", linewidth=2)
        ax2.set_title(f"VENDAS MÊS/ANO - {nome_loja}", fontsize=20)
        ax2.set_xlabel("MÊS/ANO", fontsize=12)
        ax2.set_ylabel("VENDAS (R$)", fontsize=12)
        ax2.grid(axis="y", linestyle="--")
        
        # Rótulos ajustados para datetime
        for x_time, y_value in zip(vendas_mes_ano.to_timestamp().index, vendas_mes_ano.values):
            rotulo_data = x_time.strftime("%m/%Y")
            ax2.text(x_time, y_value + 300, rotulo_data,
                     ha="center", fontsize=10, color="darkorange", rotation=90)

        plt.tight_layout()
        plt.show()

def graficos_comparativos_vendas(dict_lojas):
    print("\n" + "=" * 80)
    print("DASHBOARD COMPARATIVO DE VENDAS")
    print("=" * 80)
    
    df_combinado = combinar_lojas(dict_lojas)

    # Comparação anual
    vendas_comparativas_ano = df_combinado.groupby(
        [df_combinado["Data da Compra"].dt.year,
         df_combinado.index.get_level_values(0)]
        )["Preço"].sum()

    df_comp_anual = vendas_comparativas_ano.unstack(level=1).fillna(0)

    # TABELA DE DADOS: COMPARATIVO ANUAL
    print("\n" + "-" * 50)
    print("TABELA DE DADOS: COMPARATIVO ANUAL POR LOJA")
    print("-" * 50)
    # Formata o DataFrame para exibição (aplica R$ em todas as células)
    print(df_comp_anual.applymap(lambda x: f"R$ {x:,.2f}"))

    plt.figure(figsize=(16, 8))
    ax_comp_ano = df_comp_anual.plot(kind="bar", rot=0, figsize=(16, 8), width=0.8, ax=plt.gca())

    ax_comp_ano.set_title("COMPARAÇÃO VENDAS ANUAIS - TODAS LOJAS", fontsize=20, pad=15)
    ax_comp_ano.set_xlabel("ANO", fontsize=12)
    ax_comp_ano.set_ylabel("VENDAS (R$)", fontsize=12)
    ax_comp_ano.legend(title="LOJA", fontsize=12)
    ax_comp_ano.grid(axis="y", linestyle="--")

    for p in ax_comp_ano.patches:
        ax_comp_ano.annotate(
            f"R$ {p.get_height():,.2f}",
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha="center", va="center", xytext=(0, 10),
            textcoords="offset points", fontsize=10
        )

    plt.tight_layout()
    plt.show()

    # Comparação mês/ano
    vendas_comparativas_mes_ano = df_combinado.groupby(
        [df_combinado["Data da Compra"].dt.to_period("M"),
         df_combinado.index.get_level_values(0)]
        )["Preço"].sum()

    df_comp_mes_ano = vendas_comparativas_mes_ano.unstack(level=1).fillna(0)
    
    # TABELA DE DADOS: COMPARATIVO MENSAL
    print("\n" + "-" * 50)
    print("TABELA DE DADOS: COMPARATIVO MENSAL POR LOJA")
    print("-" * 50)
    print(df_comp_mes_ano.applymap(lambda x: f"R$ {x:,.2f}"))

    df_comp_mes_ano.index = df_comp_mes_ano.index.to_timestamp()

    plt.figure(figsize=(16, 8))
    ax_comp_mes_ano = df_comp_mes_ano.plot(kind="line", marker="o", figsize=(16, 8), linewidth=2, ax=plt.gca())

    ax_comp_mes_ano.set_title("COMPARAÇÃO VENDAS MENSAIS - TODAS LOJAS", fontsize=20, pad=15)
    ax_comp_mes_ano.set_xlabel("MÊS/ANO", fontsize=12)
    ax_comp_mes_ano.set_ylabel("VENDAS (R$)", fontsize=12)
    ax_comp_mes_ano.legend(title="LOJA", fontsize=12)
    ax_comp_mes_ano.grid(axis="y", linestyle="--")

    plt.tight_layout()
    plt.show()

def relatorio_vendas_por_categoria(dict_lojas):
    print("\n" + "=" * 80)
    print("ANÁLISE DE VENDAS POR CATEGORIA")
    print("=" * 80)
    
    for nome_loja, df in dict_lojas.items():
        print("=" * 50)
        print(f"RELATÓRIO DE VENDAS POR CATEGORIA - {nome_loja}")
        print("=" * 50)

        total_vendas_categoria = (
            df.groupby("Categoria do Produto")["Preço"]
              .sum()
              .sort_values(ascending=False)
        )

        vendas_ano_categoria = df.groupby([
            df["Data da Compra"].dt.year.rename("Ano"),
            "Categoria do Produto"
            ])["Preço"].sum()

        vendas_ano_categoria = vendas_ano_categoria.sort_index(level="Ano", ascending=True)
        # Ajuste para garantir ordenação correta sem warning de level
        vendas_ano_categoria = vendas_ano_categoria.reset_index().sort_values(
            by=["Ano", "Preço"], ascending=[True, False]
            ).set_index(["Ano", "Categoria do Produto"])["Preço"]

        # TABELA DE DADOS: POR CATEGORIA
        print("-" * 50)
        print("TABELA DE DADOS: TOTAL POR CATEGORIA")
        print("-" * 50)
        print(total_vendas_categoria.apply(lambda x: f"R$ {x:,.2f}"))

        # Gráfico total por categoria
        plt.figure(figsize=(14, 5))
        ax1 = total_vendas_categoria.plot(kind="barh", color=plt.cm.Set2.colors[0],
                                          title=f"TOTAL VENDAS POR CATEGORIA - {nome_loja}")
        ax1.invert_yaxis()
        ax1.grid(axis="x", linestyle="--")
        plt.tight_layout()
        plt.show()

        # TABELA DE DADOS: POR CATEGORIA E ANO
        print("\n" + "-" * 50)
        print("TABELA DE DADOS: TOTAL POR CATEGORIA E ANO")
        print("-" * 50)
        print(vendas_ano_categoria.apply(lambda x: f"R$ {x:,.2f}"))
        print("\n")

        # Gráfico vendas anuais por categoria
        plt.figure(figsize=(14, 5))
        df_vendas_ano_cat = vendas_ano_categoria.unstack(level="Ano", fill_value=0)
        ax2 = df_vendas_ano_cat.plot(kind="bar", ax=plt.gca(), rot=0,
                                     title=f"VENDAS POR CATEGORIA/ANO - {nome_loja}")
        ax2.grid(axis="y", linestyle="--")
        plt.tight_layout()
        plt.show()

def graficos_categorias_comparativas(dict_lojas):
    print("\n" + "=" * 80)
    print("COMPARATIVO DE CATEGORIAS ENTRE LOJAS")
    print("=" * 80)
    
    df_combinado = combinar_lojas(dict_lojas)

    # Total por categoria e loja
    total_vendas_lojas_categoria = df_combinado.groupby(
        ["Categoria do Produto", df_combinado.index.get_level_values(0)]
    )["Preço"].sum()

    df_vendas_lojas_categoria = total_vendas_lojas_categoria.unstack(level=1).fillna(0)
    df_vendas_lojas_categoria["Total"] = df_vendas_lojas_categoria.sum(axis=1)
    df_vendas_lojas_categoria = df_vendas_lojas_categoria.sort_values(
        by="Total", ascending=True
        ).drop(columns=["Total"])

    # TABELA DE DADOS: CATEGORIA x LOJA
    print("\n" + "-" * 50)
    print("TABELA DE DADOS: CATEGORIA x LOJA")
    print("-" * 50)
    print(df_vendas_lojas_categoria.applymap(lambda x: f"R$ {x:,.2f}"))

    plt.figure(figsize=(14, 8))
    ax_categoria = df_vendas_lojas_categoria.plot(kind="bar", figsize=(14, 8), ax=plt.gca(),
                                                  title="COMPARAÇÃO DE VENDAS TOTAIS POR CATEGORIA E LOJA")
    ax_categoria.grid(axis="x", linestyle="--")
    plt.tight_layout()
    plt.show()

    # Gráficos por categoria ao longo dos anos (Loops de gráficos de linha)
    todas_categorias = df_combinado["Categoria do Produto"].dropna().unique()

    for categoria in todas_categorias:
        df_cat = df_combinado[df_combinado["Categoria do Produto"] == categoria].copy()
        vendas_cat_ano_loja = df_cat.groupby(
            [df_cat["Data da Compra"].dt.year,
             df_cat.index.get_level_values(0)]
            )["Preço"].sum()

        df_cat_comp = vendas_cat_ano_loja.unstack(level=1).fillna(0)

        # TABELA DE DADOS: CATEGORIA ESPECÍFICA AO LONGO DO TEMPO
        print("\n" + "-" * 50)
        print(f"TABELA DE DADOS: EVOLUÇÃO ANUAL - {categoria}")
        print("-" * 50)
        print(df_cat_comp.applymap(lambda x: f"R$ {x:,.2f}"))

        plt.figure(figsize=(12, 6))
        ax_categoria_ano = df_cat_comp.plot(kind="line", marker="o", figsize=(12, 6), ax=plt.gca())
        ax_categoria_ano.set_title(f"VENDAS ANUAIS DA CATEGORIA {categoria}", fontsize=20)
        ax_categoria_ano.set_xlabel("ANO", fontsize=12)
        ax_categoria_ano.set_ylabel("VENDAS (R$)", fontsize=12)
        ax_categoria_ano.legend(title="LOJA")
        ax_categoria_ano.grid(axis="y", linestyle="--")
        plt.xticks(df_cat_comp.index)
        plt.tight_layout()
        plt.show()

def avaliacao_por_categoria(dict_lojas):
    print("\n" + "#" * 80)
    print("ANÁLISE DE AVALIAÇÕES (NPS/CSAT)")
    print("#" * 80)
    for nome_loja, df in dict_lojas.items():
        print("=" * 80)
        print(f"RELATÓRIO DE AVALIAÇÕES POR CATEGORIA - {nome_loja}")
        print("=" * 80)
        media_cat = round(
            df.groupby("Categoria do Produto")["Avaliação da compra"].mean(), 2
            )
        print(f"MÉDIA DA AVALIAÇÃO POR CATEGORIA:\n{media_cat}\n")

def avaliacao_comparativa_categorias(dict_lojas):
    df_combinado = combinar_lojas(dict_lojas)

    media_avaliacao_loja_categoria = df_combinado.groupby(
        ["Categoria do Produto", df_combinado.index.get_level_values(0)]
        )["Avaliação da compra"].mean()

    df_avaliacao_lojas_categoria = media_avaliacao_loja_categoria.unstack(level=1).fillna(0)
    df_avaliacao_lojas_categoria["Média Máxima"] = df_avaliacao_lojas_categoria.max(axis=1)
    df_avaliacao_lojas_categoria = df_avaliacao_lojas_categoria.sort_values(
        by="Média Máxima", ascending=True
        ).drop(columns=["Média Máxima"])

    # TABELA DE DADOS: AVALIAÇÃO COMPARATIVA
    print("\n" + "-" * 50)
    print("TABELA DE DADOS: AVALIAÇÃO MÉDIA (CATEGORIA x LOJA)")
    print("-" * 50)
    print(df_avaliacao_lojas_categoria.round(2))

    plt.figure(figsize=(14, 8))
    ax = df_avaliacao_lojas_categoria.plot(kind="bar", figsize=(14, 8), ax=plt.gca(),
                                           title="COMPARAÇÃO DE AVALIAÇÕES POR CATEGORIA E LOJA")

    for p in ax.patches:
        valor_rotulo = f"{p.get_height():.2f}"
        ax.annotate(valor_rotulo,
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="center", xytext=(0, 10),
                    textcoords="offset points", fontsize=6)

    ax.grid(axis="y", linestyle="--")
    plt.tight_layout()
    plt.show()

def avaliacao_geral_por_loja(dict_lojas):
    df_combinado = combinar_lojas(dict_lojas)

    media_avaliacao_loja = df_combinado.groupby(
        df_combinado.index.get_level_values(0)
        )["Avaliação da compra"].mean().sort_values(ascending=False)

    print("\n" + "#" * 80)
    print("AVALIAÇÃO GERAL POR LOJA")
    print("#" * 80)
    
    # TABELA DE DADOS: AVALIAÇÃO GERAL
    print("-" * 50)
    print("TABELA DE DADOS: RANKING DE AVALIAÇÃO")
    print("-" * 50)
    for loja, media in media_avaliacao_loja.items():
        print(f"{loja}: {media:.2f}")

    plt.figure(figsize=(10, 6))
    ax = media_avaliacao_loja.plot(kind="bar", ax=plt.gca(), rot=0, color="teal",
                                   title="MÉDIA DE AVALIAÇÃO GERAL POR LOJA")

    for p in ax.patches:
        valor_rotulo = f"{p.get_height():.2f}"
        ax.annotate(valor_rotulo,
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="center", xytext=(0, 10),
                    textcoords="offset points", fontsize=8)

    ax.grid(axis="y", linestyle="--")
    plt.tight_layout()
    plt.show()

def produtos_mais_menos_vendidos(dict_lojas, top=10):
    print("\n" + "#" * 80)
    print("PRODUTOS MAIS E MENOS VENDIDOS (POR LOJA)")
    print("#" * 80)
    for nome_loja, df in dict_lojas.items():
        print("=" * 80)
        print(f"PRODUTOS MAIS E MENOS VENDIDOS - {nome_loja}")
        print("=" * 80)
        qtd_venda_produto = (
            df.groupby("Produto")["Produto"]
              .count()
              .sort_values(ascending=False)
            )
        print("TOP MAIS VENDIDOS:")
        print(qtd_venda_produto.head(top), "\n")
        print("TOP MENOS VENDIDOS:")
        print(qtd_venda_produto.tail(top), "\n")

def frete_medio_por_loja(dict_lojas):
    df_combinado = combinar_lojas(dict_lojas)

    media_custo_frete_loja = df_combinado.groupby(
        df_combinado.index.get_level_values(0)
        )["Frete"].mean().sort_values(ascending=False)

    print("\n" + "#" * 80)
    print("FRETE MÉDIO POR LOJA")
    print("#" * 80)
    
    # TABELA DE DADOS: FRETE
    print("-" * 50)
    print("TABELA DE DADOS: CUSTO MÉDIO DE FRETE")
    print("-" * 50)
    for nome_loja, df in dict_lojas.items():
        media = df["Frete"].mean()
        print(f"{nome_loja}: R$ {media:,.2f}")

    plt.figure(figsize=(10, 6))
    ax = media_custo_frete_loja.plot(kind="bar", ax=plt.gca(), rot=0, color="teal",
                                     title="MÉDIA DE CUSTO DE FRETE POR LOJA (R$)")

    for p in ax.patches:
        valor_rotulo = f"R$ {p.get_height():.2f}"
        ax.annotate(valor_rotulo,
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="center", xytext=(0, 10),
                    textcoords="offset points", fontsize=8)

    ax.grid(axis="y", linestyle="--")
    plt.tight_layout()
    plt.show()

# ==============================================================================
# 3. ANÁLISE GEOGRÁFICA
# ==============================================================================

def analise_geografica_clientes(dict_lojas):
    """
    Gera um gráfico de dispersão (Scatter Plot) onde o tamanho do ponto
    indica a frequência RELATIVA (percentual) de pedidos naquele local.
    """
    print("\n" + "=" * 80)
    print("ANÁLISE GEOGRÁFICA DE PEDIDOS (DENSIDADE POR PERCENTUAL)")
    print("=" * 80)
    
    plt.figure(figsize=(12, 10))
    cores = plt.cm.tab10.colors 
    
    # TABELA DE DADOS: GEOGRÁFICA (Top 5 Locais por Loja)
    print("\n" + "-" * 50)
    print("TABELA DE DADOS: TOP 5 LOCAIS COM MAIOR CONCENTRAÇÃO (%)")
    print("-" * 50)

    for i, (nome_loja, df) in enumerate(dict_lojas.items()):
        df_geo = df.dropna(subset=['lat', 'lon'])
        
        if df_geo.empty:
            print(f"Sem dados de GPS válidos para {nome_loja}")
            continue
            
        # 1. Agrupa por coordenadas para contar a frequência
        geo_agrupado = df_geo.groupby(['lat', 'lon']).size().reset_index(name='contagem')
        
        # 2. Calcula o percentual representativo de cada ponto em relação ao total da loja
        total_pedidos_loja = len(df_geo)
        geo_agrupado['percentual'] = (geo_agrupado['contagem'] / total_pedidos_loja) * 100
        
        # Imprime os Top 5 locais
        top_locais = geo_agrupado.sort_values(by='percentual', ascending=False).head(5)
        print(f"\n>> {nome_loja} (Total Pedidos com GPS: {total_pedidos_loja})")
        print(top_locais[['lat', 'lon', 'percentual']].to_string(index=False, formatters={'percentual': '{:.2f}%'.format}))

        # 3. Define o tamanho dos pontos baseado no percentual
        # Fator de multiplicação para tornar o ponto visível (ex: 1% -> tamanho 30)
        # Adicionamos um tamanho mínimo (min_size) para pontos com % muito baixo não sumirem
        tamanhos = np.maximum(geo_agrupado['percentual'] * 50, 20)
        
        # Plotagem
        plt.scatter(
            x=geo_agrupado['lon'], 
            y=geo_agrupado['lat'], 
            s=tamanhos, 
            label=f"{nome_loja} (Total: {total_pedidos_loja})",
            color=cores[i % len(cores)],
            alpha=0.6,
            edgecolors='w',
            linewidth=0.5
        )

    plt.title("Distribuição Geográfica: Percentual de Pedidos por Local", fontsize=20, pad=15)
    plt.xlabel("Longitude", fontsize=12)
    plt.ylabel("Latitude", fontsize=12)
    plt.legend(title="Filiais", fontsize=10, loc='best', markerscale=0.5) # markerscale ajusta o tamanho na legenda
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Adiciona anotação explicativa
    plt.text(0.02, 0.02, 'O tamanho do ponto representa o % de vendas da loja naquele local', 
             transform=plt.gca().transAxes, fontsize=10, 
             bbox=dict(facecolor='white', alpha=0.8))
             
    plt.axis('equal') 
    plt.tight_layout()
    plt.show()
    print("Gráfico de densidade geográfica (baseado em percentual) gerado com sucesso.\n")

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

def main():
    lojas = carregar_dados()
    if not lojas: return

    # Execução das análises
    verificar_nulos(lojas)
    
    relatorio_vendas_por_loja(lojas)
    graficos_comparativos_vendas(lojas)
    relatorio_vendas_por_categoria(lojas)
    graficos_categorias_comparativas(lojas)
    avaliacao_por_categoria(lojas)
    avaliacao_comparativa_categorias(lojas)
    avaliacao_geral_por_loja(lojas)
    produtos_mais_menos_vendidos(lojas, top=10)
    frete_medio_por_loja(lojas)
    
    # Análise Geográfica (Agora com Tamanho por Frequência)
    analise_geografica_clientes(lojas)

if __name__ == "__main__":
    main()