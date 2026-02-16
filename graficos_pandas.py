
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# 1. Leer CSV filtrado
# -------------------------------------------------------
df = pd.read_csv("data_output/equipos_filtrados_metricas.csv")

# -------------------------------------------------------
# 2. Procesamiento con pandas (métricas derivadas)
# -------------------------------------------------------
if "DifGoles" not in df.columns:
    df["DifGoles"] = df["GolesAFavor"] - df["GolesEnContra"]

if "PorcVictorias" not in df.columns:
    df["PorcVictorias"] = df["Victorias"] / df["PartidosJugados"] * 100

# -------------------------------------------------------
# 3. Gráfico de barras: Goles a favor por equipo
# -------------------------------------------------------
fig1 = px.bar(
    df,
    x="GolesAFavor",
    y="Equipo",
    color="Liga",
    title="Goles a favor por equipo",
    orientation="h"
)
fig1.show()

# -------------------------------------------------------
# 4. Gráfico de barras: Diferencia de goles por equipo
# -------------------------------------------------------
fig2 = px.bar(
    df,
    x="DifGoles",
    y="Equipo",
    color="Liga",
    title="Diferencia de goles por equipo",
    orientation="h"
)
fig2.show()

# -------------------------------------------------------
# 5. Gráfico combinado: Puntos vs %Victorias
# -------------------------------------------------------
df["DifGolesEscalado"] = df["DifGoles"] + df["DifGoles"].abs().max() + 1

fig3 = px.scatter(
    df,
    x="Puntos",
    y="PorcVictorias",
    color="Liga",
    hover_name="Equipo",
    size="DifGolesEscalado",
    size_max=20,
    hover_data={"DifGolesEscalado": False, "DifGoles": True},
    title="Puntos vs %Victorias (tamaño ajustado por DifGoles)",
    labels={"PorcVictorias": "% Victorias"}
)

fig3.show()

# -------------------------------------------------------
# 6. Gráfico facetado: Puntos vs %Victorias por Liga
# -------------------------------------------------------
fig_facet = px.scatter(
    df,
    x="Puntos",
    y="PorcVictorias",
    color="Equipo",
    facet_col="Liga",
    title="Puntos vs %Victorias por Liga"
)
fig_facet.show()