import sqlite3
import pandas as pd

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
df = pd.read_sql_query(query, conn)

# Cerrar la conexión
conn.close()

# ---------------------------------
# 3. Calcular métricas nuevas
# ---------------------------------
# Diferencia de goles
df['DifGoles'] = df['GolesAFavor'] - df['GolesEnContra']

# Promedio de puntos por partido
df['PromPuntosPorPartido'] = df['Puntos'] / df['PartidosJugados']

# Porcentaje de victorias
df['PorcVictorias'] = df['Victorias'] / df['PartidosJugados'] * 100

# ---------------------------------
# 4. Revisar el dataframe final
# ---------------------------------
print(df)

# ---------------------------------
# 5. Guardar en CSV
# ---------------------------------
df.to_csv("equipos_filtrados_metricas.csv", index=False)
