import polars as pl
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from pathlib import Path

# -------------------------------------------------------
# 1. Leer CSV filtrado con Polars
# -------------------------------------------------------
df = pl.read_csv("data_output/equipos_filtrados_metricas_polars.csv")

# -------------------------------------------------------
# 2. Procesamiento con Polars (métricas adicionales)
# -------------------------------------------------------
if "DifGoles" not in df.columns:
    df = df.with_columns((df["GolesAFavor"] - df["GolesEnContra"]).alias("DifGoles"))

if "PorcVictorias" not in df.columns:
    df = df.with_columns((df["Victorias"] / df["PartidosJugados"] * 100).alias("PorcVictorias"))

# AÑADIDO: asegurar que EficienciaGlobal existe
if "EficienciaGlobal" not in df.columns:
    df = df.with_columns(
        ((pl.col("GolesAFavor") - pl.col("GolesEnContra"))
            / pl.max_horizontal(pl.col("PartidosJugados"), pl.lit(1))
        ).alias("EficienciaGlobal")
    )

# -------------------------------------------------------
# 3. Convertir a pandas para Plotly
# -------------------------------------------------------
df_pd = df.to_pandas()

# -------------------------------------------------------
# 4. Gráfico 1: Goles a favor por equipo
# -------------------------------------------------------
df_goals_for = df_pd.sort_values("GolesAFavor", ascending=False)

fig_goles_favor = px.bar(
    df_goals_for,
    x="GolesAFavor",
    y="Equipo",
    color="Liga",
    orientation="h",
    hover_data=["Puntos", "DifGoles", "PorcVictorias"]
)

fig_goles_favor.update_layout(
    height=20 * len(df_goals_for),
    margin=dict(l=150, t=60),
    title={
        "text": "<span style='font-weight:600; font-size:22px; color:darkslategray;'>Goles a Favor por Equipo</span>",
        "x": 0.5
    }
)

fig_goles_favor.update_yaxes(tickfont=dict(size=12), ticklabelstandoff=8)
fig_goles_favor.update_traces(hoverlabel=dict(font_color="white"))
fig_goles_favor.show()

# -------------------------------------------------------
# 5. Gráfico 2: Diferencia de goles por equipo
# -------------------------------------------------------
df_goal_diff = df_pd.sort_values("DifGoles", ascending=False)

fig_dif_goles = px.bar(
    df_goal_diff,
    x="DifGoles",
    y="Equipo",
    color="Liga",
    orientation="h",
    hover_data=["Puntos", "GolesAFavor", "GolesEnContra", "PorcVictorias"]
)

fig_dif_goles.update_layout(
    height=20 * len(df_goal_diff),
    margin=dict(l=150, t=60),
    title={
        "text": "<span style='font-weight:600; font-size:22px; color:darkslategray;'>Diferencia de Goles por Equipo</span>",
        "x": 0.5
    }
)

fig_dif_goles.update_yaxes(tickfont=dict(size=12), ticklabelstandoff=8)
fig_dif_goles.update_traces(hoverlabel=dict(font_color="white"))
fig_dif_goles.show()

# -------------------------------------------------------
# 6. Gráfico 3: Puntos vs %Victorias (tamaño = DifGolesAbs)
# -------------------------------------------------------

df_puntos_victorias = (
    df_pd
    .assign(DifGolesAbs=lambda df: df["DifGoles"].abs())
    .sort_values("DifGolesAbs")
)

fig_puntos_victorias = px.scatter(
    df_puntos_victorias,
    x="Puntos",
    y="PorcVictorias",
    color="Liga",
    hover_name="Equipo",
    size="DifGolesAbs",
    size_max=25,
    hover_data={
        "DifGoles": True,
        "GolesAFavor": True,
        "GolesEnContra": True,
        "Puntos": True
    },
    labels={"PorcVictorias": "% Victorias"}
)

fig_puntos_victorias.update_layout(
    margin=dict(l=80, t=60),
    title={
        "text": "<span style='font-weight:600; font-size:22px; color:darkslategray;'>Puntos vs %Victorias (tamaño = DifGoles)</span>",
        "x": 0.5
    },
    xaxis=dict(ticklabelstandoff=5),
    yaxis=dict(ticklabelstandoff=5)
)

fig_puntos_victorias.update_traces(
    hoverlabel=dict(font_color="white")
)

fig_puntos_victorias.show()

## -------------------------------------------------------
# 7. Gráfico 4: DifGoles vs Promedio de Puntos por Partido
# -------------------------------------------------------
fig_difgoles_prompuntos = px.scatter(
    df_pd,
    x="DifGoles",
    y="PromPuntosPorPartido",
    color="Liga",
    hover_name="Equipo",
    hover_data={
        "Puntos": True,
        "GolesAFavor": True,
        "GolesEnContra": True,
        "PorcVictorias": True,
        "DifGoles": True,
        "PromPuntosPorPartido": True
    },
    labels={
        "DifGoles": "Diferencia de Goles",
        "PromPuntosPorPartido": "Promedio de Puntos por Partido"
    }
)

fig_difgoles_prompuntos.update_layout(
    margin=dict(l=80, t=60),
    title={
        "text": "<span style='font-weight:600; font-size:22px; color:darkslategray;'>Relación entre Diferencia de Goles y Promedio de Puntos por Partido</span>",
        "x": 0.5
    }
)

fig_difgoles_prompuntos.update_xaxes(ticklabelstandoff=5)
fig_difgoles_prompuntos.update_yaxes(ticklabelstandoff=5)

fig_difgoles_prompuntos.update_traces(
    marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')),
    hoverlabel=dict(font_color="white")
)

fig_difgoles_prompuntos.show()

# -------------------------------------------------------
# 8. Gráfico 5: Distribución de Eficiencia Global por Liga
# -------------------------------------------------------
orden_ligas_eff = (
    df_pd.groupby("Liga")["EficienciaGlobal"]
    .median()
    .sort_values(ascending=False)
    .index
)

fig_eficiencia_box = px.box(
    df_pd,
    x="Liga",
    y="EficienciaGlobal",
    points="all",
    color="Liga",
    category_orders={"Liga": list(orden_ligas_eff)},
    hover_data={
        "Equipo": True,
        "Puntos": True,
        "DifGoles": True,
        "GolesAFavor": True,
        "GolesEnContra": True,
        "EficienciaGlobal": True
    },
    labels={"EficienciaGlobal": "Eficiencia Global"},
)

fig_eficiencia_box.update_layout(
    margin=dict(l=80, t=60),
    title={
        "text": "<span style='font-weight:600; font-size:22px; color:darkslategray;'>Distribución de Eficiencia Global por Liga (ordenada por mediana)</span>",
        "x": 0.5
    }
)

fig_eficiencia_box.update_traces(hoverlabel=dict(font_color="white"))
fig_eficiencia_box.show()

# -------------------------------------------------------
# 9. Gráfico 6: Facetado Puntos vs Eficiencia Global por Liga
# -------------------------------------------------------
orden_ligas_facet = (
    df_pd.groupby("Liga")["EficienciaGlobal"]
    .median()
    .sort_values(ascending=False)
    .index
)

fig_facet = px.scatter(
    df_pd,
    x="Puntos",
    y="EficienciaGlobal",
    color="Liga",
    facet_col="Liga",
    facet_col_wrap=3,
    category_orders={"Liga": list(orden_ligas_facet)},
    hover_name="Equipo",
    hover_data={
        "DifGoles": True,
        "PorcVictorias": True,
        "GolesAFavor": True,
        "GolesEnContra": True,
        "EficienciaGlobal": True,
        "Puntos": True
    },
    labels={
        "Puntos": "Puntos Totales",
        "EficienciaGlobal": "Eficiencia Global"
    }
)

fig_facet.update_layout(
    height=650,
    margin=dict(l=80, t=120, r=40, b=40),
    title={
        "text": "<span style='font-weight:600; font-size:20px; color:darkslategray;'>Puntos vs Eficiencia Global por Liga (facetado y ordenado por mediana)</span>",
        "x": 0.5,
        "y": 0.93,
        "yanchor": "top"
    },
    title_pad=dict(t=1)
)

fig_facet.update_traces(hoverlabel=dict(font_color="white"))
fig_facet.show()

# -------------------------------------------------------
# 10. Gráfico 7: Nube 3D Puntos vs %Victorias vs DifGoles
# -------------------------------------------------------
fig_3d = go.Figure()

fig_3d.add_trace(go.Scatter3d(
    x=df_pd["Puntos"],
    y=df_pd["PorcVictorias"],
    z=df_pd["DifGoles"],
    mode='markers',
    marker=dict(
        size=8,
        color=df_pd["DifGoles"],
        colorscale='Viridis',
        opacity=0.8,
    ),
    text=df_pd["Equipo"],
    hovertemplate="<b>%{text}</b><br>"
                  "Puntos: %{x}<br>"
                  "% Victorias: %{y:.2f}<br>"
                  "Dif Goles: %{z}<extra></extra>"
))

fig_3d.update_layout(
    title={
        "text": "<span style='font-weight:600; font-size:22px; color:darkslategray;'>Puntos, % de Victorias y Diferencia de Goles (Relación 3D)</span>",
        "x": 0.5
    },
    scene=dict(
        xaxis=dict(title="Puntos Totales", nticks=5),
        yaxis=dict(title="% Victorias", nticks=5),
        zaxis=dict(title="Diferencia de Goles", nticks=5),
    ),
    width=1100, 
    height=750, 
    margin=dict(r=40, l=40, b=40, t=80)
)

fig_3d.update_traces(
    hoverlabel=dict(font_color="white")
)

fig_3d.show()

# -------------------------------------------------------
# 11. Exportar gráficos (HTML)
# -------------------------------------------------------
Path("plots_output").mkdir(parents=True, exist_ok=True)

fig_goles_favor.write_html("plots_output/goles_a_favor.html")
fig_dif_goles.write_html("plots_output/diferencia_goles.html")
fig_puntos_victorias.write_html("plots_output/puntos_vs_victorias.html")
fig_difgoles_prompuntos.write_html("plots_output/difgoles_vs_prompuntos.html")
fig_eficiencia_box.write_html("plots_output/eficiencia_global_boxplot.html")
fig_facet.write_html("plots_output/eficiencia_global_facetado.html")
fig_3d.write_html("plots_output/nube3d_puntos_victorias_difgoles.html")

# -------------------------------------------------------
# 12. Resumen del proceso
# -------------------------------------------------------
print("\n" + "=" * 50)
print("RESUMEN DEL PROCESO".center(50))
print("=" * 50)

print("✓ Datos cargados desde: equipos_filtrados_metricas_polars.csv")
print(f"✓ Equipos procesados: {len(df_pd)}")
print("✓ Gráficos generados: 7")
print("✓ Archivos exportados en: plots_output/")

print("\n" + "-" * 50)
print("Archivos HTML exportados".center(50))
print("-" * 50)
print(" - goles_a_favor.html")
print(" - diferencia_goles.html")
print(" - puntos_vs_victorias.html")
print(" - difgoles_vs_prompuntos.html")
print(" - eficiencia_global_boxplot.html")
print(" - eficiencia_global_facetado.html")
print(" - nube3d_puntos_victorias_difgoles.html")

print("\n" + "=" * 50)
print("PROCESO COMPLETADO".center(50))
print("=" * 50 + "\n")