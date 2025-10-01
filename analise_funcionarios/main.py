import pandas as pd
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px  # 🆕 Adicionar Plotly para gráficos melhores

# Configuração da página
st.set_page_config(page_title="Análise de Funcionários", layout="wide")

@st.cache_data
def carregar_dados():
    df = pd.read_csv('./funcionarios.csv', sep=',', encoding='utf-8')
    df['data_contratacao'] = pd.to_datetime(df['data_contratacao'])
    df['lucro'] = df['vendas_mensal'] - df['comissao']
    df = df.rename(columns={'vendas_mensal': 'vendas_mensais'})
    return df

# Carregar dados
df = carregar_dados()

# Sidebar com filtros
st.sidebar.title("Filtros")
departamento = st.sidebar.selectbox(
    "Departamento",
    options=['Todos'] + list(df['departamento'].unique())
)

# Aplicar filtros
if departamento != 'Todos':
    df_filtrado = df[df['departamento'] == departamento].copy()
else:
    df_filtrado = df.copy()

df_filtrado = df_filtrado.sort_values('lucro', ascending=False).reset_index(drop=True)

# Identificar baixo desempenho (usando percentil para ser mais inteligente)
limite_baixo = df_filtrado['vendas_mensais'].quantile(0.25)  # Primeiro quartil
funcionarios_baixo_desempenho = df_filtrado[df_filtrado['vendas_mensais'] < limite_baixo].copy()

# Layout principal
st.title('📊 Dashboard de Análise de Funcionários')
st.write(f'Data de análise: {datetime.now().strftime("%d/%m/%Y %H:%M")}')

# Métricas de negócio
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Funcionários", len(df_filtrado))
with col2:
    st.metric("Vendas Médias", f"R$ {df_filtrado['vendas_mensais'].mean():,.0f}")
with col3:
    st.metric("Lucro Total", f"R$ {df_filtrado['lucro'].sum():,.0f}")
with col4:
    st.metric("Baixo Desempenho", len(funcionarios_baixo_desempenho))

# Gráficos modernos com Plotly
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Vendedores")
    top_10 = df_filtrado.head(10)
    fig = px.bar(top_10, x='nome', y='vendas_mensais', 
                 color='vendas_mensais',
                 title="Top 10 Melhores Vendedores")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Vendas vs Idade")
    fig2 = px.scatter(df_filtrado, x='idade', y='vendas_mensais',
                     color='departamento', size='avaliacao',
                     title="Relação: Idade vs Vendas",
                     hover_data=['nome'])
    st.plotly_chart(fig2, use_container_width=True)

# Tabela interativa
st.subheader("📋 Dados Detalhados dos Funcionários")
st.dataframe(df_filtrado[['nome', 'idade', 'departamento', 'vendas_mensais', 
                         'comissao', 'lucro', 'metas_atingidas', 'avaliacao']], 
             use_container_width=True)

# Análise de baixo desempenho
if not funcionarios_baixo_desempenho.empty:
    st.subheader("🎯 Funcionários com Baixo Desempenho (Necessitam Atenção)")
    st.dataframe(funcionarios_baixo_desempenho[['nome', 'vendas_mensais', 'metas_atingidas', 'avaliacao']],
                 use_container_width=True)
    
    
# 1. Análise temporal (se tiver dados históricos)
st.subheader("📈 Evolução Temporal")
# Gráfico de contratações por ano/mês

# 2. Análise de correlação
st.subheader("🔍 Correlações")
correlacao = df_filtrado[['idade', 'vendas_mensais', 'metas_atingidas', 'avaliacao']].corr()
st.dataframe(correlacao.style.background_gradient(cmap='coolwarm'))

# 3. KPIs por departamento
st.subheader("🏢 Performance por Departamento")
kpi_departamento = df_filtrado.groupby('departamento').agg({
    'vendas_mensais': 'mean',
    'lucro': 'sum',
    'nome': 'count'
}).round(2)
st.dataframe(kpi_departamento)