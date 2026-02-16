import os
import time
import polars as pl

# -----------------------------------------------
# 1. Rutas de los archivos a comparar
# -----------------------------------------------
csv_path = "data_output/equipos_filtrados_metricas_polars.csv"
parquet_path = "data_output/equipos.parquet"

# -----------------------------------------------
# 2. Comparación de tamaño en disco
# -----------------------------------------------
csv_size = os.path.getsize(csv_path)
parquet_size = os.path.getsize(parquet_path)

print("\n" + "=" * 50)
print("--- BENCHMARK: CSV vs Parquet ---".center(50))
print("=" * 50)

print(f"Tamaño CSV:     {csv_size} bytes")
print(f"Tamaño Parquet: {parquet_size} bytes\n")

# -----------------------------------------------
# 3. Tiempo de lectura del CSV
# -----------------------------------------------
start = time.perf_counter()
df_csv = pl.read_csv(csv_path)
end = time.perf_counter()
t_csv = end - start
print(f"Tiempo lectura CSV:     {t_csv:.6f} segundos")

# -----------------------------------------------
# 4. Tiempo de lectura del Parquet
# -----------------------------------------------
start = time.perf_counter()
df_parquet = pl.read_parquet(parquet_path)
end = time.perf_counter()
t_parquet = end - start
print(f"Tiempo lectura Parquet: {t_parquet:.6f} segundos")

# -----------------------------------------------
# 5. Fin del benchmark
# -----------------------------------------------
print("\nBenchmark completado.\n")
