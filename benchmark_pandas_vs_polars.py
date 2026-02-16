import time
import pandas as pd
import polars as pl

# -----------------------------------------------
# 1. Cargar el dataset generado por Polars
# -----------------------------------------------
csv_path = "data_output/equipos_filtrados_metricas_polars.csv"

df_pandas = pd.read_csv(csv_path)
df_polars = pl.read_csv(csv_path)

# -----------------------------------------------
# 2. Mostrar información básica del dataset
# -----------------------------------------------
print("\n" + "=" * 50)
print("--- BENCHMARK: Pandas vs Polars ---".center(50))
print("=" * 50)
print(f"Filas en el dataset: {len(df_pandas)}\n")

# -----------------------------------------------
# 3. Operación compleja en Pandas
# -----------------------------------------------
start = time.perf_counter()
resultado_pandas = (
    df_pandas.groupby("Liga")["Puntos"]
    .mean()
    .sort_values(ascending=False)
)
end = time.perf_counter()
print(f"Pandas: {end - start} segundos")

# -----------------------------------------------
# 4. Operación equivalente en Polars
# -----------------------------------------------
start = time.perf_counter()
resultado_polars = (
    df_polars.group_by("Liga")
    .agg(pl.col("Puntos").mean())
    .sort("Puntos", descending=True)
)
end = time.perf_counter()
print(f"Polars: {end - start} segundos")

# -----------------------------------------------
# 5. Fin del benchmark
# -----------------------------------------------
print("\nBenchmark completado.\n")
