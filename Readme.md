Análisis de datos de ligas de fútbol
Este proyecto realiza un proceso de extracción, transformación, carga y análisis visual de estadísticas de equipos de fútbol utilizando una base de datos SQLite y Polars.

Características
Ingesta: Uso de Polars para manejar grandes volúmenes de datos desde SQL, en este caso SQLite.

Ingeniería de variables: Cálculo de métricas avanzadas como % de Victorias, Diferencia de Goles y Promedio de Puntos por Partido.

Visualización Interactiva: Gráficos 3D y de dispersión utilizando Plotly para identificar patrones de rendimiento. Los Gráficos se exportan en un HTML interactivo que se abre directamente en el navegador. Ambos gráficos son interactivos, en el caso de Scatter3D se permite analizar el gráfico en tres dimensiones, y en el segundo gráfico se puede seleccionar un tramo para ampliar la vista sobre una zona específica.

Instalación y Uso
Clona este repositorio.

Instala las dependencias:

Bash
pip install -r requirements.txt

Ejecuta el script principal:

Bash
python main.py
python filtrado_polars.py
python graficos_polars_interactivo.py

Visualizaciones Incluidas
Scatter Plot 2D: Relación entre la Diferencia de Goles y el Promedio de los Puntos por Partido. Ideal para ver la consistencia del equipo.

Scatter Plot 3D: Un análisis multidimensional que cruza Puntos, Porcentaje de Victorias y Diferencia de Goles para clasificar el dominio de los equipos.

Análisis Extraído de los Gráficos:
El análisis realizado a través de las visualizaciones revela tres puntos clave sobre el rendimiento de los equipos:
Correlación Lineal Dif. Goles/Promedio de Puntos: El gráfico de dispersión muestra una correlación positiva casi perfecta. Esto confirma que la "Diferencia de Goles" no es solo una métrica de desempate, sino un indicador predictivo del éxito. Los equipos con una diferencia superior a $+20$ rara vez caen por debajo del top 4 de sus ligas, teniendo un promedio de puntos elevado.
Eficiencia en la Nube 3D: Al introducir el % de Victorias, observamos clusters de equipos. Los equipos en la parte superior del eje Z (Diferencia de Goles) y con alto % de victorias son los "dominadores absolutos". Aquellos con muchos puntos pero baja diferencia de goles sugieren una alta eficiencia defensiva (ganar por la mínima diferencia).
Detección de Outliers: El gráfico 3D permite identificar equipos que tienen un alto porcentaje de victorias pero una diferencia de goles baja, lo que indica un estilo de juego más conservador.


Autores

Proyecto desarrollado por Eva María García Gálvez y Pablo Baeza Gómez.
