import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8& language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

model = pickle.load(open('model.pkl', 'rb'))
vectors = pickle.load(open('vectors.pkl', 'rb'))
movies_dict = pickle.load(open('movies_list_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances, indices = model.kneighbors(
        vectors[movie_index],
        n_neighbors=6
    )

    recommended_movies = []
    recommended_movies_posters = []

    for i in indices[0][1:]:
        movie_id = movies.iloc[i].movie_id
        recommended_movies.append(movies.iloc[i].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

st.title('Movie Recommendation System')

option = st.selectbox(
    "which movie did u likee?",
    movies['title'].values
)

st.write("You selected:", option)

if st.button(f"Recommend more movies like '{option}'"):
    names,posters = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

