# RECOMENDADOR DE PELÍCULAS CON MACHINE LEARNING. 
# Proyecto final - Asignatura: Automatización y Control

## Creadores:

### José Luis Mera Tulcán - Deyson Mauricio Laos S.

Este proyecto consiste en la elaboración de un recomendador de películas usando el algoritmo Cosine similarity con una interfaz creada mediante Streamlit

[![Imagen representativa](img/fondo.jpg)](img/fondo.jpg)

## Objetivos
- Automatizar la busqueda de películas de características similares a la ingresada
- Crear una interfaz con Streamlit que permita la visualización de las películas recomendadas

## Descripción 
Se dispone una base de datos obtenida desde Kaggle [**movies_kaggle.csv**](./datos_kaggle/movies.csv) que contiene el catálogo de películas que se usan en el entrenamiento del algoritmo de recomendación además de otra información de cada película, como generos, actores de reparto, director, descripción, y otros más. Tambien se cuenta con una base de datos de IMDB [**movies_IMDb.csv**](./datos_IMDb/movie_metadata.csv) que contiene un catálogo similar de pellículas con la diferencia de que dispone de un enlace para cada película que al hacer clic en el lleva a la plataforma de IMDb, permitiendo así al usuario tener toda la información de la película recomendada que es de su interés incluyendo el trailer de cada película. 

### CONSTRUCCIÓN DEL MODELO DE RECOMENDACIÓN

1. IMPORTACIÓN DE LIBRERÍAS
Se importa las librerías necesarias para los siguientes propósitos:
    - Creación de interfaz en Streamlit
    - Vectorización de datos
    - Algoritmo Cosine similarity
    - Manejo de datos y de imagenes

2. CARGA DE DATOS 
Se carga los datos de las dos bases de datos y se asingan las películas que estén en las dos bases a una nueva variable.
Una vez cargados los datos, se seleccionan las columnas o características que se usarán en el entrenamiento del algoritmo.
Con la selección de las características lista es posible verificar las filas vacías y continuar en el siguiente paso.

3. VECTORIZACIÓN DE DATOS
Los datos seleccionados deben ser vectorizados, es decir que el texto que conforma los titulos de las películas debe convertirse en vectores numéricos que representan las características.

4. SIMILITUD COSENO
Con los datos vectorizados se puede ya hacer la aplicación del algoritmo de cosine similarity. Cuando el usuario ingresa una película se evalua si hay coincidencias con la base de datos, si es así se procede a ordenar las películas incluyendo sus indices por similitud con la película ingresada. 

5. RECOMENDACIÓN DE PELÍCULAS
Dado que ya se tiene la lista de películas similares, es decir las que se va a recomendar por su cercania en sus características, se consulta con el nombre de estas películas en la variable donde se guardan las películas que están en las dos bases de datos y se extrae el enlace de cada película. Finalmente son mostrados en la interfaz.

## Resultados
Se hicieron diferentes pruebas con seleccionando o ingresando diferentes películas de la base de datos, y para los diferentes casos se pudo observar que el algoritmo entrega otros títulos de películas en orden descendente por su similitud en las características de las películas que fueron seleccionadas. Además la interfaz permite aumnetar o disminuir correctamente el número de películas recomendadas.
 
Se muestra a continuación la interfaz de este proyecto de recomendadr de películas.

[![Imagen representativa](img/interfaz1.JPG)](img/interfaz1.JPG)

Ahora observemos un ejemplo de como se ve el modelo en acción.

[![Imagen representativa](img/interfaz2.JPG)](img/interfaz2.JPG)

## Conclusiones
Es posible construir un modelo de recomendación de películas basado en nuestra película favorita o película de interés usando el algoritmo de similitud de coseno. 
Es importante mencionar que este modelo de recomendación funciona bien para este propósito, aunque puede mejorar en diferentes aspectos como incluir imagenes de cada película en la interfaz, y reducir el uso de las bases de datos a solo una, entre otras que considere oportuna.