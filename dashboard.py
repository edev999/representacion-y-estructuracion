import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. CONFIGURACIÓN BÁSICA DEL DASHBOARD
# ---------------------------------------------------------

st.set_page_config(
    page_title="Scouting Dashboard",
    layout="wide"
)

st.title("Análisis de Valor de Mercado")

st.markdown("""
Visualización del **valor real** frente al **valor estimado** por el modelo, organizado por ligas.
""")

# ---------------------------------------------------------
# 2. CARGA DE DATOS
# ---------------------------------------------------------

df = pd.read_csv("data_output/datos_jugadores_modelado.csv")

# Limpieza mínima (igual que en tu script)
df = df.dropna(subset=['MarketValue', 'Age', 'goals', 'assists']).copy()
df = df[df['MarketValue'] > 0]

# Asegurar que las columnas necesarias existen
if "Valor_IA" not in df.columns:
    st.error("El CSV no contiene la columna 'Valor_IA'. Asegúrate de ejecutar antes el script de modelado.")
    st.stop()

df["Error"] = df["Valor_IA"] - df["MarketValue"]

# ---------------------------------------------------------
# 3. GRÁFICO GLOBAL (Plotly)
# ---------------------------------------------------------

fig_ligas = px.scatter(
    df,
    x="MarketValue",
    y="Valor_IA",
    color="Error",
    size="goals",
    facet_row="League",
    hover_name="Player",
    hover_data={
        "MarketValue": ":.2s",
        "Valor_IA": ":.2s",
        "Team": True,
        "Age": True
    },
    title="Valor Real vs Valor Estimado por Liga (jugadores)",
    labels={
        "MarketValue": "Valor Real (€)",
        "Valor_IA": "Valor Estimado",
        "goals": "Goles"
    },
    color_continuous_scale="RdYlGn",
    height=1000,
    size_max=20
)

# Limpiar títulos de facetas
fig_ligas.for_each_annotation(
    lambda a: a.update(text=a.text.split("=")[-1]) if "=" in a.text else a
)

# Línea diagonal automática en todas las facetas
fig_ligas.add_shape(
    type="line",
    x0=0,
    y0=0,
    x1=df['MarketValue'].max(),
    y1=df['MarketValue'].max(),
    line=dict(color="SlateGray", dash="dot", width=0.5),
    row="all",
    col="all"
)

# ---------------------------------------------------------
# 4. MOSTRAR GRÁFICO EN STREAMLIT
# ---------------------------------------------------------

st.plotly_chart(fig_ligas, use_container_width=True)
# st.success("Dashboard cargado correctamente.")