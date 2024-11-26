import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from transformers import pipeline

# Título de la aplicación
st.title("MoodTrack: Análisis Emocional de Canciones")

# Inicializamos la variable `sp`
sp = None

# 1. Configuración de credenciales de Spotify
st.sidebar.header("Configuración de Spotify")
client_id = st.sidebar.text_input("Client ID")
client_secret = st.sidebar.text_input("Client Secret", type="password")

if client_id and client_secret:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))
        st.sidebar.success("Autenticado correctamente.")
    except Exception as e:
        st.sidebar.error("Error en la autenticación. Verifica las credenciales.")

# 2. Selección de playlist
if sp:  # Verificar que `sp` se haya inicializado correctamente
    playlist_url = st.text_input("Introduce la URL de una playlist de Spotify:")
    if st.button("Cargar Playlist"):
        try:
            # Obtener datos de la playlist
            playlist_id = playlist_url.split("/")[-1].split("?")[0]
            playlist = sp.playlist(playlist_id)
            tracks = playlist['tracks']['items']
            data = [
                {
                    "Track": track['track']['name'],
                    "Artist": track['track']['artists'][0]['name'],
                    "ID": track['track']['id']
                } for track in tracks
            ]
            df = pd.DataFrame(data)
            st.write("Datos de la Playlist:", df)
        except Exception as e:
            st.error("Error al cargar la playlist. Verifica el enlace.")

# 3. Análisis de sentimiento
st.header("Análisis de Sentimiento")
if 'df' in locals():
    analyzer = pipeline("sentiment-analysis")
    if st.button("Analizar Sentimientos"):
        df['Sentiment'] = df['Track'].apply(lambda x: analyzer(x)[0]['label'])
        st.write("Resultados del Análisis de Sentimiento:", df)

# 4. Visualización
if 'df' in locals() and 'Sentiment' in df.columns:
    st.header("Visualización de Resultados")
    sentiment_counts = df['Sentiment'].value_counts()
    st.bar_chart(sentiment_counts)
