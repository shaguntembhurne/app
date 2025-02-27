import pickle
import streamlit as st
import requests
import pandas as pd
import gdown
import os

# Download similarity.pkl from Google Drive
url = "https://drive.google.com/file/d/1Sb-qrnJBfZDBNUZXP8C2B1jVn9isgg3Q/view"
output = "similarity.pkl"
if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

# Function to fetch movie posters from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return "https://via.placeholder.com/500"  # Default placeholder if API fails
    data = response.json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return "https://via.placeholder.com/500"  # Return placeholder if no poster found
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit App Header
st.header('🎬 Movie Recommender System')

# Load Movies Data
if os.path.exists('movies_dict.pkl'):
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    if isinstance(movies_dict, dict):
        movies = pd.DataFrame(movies_dict)
    else:
        movies = movies_dict
else:
    st.error("Error: 'movies_dict.pkl' not found!")
    st.stop()

# Load Similarity Data
if os.path.exists('similarity.pkl'):
    similarity = pickle.load(open('similarity.pkl', 'rb'))
else:
    st.error("Error: 'similarity.pkl' not found!")
    st.stop()

# Check if 'title' column exists in movies
if 'title' not in movies.columns:
    st.error("Error: 'title' column missing in movies_dict.pkl. Please check the data format.")
    st.stop()

# Movie Selection Dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("\ud83c\udfa5 Type or select a movie:", movie_list)

# Show Recommendations on Button Click
if st.button('\ud83d\udd0d Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Create 5 columns for displaying recommendations
    cols = st.columns(5)
    
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
