import streamlit as st
import pandas as pd
import difflib
#from nltk import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import base64
import plotly.express as px

df = px.data.iris() 

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("./img/fondo.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("https://raw.githubusercontent.com/JoseTulcan/proyecto-final-automatizacion-y-control/7477858c19d499677d0f28b20490f561ebb8dcfd/fondo.jpg");
    background-size: 100%;
    background-position: top left;
    background-repeat: repeat;
    background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{img}");
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Cambiar el tamaño y color del texto
# Configuraciones para el título
title_style = """
    color: white;          /* Cambiar el color del título (por ejemplo, a verde) */
    font-size: 36px;       /* Cambiar el tamaño del título (por ejemplo, a 36px) */
    font-weight: bold;     /* Cambiar el grosor del título a negrita */
"""

# Configuraciones para el subtítulo
subtitle_style = """
    color: white;           /* Cambiar el color del subtítulo (por ejemplo, a azul) */
    font-size: 24px;       /* Cambiar el tamaño del subtítulo (por ejemplo, a 24px) */
    font-weight: bold;     /* Cambiar el grosor del subtítulo a negrita */
"""

# Mostrar el título de página
st.markdown(
    f"""
    <h1 style='{title_style}'>
        RECOMENDADOR DE PELÍCULAS
    </h1>
    """,
    unsafe_allow_html=True
)

# Carga de datos
movies_data = pd.read_csv('./datos_kaggle/movies.csv')

movies_data2 = pd.read_csv('./datos_IMDB/movie_metadata.csv')

movies_data2['index'] = movies_data2.index

# Normalizar las columnas antes de realizar la comparación
movies_data['title_normalized'] = movies_data['title'].str.lower().str.strip()
movies_data2['movie_title_normalized'] = movies_data2['movie_title'].str.lower().str.strip()

# Realizar un merge en las columnas normalizadas
merged_df = pd.merge(movies_data, movies_data2, how='inner', left_on='title_normalized', right_on='movie_title_normalized')

# Seleccionar las columnas deseadas
selected_columns = ['title', 'movie_imdb_link', 'keywords','tagline', 'cast', 'director']

# Guardar las coincidencias en una variable
result_df = merged_df[selected_columns]

# Iterando a través de cada fila en movies_data
for index, row in movies_data.iterrows():
    title_movies_data = row['title']

#Seleccionar las características(columnas) de la base de datos a consideración
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

#Asignación de las características no existentes con espacio vacío
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

#Combinar las características elegídas para el entrenamiento
combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']

#Vectorizar las características
vectorizer = TfidfVectorizer()

#Ajustar vectorizador y transformar textos en características
feature_vectors = vectorizer.fit_transform(combined_features)

#Aplicar el algoritmo de cosine similarity a las características
similarity = cosine_similarity(feature_vectors)

# Definir el nombre de la película usando la caja de texto
default_option = "Nombre de la película"

#Desplegar caja de selección o inserción de la película
movie_name = st.selectbox('## SELECCIONE O ESCRIBA EL NOMBRE DE LA PELÍCULA',
                          [default_option] + movies_data['title'].tolist(), key="movie_name", index=0)

#Almacenar todos los títulos de las películas en nueva variable
list_of_all_titles = movies_data['title'].tolist()

#Buescar coincidencias entre la película ingreasda y la base de datos
find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

#Cuando la película buscada está en la base de datos
if len(find_close_match) > 0:
    
    #Asignar la coincidencia a una variable
    close_match = find_close_match[0]

    #Asignación indexada de coincidencia de título de la base de datos y la coincidencia
    close_match_index = movies_data[movies_data.title == close_match].index[0]

    # Obtener una lista de tuplas que representan los índices y puntajes de similitud
    # de la película con índice close_match_index en relación con otras películas.
    similarity_score = list(enumerate(similarity[close_match_index]))

    #Ordenar de manera descendente las similitudes con las pelpiculas
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
 
    #Ajusta el valor del margen según del título de número de películas
    margin_value = "-50px"

    #Título de caja elección número de películas recomendadas que se desea
    st.markdown(f'<h3 style="color:white; margin-bottom: {margin_value};">Número de películas</h3>',
                unsafe_allow_html=True)
    
    #Definir mínimo, máximo y valor por defecto del número de películas recomendadas
    num_recommendations = st.number_input('', min_value=5, max_value=30, value=10, format="%d", key="num_recommendations")

    #Título para mostrar películas recomendadas
    st.markdown('## Películas recomendadas:')

    #Mostrar los nombres de las películas en 4 columnas
    cols = st.columns(4)

    #Obtener el índice y el título de mayor a menor nivel de coincidencia
    for i, movie in enumerate(sorted_similar_movies[:num_recommendations]):

        #Asignar título a variable index
        index = movie[0]

        #Obtener el título de la película correspondiente al índice index en la base de datos
        title = movies_data[movies_data.index == index]['title'].values[0]
 
        # Búsqueda aproximada 
        #Asignar los títulos de result_df a movie_titles
        movie_titles = result_df['title'].tolist()

        #Closest_match contendrá el título de la película más cercana al título proporcionado en la variable title
        closest_match = difflib.get_close_matches(title, movie_titles)[0]

        #Asignar a movie_row la fila en result_df de la peelícula más cercana a la ingresada
        movie_row = result_df[result_df['title'] == closest_match]

        #Asignar el enlace de la película si la fila no está vacía
        if not movie_row.empty:
            imdb_link = movie_row['movie_imdb_link'].values[0]
        
        #Si la fila está vacía dejar igual
        else:
            imdb_link = ""

        #Mostrar título y enlace de cada película recomendada
        with cols[i % 4]:
            st.header(title)
            st.write(f"IMDB: {imdb_link}")
        
else:  
    #Crear estilo con CSS para mostrar advertencia 
    css = """
    <style>
        .warning-box {
            background-color: #ffcccb; /* Color de fondo personalizado */
            padding: 1em;
            border-radius: 10px; /* Bordes redondeados */
            border: 2px solid #8b0000; /* Color del borde */
            color: #8b0000; /* Color del texto */
        }
    </style> 
    """

    # Inyectar estilos CSS
    st.markdown(css, unsafe_allow_html=True)

    # Mensaje de advertencia personalizado
    st.markdown('<div class="warning-box">NO SE ENCONTRÓ UNA COINCIDENCIA APROXIMADA!!</div>', unsafe_allow_html=True)

