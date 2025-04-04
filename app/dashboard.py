# dashboard.py
import streamlit as st
import matplotlib.pyplot as plt
from modules.data_loader import carregar_pasta
from modules.processing import aplicar_regras_compartilhadas, aplicar_regras_exclusao
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(layout="wide")


# Carregar dados
df = carregar_pasta()

# Aplicar regras de exclusão antes de qualquer outro processamento
df = aplicar_regras_exclusao(df)

# Definir mês
df["mês_ano"] = df["data"].dt.to_period("M").astype(str)
mes = st.sidebar.selectbox(
    "Selecione o mês:", sorted(df["mês_ano"].unique(), reverse=True)
)

# Aplicar regras compartilhadas
df, mask_compartilhados_full = aplicar_regras_compartilhadas(df)

# Filtrar pelo mês
df_mes = df[df["mês_ano"] == mes]
mask_compartilhados = mask_compartilhados_full[df["mês_ano"] == mes]

# Títulos e gráficos
st.title("📊 Dashboard Financeiro Pessoal")
st.subheader(f"Gastos detalhados - {mes}")

# fig, ax = plt.subplots(figsize=(10, 5))
# df_mes.groupby("categoria")["valor_final"].sum().sort_values().plot.barh(
#     ax=ax, color="lightblue"
# )
# ax.set_xlabel("Total Gasto (R$)")
# ax.set_ylabel("Categoria")
# st.pyplot(fig)

# Totais
total_compartilhado = df_mes[mask_compartilhados]["valor_final"].sum()
total_geral = df_mes["valor_final"].sum()
total_individual = total_geral - total_compartilhado

total_compartilhado = df_mes[mask_compartilhados & (df_mes["valor"] < 0)][
    "valor_final"
].sum()
total_gastos_individuais = df_mes[~mask_compartilhados & (df_mes["valor"] < 0)][
    "valor_final"
].sum()
total_entradas_individuais = df_mes[~mask_compartilhados & (df_mes["valor"] > 0)][
    "valor_final"
].sum()

# Saldo total do mês (soma de tudo)
saldo_total = df_mes["valor_final"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gastos Compartilhados", f"R$ {abs(total_compartilhado):.2f}")
col2.metric("Gastos Individuais", f"R$ {abs(total_gastos_individuais):.2f}")
col3.metric("Entradas Individuais", f"R$ {total_entradas_individuais:.2f}")
col4.metric("Saldo Total", f"R$ {saldo_total:.2f}")


# Função para exibir AgGrid
def exibir_aggrid(df, key):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filter=True, sortable=True, resizable=True)
    gb.configure_grid_options(domLayout="normal")
    gb.configure_side_bar()
    grid_options = gb.build()
    AgGrid(df, gridOptions=grid_options, height=400, theme="alpine", key=key)


# Tabela gastos compartilhados
st.subheader("🔗 Gastos Compartilhados")
exibir_aggrid(df_mes[mask_compartilhados].sort_values(by="data"), key="compartilhados")

# Tabela gastos individuais
st.subheader("📋 Gastos Individuais")
exibir_aggrid(df_mes[~mask_compartilhados].sort_values(by="data"), key="individuais")


# Gráficos lado a lado
col1, col2 = st.columns(2)

# Gráfico gastos por categoria
with col1:
    st.subheader("📊 Gastos por Categoria")
    fig, ax = plt.subplots(figsize=(10, 7))
    df_mes.groupby("categoria")["valor_final"].sum().sort_values().plot.barh(
        ax=ax, color="lightblue"
    )
    ax.set_xlabel("Total Gasto (R$)", fontsize=12)
    ax.set_ylabel("Categoria", fontsize=12)
    ax.tick_params(axis="both", labelsize=10)
    st.pyplot(fig)

# Gráfico evolução mensal
with col2:
    st.subheader("📈 Evolução Mensal dos Gastos Totais")
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    df.groupby("mês_ano")["valor_final"].sum().plot(
        ax=ax2, marker="o", linestyle="--", color="skyblue"
    )
    ax2.set_xlabel("Mês", fontsize=12)
    ax2.set_ylabel("Total Gasto (R$)", fontsize=12)
    ax2.tick_params(axis="both", labelsize=10)
    ax2.grid(True)
    st.pyplot(fig2)
