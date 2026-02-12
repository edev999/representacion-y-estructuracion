import polars as pl
import plotly.graph_objects as go
import numpy as np

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
        "Puntos: %{x}<br>" +
        "% Victorias: %{y:.2f}<br>" +
        "Dif Goles: %{z}<extra></extra>"
))

fig.update_layout(
    title="Nube 3D: Puntos vs %Victorias vs DifGoles",
    scene=dict(
        xaxis=dict(title="GolesAFavor", nticks=5),
        yaxis=dict(title="GolesEnContra", nticks=5),
        zaxis=dict(title="PromPuntosPorPartido", nticks=5),
    ),
    width=800,
    height=700,
    margin=dict(r=20, l=10, b=10, t=40)
)

fig.show()


