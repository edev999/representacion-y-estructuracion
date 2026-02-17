# **Análisis de datos de ligas de fútbol**

## 1. Introducción

Este proyecto desarrolla un pipeline completo de análisis de datos futbolísticos utilizando Polars y Plotly. A partir de un dataset de equipos y resultados almacenado en una base de datos SQLite, se lleva a cabo un proceso estructurado de extracción, transformación, carga y análisis visual. El objetivo es convertir los datos brutos en información clara, comparable y visualmente interpretable, permitiendo analizar el rendimiento de los equipos desde múltiples perspectivas.

## 2. Objetivos

El proyecto persigue los siguientes objetivos:  
- Extraer y cargar los datos desde una base de datos SQLite dentro de un flujo automatizado en Python.  
- Aplicar técnicas de limpieza, filtrado y estructuración utilizando Polars.  
- Generar métricas avanzadas como porcentaje de victorias, diferencia de goles y promedio de puntos por partido.  
- Exportar los resultados en formatos estándar (CSV) y orientados a análisis de alto rendimiento (Parquet).  
- Crear visualizaciones interactivas con Plotly que permitan identificar patrones, comparar equipos y explorar el dataset de forma dinámica.  
- Evaluar el rendimiento de distintas tecnologías (Pandas vs Polars, CSV vs Parquet) como parte de la ampliación solicitada.  

## Características

Ingesta: Uso de Polars para manejar grandes volúmenes de datos desde SQL, en este caso SQLite.

## 3. Pasos

## Paso 1: Conexión

Se establece la conexión con la base de datos SQLite y se extraen las tablas necesarias para cargarlas directamente en Polars mediante los métodos de lectura adecuados, asegurando una importación eficiente como punto de partida del análisis.

## Paso 2: Limpieza y Estructuración con Polars

## Ingeniería de variables

Cálculo de métricas avanzadas como % de Victorias, Diferencia de Goles y Promedio de Puntos por Partido, junto con la creación de columnas derivadas y transformaciones necesarias para estandarizar el dataset. En este paso también se aplican filtros, normalizaciones y ajustes de tipos con Polars, dejando los datos limpios y estructurados para su posterior análisis y visualización.

## Paso 3: Generación de Datasets para Informes

En esta fase se exportan los resultados del análisis a distintos formatos para facilitar su uso en informes y herramientas externas. El dataset principal se guarda en CSV, un formato universal que permite revisar y compartir los datos fácilmente.

Además, se generan varios archivos derivados (ranking ofensivo, top por victorias y resumen por liga), cada uno orientado a responder preguntas específicas del análisis y a facilitar la exploración desde distintos ángulos.
Junto al CSV, el script exporta también el dataset final en formato Parquet, con el objetivo de evaluar su comportamiento en entornos Big Data. Aunque Parquet suele ser más eficiente en cargas analíticas de gran volumen, en este proyecto se genera principalmente para permitir su comparación con el CSV dentro de la ampliación solicitada. 

La exportación se realiza mediante:

```Bash
df.write_parquet("data_output/equipos.parquet")
```

## Paso 4: Análisis Visual con Plotly

A continuación se presenta el análisis visual realizado con Plotly, que permite explorar patrones de rendimiento, identificar outliers y comparar equipos y ligas desde múltiples perspectivas.

## Visualización Interactiva

Gráficos 3D y de dispersión utilizando Plotly para identificar patrones de rendimiento. Los Gráficos se exportan en un HTML interactivo que se abre directamente en el navegador. 

Ambos gráficos son interactivos, en el caso de Scatter3D se permite analizar el gráfico en tres dimensiones, y en el segundo gráfico se puede seleccionar un tramo para ampliar la vista sobre una zona específica.

## Visualizaciones Incluidas

Scatter Plot 2D: Relación entre la Diferencia de Goles y el Promedio de los Puntos por Partido. Ideal para ver la consistencia del equipo.

Scatter Plot 3D: Un análisis multidimensional que cruza Puntos, Porcentaje de Victorias y Diferencia de Goles para clasificar el dominio de los equipos.

Además de estos gráficos estratégicos, el análisis incorpora un conjunto más amplio de visualizaciones que permiten explorar el rendimiento de los equipos desde distintos ángulos:

Goles a Favor por Equipo (barras): identifica qué equipos destacan ofensivamente dentro de cada liga.

Diferencia de Goles por Equipo (barras): muestra qué equipos dominan en balance ofensivo‑defensivo.

Puntos vs % Victorias (scatter): relaciona regularidad (puntos) y eficacia (victorias), con el tamaño indicando la diferencia de goles.

Diferencia de Goles vs Promedio de Puntos por Partido (scatter): confirma la correlación entre dominancia en el marcador y rendimiento competitivo.

Eficiencia Global por Liga (boxplot): compara la competitividad entre ligas y permite detectar ligas más equilibradas o más dominadas por pocos equipos.

Puntos vs Eficiencia Global por Liga (facetado): facilita comparar patrones entre ligas manteniendo la misma escala visual.

(Nube 3D) Puntos - % Victorias – Diferencia de Goles: ofrece una visión multidimensional para identificar perfiles de equipos y posibles outliers.

Plotly muestra los gráficos directamente en el navegador al ejecutarse el script, pero no los guarda en disco a menos que se indique explícitamente. En este proyecto, además de mostrarse, los gráficos se exportan como HTML interactivo dentro de plots_output/.

Para generar un archivo .html se utiliza:

```Bash
fig.write_html("plots_output/nombre_del_grafico.html")
```

## 4. Estructura del proyecto y archivos incluidos

├── main.py                         # Pipeline principal del proyecto  
├── filtrado_polars.py              # Filtrado y cálculo de métricas con Polars  
├── graficos_polars_analisi.py  # Visualizaciones interactivas con Plotly  
│  
├── filtrado_pandas.py              # Pipeline equivalente en Pandas (fase exploratoria)  
├── graficos_pandas.py              # Gráficos iniciales con Pandas  
│  
├── benchmark_pandas_vs_polars.py   # Comparación de rendimiento entre Pandas y Polars  
├── benchmark_csv_vs_parquet.py     # Evaluación CSV vs Parquet  
│  
├── data_output/                    # Resultados generados por el pipeline  
│   ├── equipos.csv  
│   ├── equipos.parquet  
│   ├── ranking_ofensivo.csv  
│   ├── top_victorias.csv  
│   └── resumen_liga.csv  
│  
├── plots_output/                   # Gráficos interactivos exportados en HTML  
│   ├── goles_a_favor.html  
│   ├── diferencia_goles.html  
│   ├── puntos_vs_victorias.html 
│   ├── difgoles_vs_prompuntos.html  
│   ├── eficiencia_global_boxplot.html  
│   ├── eficiencia_global_facetado.html  
│   └── nube3d_puntos_victorias_difgoles.html  
│  
└── README.md                       # Documentación del proyecto  

## 5. Ampliación (Opcional)

## Fase exploratoria

Durante la fase inicial se ha trabajado también con Pandas para comprender el flujo completo antes de migrarlo a Polars. Por este motivo se conservan dos scripts auxiliares:

filtrado_pandas.py, que muestra el pipeline equivalente en Pandas y sirve como referencia comparativa para la ampliación de rendimiento.

graficos_pandas.py, utilizado para validar visualmente los datos filtrados en esa fase inicial. Aunque el análisis final se realiza con Polars y Plotly, ambos archivos se mantienen como parte del proceso exploratorio seguido.


## Benchmarking: Pandas vs Polars
Para comparar el rendimiento de ambas librerías se ha creado el script benchmark_pandas_vs_polars.py, que ejecuta la misma operación en Pandas y en Polars utilizando el dataset generado por Polars. 

La salida incluye también el número de filas del dataset, ya que en conjuntos pequeños los tiempos pueden variar entre ejecuciones y Pandas puede resultar competitivo debido a su menor coste de arranque y la diferencia real de rendimiento no se aprecia igual que en escenarios Big Data.

Los tiempos pueden fluctuar ligeramente en cada ejecución debido al tamaño reducido del dataset, la simplicidad de la operación y la propia gestión del sistema operativo.

## Benchmarking: CSV vs Parquet
Como parte de la ampliación solicitada, se ha evaluado también el rendimiento del formato Parquet frente al CSV. Para ello se ha creado un benchmark independiente que compara:
- Tamaño en disco
- Tiempo de lectura en Polars

El archivo equipos.parquet se genera exclusivamente para esta evaluación; no forma parte del pipeline principal.

Conclusiones

Aunque Parquet suele ser más eficiente en entornos Big Data, en este caso concreto el CSV es más ligero y rápido debido al tamaño reducido del dataset. En datasets pequeños, el coste fijo de la estructura interna de Parquet puede superar sus ventajas, dando lugar a: archivos algo mayores y tiempos de lectura ligeramente superiores

Aun así, se incluye la exportación en Parquet para evaluar su comportamiento en escenarios de mayor escala, donde sí ofrece mejoras en:

- compresión
- velocidad de acceso por columnas
- y eficiencia en cargas analíticas

## Análisis Extraído de los Gráficos

El análisis visual realizado con los distintos gráficos generados en Plotly permite identificar patrones claros sobre el rendimiento de los equipos en sus respectivas ligas. A partir de las métricas calculadas —Puntos, % de Victorias, Diferencia de Goles y Eficiencia Global— se observan relaciones consistentes que ayudan a interpretar tanto el estilo de juego como la eficacia competitiva de cada equipo.

El análisis, a través de las visualizaciones, revela tres puntos clave sobre el rendimiento de los equipos:

*Correlación Lineal Dif. Goles/Promedio de Puntos:* 
El gráfico de dispersión muestra una correlación positiva casi perfecta. Esto confirma que la "Diferencia de Goles" no es solo una métrica de desempate, sino un indicador predictivo del éxito. Los equipos con una diferencia superior a $+20$ rara vez caen por debajo del top 4 de sus ligas, teniendo un promedio de puntos elevado.

*Eficiencia en la Nube 3D:*
Al introducir el % de Victorias, observamos clusters de equipos. Los equipos en la parte superior del eje Z (Diferencia de Goles) y con alto % de victorias son los "dominadores absolutos". Aquellos con muchos puntos pero baja diferencia de goles sugieren una alta eficiencia defensiva (ganar por la mínima diferencia).

*Detección de Outliers:*
El gráfico 3D permite identificar equipos que tienen un alto porcentaje de victorias pero una diferencia de goles baja, lo que indica un estilo de juego más conservador.

Estos outliers son especialmente útiles para comprender comportamientos atípicos: equipos que ganan mucho pero por márgenes muy ajustados, o equipos que marcan mucho pero no logran convertir ese dominio en victorias consistentes.

*Comparación entre ligas mediante Eficiencia Global*
El boxplot de Eficiencia Global revela diferencias significativas entre ligas. Algunas presentan una mediana más alta, lo que indica mayor dominancia de los equipos punteros; otras muestran distribuciones más compactas, reflejando competiciones más equilibradas. La presencia de valores atípicos también ayuda a identificar ligas con equipos extremadamente dominantes o especialmente débiles.

*Conclusión general*
En conjunto, las visualizaciones permiten afirmar que:
La Diferencia de Goles es el indicador más sólido del rendimiento global.
El análisis multidimensional (3D) aporta una visión más rica del estilo de juego.
La Eficiencia Global permite comparar ligas completas, no solo equipos individuales.
Los outliers detectados ayudan a interpretar estrategias defensivas u ofensivas particulares.
Estas conclusiones complementan el análisis numérico y permiten una comprensión más profunda del comportamiento competitivo de los equipos.

## Instalación y Uso

1. *Clonar el repositorio*

```Bash
git clone <URL-del-repo>
cd <carpeta-del-repo>
```

2. *Instalar las dependencias*

Puedes elegir uno de los dos métodos:

Opción 1: Usando pip (requirements.txt)
```Bash
pip install -r requirements.txt
```

Opción 2: Usando uv (pyproject.toml)
```Bash
uv sync
```

3. *Generar la base de datos (obligatorio)*

Este paso crea o actualiza soccer.db a partir de la API

Con pip:
```Bash
python main.py
```

Con uv:
```Bash
uv run python main.py
```

4. *Procesar datos y generar visualizaciones*

Con pip:
```Bash
python filtrado_polars.py
python graficos_polars_analisis.py
```

Con uv:
```Bash
uv run python filtrado_polars.py
uv run python graficos_polars_analisis.py
```

### Autores

Proyecto desarrollado por Eva María García Gálvez y Pablo Baeza Gómez.







