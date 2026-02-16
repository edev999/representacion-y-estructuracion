import sqlite3
import polars as pl
from pathlib import Path

# Configurar la visualización del DataFrame
pl.Config.set_tbl_cols(-1)          # Todas las columnas
pl.Config.set_fmt_str_lengths(200)  # Evitar truncado de valores largos


# -----------------------------------------------
# 1. Carga de datos desde SQL
# -----------------------------------------------
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

with sqlite3.connect("soccer.db") as conn: 
    df = pl.read_database(query, connection=conn)

# -----------------------------------------------
# 2. Limpiar y estructurar los datos
# -----------------------------------------------
df = df.filter(pl.col("Equipo").is_not_null())
df = df.filter(pl.col("Puntos").is_not_null())
df = df.with_columns(
    pl.col("GolesAFavor").fill_null(0),
    pl.col("GolesEnContra").fill_null(0)
)

# -----------------------------------------------
# 3. Calcular métricas nuevas
# -----------------------------------------------
df = df.with_columns([

    (pl.col("GolesAFavor") - pl.col("GolesEnContra")).alias("DifGoles"),

    pl.when(pl.col("PartidosJugados") > 0)
      .then(pl.col("Puntos") / pl.col("PartidosJugados"))
      .otherwise(None)
      .alias("PromPuntosPorPartido"),

    pl.when(pl.col("PartidosJugados") > 0)
      .then(pl.col("Victorias") / pl.col("PartidosJugados") * 100)
      .otherwise(None)
      .alias("PorcVictorias"),

    pl.when(pl.col("GolesEnContra") > 0)
      .then(pl.col("GolesAFavor") / pl.col("GolesEnContra"))
      .otherwise(None)
      .alias("RatioOfensivoDefensivo"),

    ((pl.col("GolesAFavor") - pl.col("GolesEnContra"))
        / pl.max_horizontal(pl.col("PartidosJugados"), pl.lit(1))
    ).alias("EficienciaGlobal")
])

# -----------------------------------------------
# 4. Revisar el dataframe final
# -----------------------------------------------
print(df)

# -----------------------------------------------
# 5. Métricas agregadas por liga
# -----------------------------------------------
df_liga = df.group_by("Liga").agg([
    pl.col("Puntos").mean().alias("MediaPuntos"),
    pl.col("GolesAFavor").mean().alias("MediaGolesAFavor"),
    pl.col("GolesEnContra").mean().alias("MediaGolesEnContra"),
    pl.col("DifGoles").mean().alias("MediaDifGoles")
])

# -----------------------------------------------
# 6. Generar datasets
# -----------------------------------------------

# Top por victorias
df_top = df.sort("PorcVictorias", descending=True)

# Ranking ofensivo
df_ofensivo = df.sort("GolesAFavor", descending=True)

# Crear carpeta de salida si no existe
Path("data_output").mkdir(parents=True, exist_ok=True)

# Exportar dataset principal (CSV y Parquet)
df.write_csv("data_output/equipos_filtrados_metricas_polars.csv")
df.write_parquet("data_output/equipos.parquet")

# Exportar datasets adicionales
df_liga.write_csv("data_output/resumen_por_liga.csv")
df_top.write_csv("data_output/top_por_victorias.csv")
df_ofensivo.write_csv("data_output/ranking_ofensivo.csv")

# -----------------------------------------------
# 7. Resumen del proceso
# -----------------------------------------------
print("\n" + "=" * 50)
print("RESUMEN DEL PROCESO".center(50))
print("=" * 50)

# Confirmar carga desde SQL
print("✓ Datos cargados correctamente desde SQLite.")

# Mostrar número de filas del dataframe final
print(f"✓ Equipos procesados: {df.height} filas.")

# Confirmar exportaciones
print("\n" + "-" * 50) 
print("Archivos exportados".center(50)) 
print("-" * 50)
print("data_output/\n")
print(" - equipos_filtrados_metricas_polars.csv")
print(" - equipos.parquet")
print(" - resumen_por_liga.csv")
print(" - top_por_victorias.csv")
print(" - ranking_ofensivo.csv")

print("\n" + "-" * 50)
print("Resumen por liga".center(50))
print("-" * 50)
print(df_liga)

print("\n" + "=" * 50)
print("PROCESO COMPLETADO".center(50))
print("=" * 50 + "\n")