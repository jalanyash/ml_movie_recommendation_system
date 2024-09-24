import streamlit as st
import pickle
import requests
import pandas as pd
import nbformat
from nbconvert import PythonExporter

def run_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb_content = nbformat.read(f, as_version=4)
    
    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb_content)

    exec(source, globals())
    return similarity  # Adjust according to how `similarity` is defined

similarity = run_notebook('model-training.ipynb')
st.title('Movie Recommender System')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    print(data)
    # poster_path = data['poster_path']
    poster_path = data.get('poster_path')
    # full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    # return full_path
    if poster_path:  # Check if poster_path exists
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = "path/to/default/image.jpg"  # Provide a default image URL or path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] ==movie].index[0]
    distances = similarity[movie_index]
    movies_list= sorted(list(enumerate(distances)), reverse=True, key = lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # movie_id= i[0]
        movie_id = movies.iloc[i[0]].movie_id 
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movies_dic.pkl','rb'))
movies=pd.DataFrame(movies_dict)

# similarity =  pickle.load(open('similarity.pkl','rb'))
selected_movie_name= st.selectbox(
    'closest recommendation of this movie',
    movies['title'].values 
)
if st.button('Recommend'):
    recommended_movies,recommended_movies_posters= recommend(selected_movie_name)
  

    # Loop through the recommendations in groups of three
    for i in range(0, len(recommended_movies), 3):
        col1, col2, col3 = st.columns(3)  # Create three columns for each row
        
        with col1:
            if i < len(recommended_movies):  # Check if the movie exists
                st.text(recommended_movies[i])
                st.image(recommended_movies_posters[i])

        with col2:
            if i + 1 < len(recommended_movies):  # Check if the next movie exists
                st.text(recommended_movies[i + 1])
                st.image(recommended_movies_posters[i + 1])

        with col3:
            if i + 2 < len(recommended_movies):  # Check if the third movie exists
                st.text(recommended_movies[i + 2])
                st.image(recommended_movies_posters[i + 2])
    # col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])  # Equal widths

    # with col1:
    #     st.text(recommended_movies[0])
    #     st.image(recommended_movies_posters[0])
    # with col2:
    #     st.text(recommended_movies[1])
    #     st.image(recommended_movies_posters[1])

    # with col3:
    #     st.text(recommended_movies[2])
    #     st.image(recommended_movies_posters[2])
    # with col4:
    #     st.text(recommended_movies[3])
    #     st.image(recommended_movies_posters[3])
    # with col5:
    #     st.text(recommended_movies[4])
    #     st.image(recommended_movies_posters[4])