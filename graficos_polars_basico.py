import polars as pl
import plotly.express as px

# -------------------------------------------------------
# 1. Leer CSV filtrado con Polars
# -------------------------------------------------------
df = pl.read_csv("equipos_filtrados_metricas_polars.csv")

# -------------------------------------------------------
# 2. Procesamiento con Polars (métricas adicionales)
# -------------------------------------------------------
# Crear columna de diferencia de goles si no existe
if "DifGoles" not in df.columns:
    df = df.with_columns((df["GolesAFavor"] - df["GolesEnContra"]).alias("DifGoles"))

# Crear columna de porcentaje de victorias si no existe
if "PorcVictorias" not in df.columns:
    df = df.with_columns((df["Victorias"] / df["PartidosJugados"] * 100).alias("PorcVictorias"))

# -------------------------------------------------------
# 3. Convertir a pandas solo para Plotly
# -------------------------------------------------------
df_pd = df.to_pandas()

# -------------------------------------------------------
# 4. Gráfico de barras: Goles a favor por equipo
# -------------------------------------------------------
fig1 = px.bar(
    df_pd,
    x="GolesAFavor",
    y="Equipo",
    color="Liga",
    title="Goles a favor por equipo",
    orientation="h"
)
fig1.show()

# -------------------------------------------------------
# 5. Gráfico de barras: Diferencia de goles por equipo
# -------------------------------------------------------
fig2 = px.bar(
    df_pd,
    x="DifGoles",
    y="Equipo",
    color="Liga",
    title="Diferencia de goles por equipo",
    orientation="h"
)
fig2.show()

# -------------------------------------------------------
# 6. Gráfico combinado: Puntos vs %Victorias
# -------------------------------------------------------
fig3 = px.scatter(
    df_pd,
    x="Puntos",
    y="PorcVictorias",
    color="Liga",
    hover_name="Equipo",
    size="DifGoles",
    title="Puntos vs %Victorias (tamaño = DifGoles)"
)
fig3.show()
