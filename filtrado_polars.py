import sqlite3
import polars as pl
from pathlib import Path

# ---------------------------------
# 1. Conectar a la base de datos
# ---------------------------------
conn = sqlite3.connect("soccer.db")

# ---------------------------------
# 2. Traer los datos de la base
# ---------------------------------
query = """
SELECT t.name AS Equipo,
       l.name AS Liga,
       s.points AS Puntos,
       s.goals_for AS GolesAFavor,
       s.goals_against AS GolesEnContra,
       s.wins AS Victorias,
       s.draws AS Empates,
       s.losses AS Derrotas,
       s.played AS PartidosJugados
FROM teams t
JOIN league l ON t.league_id = l.id
JOIN stats s ON t.id = s.team_id
"""
df = pl.read_database(query, connection=conn)

# Cerrar la conexión
conn.close()

df = df.filter(pl.col("Equipo").is_not_null())
df = df.filter(pl.col("Puntos").is_not_null())
df = df.with_columns(
    pl.col("GolesAFavor").fill_null(0),
    pl.col("GolesEnContra").fill_null(0)
)

# ---------------------------------
# 3. Calcular métricas nuevas
# ---------------------------------
df = df.with_columns([
    (pl.col("GolesAFavor") - pl.col("GolesEnContra")).alias("DifGoles"),
    (pl.col("Puntos") / pl.col("PartidosJugados")).alias("PromPuntosPorPartido"),
    (pl.col("Victorias") / pl.col("PartidosJugados") * 100).alias("PorcVictorias")
])

# ---------------------------------
# 4. Revisar el dataframe final
# ---------------------------------
print(df)

# ---------------------------------
# 5. Guardar en CSV opcional
# ---------------------------------
Path("data_output").mkdir(parents=True, exist_ok=True)
df.write_csv("data_output/equipos_filtrados_metricas_polars.csv")
