import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = "https://via.placeholder.com/500x750?text=No+Image"
    return full_path

# Load data
try:
    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
except FileNotFoundError:
    st.error("Required files `movies_list.pkl` or `similarity.pkl` not found.")

# Dropdown list
movies_list = movies['title'].values if 'title' in movies else []

st.header("Movie Recommender System")

# Image Carousel
imageCarouselComponent = components.declare_component("image-carousel-component", path="./frontend/public")
imageUrls = [fetch_poster(movie_id) for movie_id in [1632, 299536, 17455, 2830, 429422, 9722, 13972, 240, 155, 598, 914, 255709, 572154]]
imageCarouselComponent(imageUrls=imageUrls, height=200)

# Movie selector
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    if 'title' not in movies or 'id' not in movies:
        return [], []
    try:
        index = movies[movies['title'] == movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        recommend_movie = []
        recommend_poster = []
        for i in distance[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_poster.append(fetch_poster(movie_id))
        return recommend_movie, recommend_poster
    except IndexError:
        st.error("Selected movie not found in the database.")
        return [], []

if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    for idx in range(min(5, len(movie_name))):  # Adjust if less than 5 recommendations
        col = st.columns(5)[idx]
        with col:
            st.text(movie_name[idx])
            st.image(movie_poster[idx])
