import polars as pl
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# -----------------------------------------------
# 1. Leer CSV filtrado con Polars
# -----------------------------------------------
df = pl.read_csv("equipos_filtrados_metricas.csv")

# -----------------------------------------------
# 2. Procesamiento con Polars
# -----------------------------------------------
if "DifGoles" not in df.columns:
    df = df.with_columns(
        (df["GolesAFavor"] - df["GolesEnContra"]).alias("DifGoles")
    )

if "PorcVictorias" not in df.columns:
    df = df.with_columns(
        (df["Victorias"] / df["PartidosJugados"] * 100).alias("PorcVictorias")
    )

# -----------------------------------------------
# 3. Convertir a pandas para Plotly
# -----------------------------------------------
df_pd = df.to_pandas()

# -----------------------------------------------
# 4. Gráfico 3D
# -----------------------------------------------
fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=df_pd["Puntos"],
    y=df_pd["PorcVictorias"],
    z=df_pd["DifGoles"],
    mode='markers',
    marker=dict(
        size=8,
        color=df_pd["DifGoles"],
        colorscale='Viridis',
        opacity=0.7
    ),
    text=df_pd["Equipo"],
    hovertemplate=
        "<b>%{text}</b><br>" +
        "% Victorias: %{y:.2f}<br>" +
        "Dif Goles: %{z}<extra></extra>"
))

fig.update_layout(
    title="Nube 3D: Puntos vs %Victorias vs DifGoles",
    scene=dict(
        xaxis=dict(title="GolesAFavor", nticks=5),
        yaxis=dict(title="GolesEnContra", nticks=5),
        zaxis=dict(title="PorcVictorias", nticks=5),
    ),
    width=800,
    height=700,
    margin=dict(r=20, l=10, b=10, t=40)
)

fig.show()

fig1 = px.scatter(
    df_pd, 
    x="DifGoles", 
    y="Puntos", 
    hover_name="Equipo",
    labels={
        "DifGoles": "Diferencia de Goles",
        "Puntos": "Puntos Totales"
    },
    title="Relación entre Diferencia de Goles y Puntos por Equipo"
)

fig1.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))

fig1.show()

