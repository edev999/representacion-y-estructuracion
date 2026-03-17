import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import plotly.express as px

# 1. Cargar dataset y limpiar datos
df = pd.read_csv("data_output/datos_jugadores.csv")

# Eliminar jugadores con datos clave faltantes
df = df.dropna(subset=['MarketValue', 'Age', 'goals', 'assists']).copy()

# Eliminar valores de mercado no válidos
df = df[df['MarketValue'] > 0]


# 2. Seleccionar variables que explican el valor de mercado
features = ['Age', 'goals', 'assists', 'time']

# Añadir métricas avanzadas si existen en el dataset
if 'xG' in df.columns:
    features.append('xG')
if 'xA' in df.columns:
    features.append('xA')

X = df[features]        # Variables explicativas
y = df['MarketValue']   # Variable objetivo


# 3. Dividir datos para entrenamiento y validación (80 / 20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# 4. Escalar variables
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Ajustar scaler con entrenamiento
X_test_scaled = scaler.transform(X_test)        # Aplicar el mismo scaler al test


# 5. Entrenar modelo
modelo = LinearRegression()
modelo.fit(X_train_scaled, y_train)


# 6. Predecir el valor estimado para todos los jugadores
X_all_scaled = scaler.transform(X)
y_all_pred = modelo.predict(X_all_scaled)


# 7. Preparar dataframe para visualización
df_plot = df.copy()

# Valor estimado por el modelo
df_plot['Valor_IA'] = y_all_pred

# Diferencia entre valor predicho y valor real
df_plot['Error'] = df_plot['Valor_IA'] - df_plot['MarketValue']

# Marcar qué jugadores fueron usados en validación
df_plot['Origen'] = 'Entrenamiento (Train)'
df_plot.loc[X_test.index, 'Origen'] = 'Validación (Test)'


# 8. Evaluación del modelo
y_test_pred = modelo.predict(X_test_scaled)
r2 = r2_score(y_test, y_test_pred)                # Calidad de la predicción
mae = mean_absolute_error(y_test, y_test_pred)    # Error medio en euros


# 9. Gráfico técnico (train/test + ligas): valor real vs valor estimado
fig = px.scatter(
    df_plot,
    x="MarketValue",         # Valor real
    y="Valor_IA",            # Valor estimado
    color="Error",           # Diferencia entre ambos
    size="goals",            # Tamaño según goles
    facet_col="Origen",      # Separar train/test
    facet_row="League",      # Separar por liga
    hover_name="Player",
    hover_data={
        "MarketValue": ":.2s",
        "Valor_IA": ":.2s",
        "Team": True,
        "Age": True
    },
    title="Rendimiento vs Valor de Mercado",
    labels={
        "MarketValue": "Valor Real (€)",
        "Valor_IA": "Valor Estimado",
        "goals": "Goles"
    },
    color_continuous_scale="RdYlGn",
    height=1000,
    size_max=20
)

# Limpiar títulos de subgráficos
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Añadir línea de referencia: predicción perfecta (y = x)
for r in range(1, 6):
    for c in range(1, 3):
        fig.add_shape(
            type="line",
            x0=0, y0=0,
            x1=df['MarketValue'].max(),
            y1=df['MarketValue'].max(),
            line=dict(color="SlateGray", dash="dot", width=0.5),
            row=r, col=c
        )

# fig.show()

# Exportación
fig.write_html("plots_output/scouting_final.html")
print("\nArchivo 'scouting_final.html' generado con éxito.")


# 10. Nuevo gráfico global (sin separar train/test)
fig_ligas = px.scatter(
    df_plot,
    x="MarketValue",
    y="Valor_IA",
    color="Error",
    size="goals",
    # facet_col="League",
    facet_row="League",
    hover_name="Player",
    hover_data={
        "MarketValue": ":.2s",
        "Valor_IA": ":.2s",
        "Team": True,
        "Age": True
    },
    title="Valor Real vs Valor Estimado por Liga (Todos los jugadores)",
    labels={
        "MarketValue": "Valor Real (€)",
        "Valor_IA": "Valor Estimado",
        "goals": "Goles"
    },
    color_continuous_scale="RdYlGn",
    height=1000,
    size_max=20
)

# Limpiar títulos de subgráficos
fig_ligas.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

num_ligas = df_plot['League'].nunique()

for row in range(1, num_ligas + 1):
    fig_ligas.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=df['MarketValue'].max(),
        y1=df['MarketValue'].max(),
        line=dict(color="SlateGray", dash="dot", width=0.5),
        row=row,
        col=1
    )

fig_ligas.write_html("plots_output/scouting_ligas.html")
fig_ligas.show()

print("Archivo 'scouting_ligas.html' generado con éxito.")


# 11. Informe técnico del modelo
print("\n" + "="*40)
print("INFORME DE MODELADO - VALOR DE MERCADO")
print("="*40)
print(f"Muestra entrenamiento (80%): {len(X_train)} jugadores")
print(f"Muestra validación (20%): {len(X_test)} jugadores")
print("-" * 40)
print(f"R2 del modelo: {r2:.2f}")
print(f"Error medio de predicción: {mae:,.0f} €")
print("-" * 40)

# Interpretación básica del resultado
if r2 > 0.6:
    print("Conclusión: el rendimiento explica bien el valor de mercado.")
else:
    print("Conclusión: el mercado incluye factores adicionales (marketing, potencial, reputación).")

print("="*40)