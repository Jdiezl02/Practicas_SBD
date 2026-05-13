import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial import distance
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go

# Configuración básica de la app de Streamlit.
# Aquí definimos el título de la pestaña y el diseño general (ancho completo).
st.set_page_config(page_title="Centro de Inteligencia", layout="wide")

# Cargamos el dataset de jugadores.
# @st.cache_data hace que Streamlit guarde el resultado en caché
# para no estar leyendo el CSV cada vez que se recarga la app.
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "players_data.csv")
    return pd.read_csv(file_path)

df = load_data()

# Estas son las variables que vamos a usar para comparar jugadores.
# Básicamente son las “estadísticas importantes” del análisis.
features = [
    "Goles",
    "Asistencias",
    "Pases_%",
    "Regates",
    "Recuperaciones",
    "xG",
    "Potencial"
]

# Normalizamos los datos para que todas las métricas estén en la misma escala (0 a 1).
# Esto es clave porque si no, variables grandes como “Pases” dominarían el análisis.
scaler = MinMaxScaler()
df_scaled = df.copy()
df_scaled[features] = scaler.fit_transform(df[features])

# Panel lateral donde el usuario puede filtrar y seleccionar el jugador objetivo.
st.sidebar.title("🧭 Panel de Control")

# Filtros básicos por edad y valor de mercado.
min_edad = st.sidebar.slider(
    "Edad mínima",
    int(df["Edad"].min()),
    int(df["Edad"].max()),
    18
)

max_valor = st.sidebar.slider(
    "Valor máximo",
    int(df["Valor_Mercado"].min()),
    int(df["Valor_Mercado"].max()),
    int(df["Valor_Mercado"].max())
)

# Selección del jugador que vamos a usar como referencia.
jugador_objetivo = st.sidebar.selectbox(
    "Selecciona jugador objetivo",
    df["Nombre"].tolist()
)

# Aplicamos los filtros al dataset (aunque aquí no se usa después directamente).
df_filtered = df[
    (df["Edad"] >= min_edad) &
    (df["Valor_Mercado"] <= max_valor)
]

# Sacamos el vector de características del jugador seleccionado.
# Es decir, sus valores normalizados en las estadísticas.
target_vector = df_scaled[
    df_scaled["Nombre"] == jugador_objetivo
][features].values[0]

# Función que calcula qué jugadores son más parecidos al objetivo.
# Lo hacemos con distancia euclidiana en el espacio de características.
def calcular_similitud(df_scaled, target_vector):
    distancias = []

    # Recorremos todos los jugadores y calculamos su distancia al objetivo
    for i in range(len(df_scaled)):
        vec = df_scaled.iloc[i][features].values
        dist = distance.euclidean(target_vector, vec)
        distancias.append(dist)

    # Añadimos la distancia al dataframe original para poder ordenar
    df_result = df.copy()
    df_result["Distancia"] = distancias

    # Ordenamos de más parecido a menos parecido
    return df_result.sort_values("Distancia")

# Ejecutamos la comparación
resultados = calcular_similitud(df_scaled, target_vector)

# Nos quedamos con los 5 jugadores más similares (quitando el propio jugador)
top5 = resultados[resultados["Nombre"] != jugador_objetivo].head(5)

# Título principal de la aplicación
st.title("🧠 Centro de Inteligencia de la Alianza Shinobi")

# Dividimos la pantalla en dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("📡 Perfil del objetivo")

    fig = go.Figure()

    # Representamos el jugador seleccionado en un gráfico tipo radar
    fig.add_trace(go.Scatterpolar(
        r=df_scaled[df_scaled["Nombre"] == jugador_objetivo][features].values[0],
        theta=features,
        fill='toself',
        name=jugador_objetivo
    ))

    # Ajustes visuales del radar
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 5 candidatos más similares")

    # Mostramos los jugadores más parecidos con sus distancias
    st.dataframe(top5[["Nombre", "Edad", "Equipo", "Distancia"]])

st.subheader("🌱 Rastreo de cantera (U25 con alto potencial)")

# Filtramos jugadores jóvenes con potencial alto
promesas = df[(df["Edad"] <= 25) & (df["Potencial"] > 70)]

st.dataframe(promesas[["Nombre", "Edad", "Potencial", "Equipo"]])

st.subheader("🧩 Agrupamiento táctico")

# Aplicamos KMeans para agrupar jugadores en clusters según su estilo
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)

df_scaled["Cluster"] = kmeans.fit_predict(df_scaled[features])

# Representamos visualmente los grupos
fig2 = px.scatter(
    df_scaled,
    x="Potencial",
    y="Goles",
    color=df_scaled["Cluster"].astype(str),
    hover_data=["Nombre"]
)

st.plotly_chart(fig2, use_container_width=True)