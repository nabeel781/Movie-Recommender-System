import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ------------------- Page Setup -------------------
st.set_page_config(page_title="MovieBox Recommender", layout="wide")

# ------------------- CSS Styling -------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Main title */
    .main-title {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        color: white;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }

    /* Section headings */
    .category-title {
        font-size: 1.4rem;
        font-weight: bold;
        margin: 2rem 0 1rem;
        color: #f0f0f0;
    }

    /* Posters */
    .movie-title {
        font-size: 1rem;
        margin-top: 0.5rem;
        color: #ffffff;
        text-align: center;
    }

    .stImage img {
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(255, 255, 255, 0.15);
    }

    /* Recommend Button */
    .stButton>button {
        background-color: #ffffff !important;
        color: black !important;
        font-weight: bold !important;
        font-size: 1.1rem;
        padding: 12px 28px;
        border-radius: 10px;
        border: 2px solid #ffffff;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #e6e6e6 !important;
        border-color: #e6e6e6;
    }

    /* Footer */
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 0.9rem;
        color: #888;
        padding: 20px 0;
        border-top: 1px solid #222;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- Title -------------------
st.markdown("<div class='main-title'>🎬 MovieBox Recommender</div>", unsafe_allow_html=True)

# ------------------- Helper Functions -------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', "")
    return "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else ""

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# ------------------- Load Data -------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
movies_dict = pickle.load(open(os.path.join(current_dir, 'movies_dict.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(current_dir, 'similarity.pkl'), 'rb'))
movies = pd.DataFrame(movies_dict)

# ------------------- Recommendation Section -------------------
st.markdown("<div class='category-title'>🎯 Get Your Recommendations</div>", unsafe_allow_html=True)
selected_movie_name = st.selectbox("Choose a movie", movies['title'].values)

if st.button("Recommend"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i], use_column_width='always')
            st.markdown(f"<div class='movie-title'>{recommended_movie_names[i]}</div>", unsafe_allow_html=True)

# ------------------- Footer -------------------
st.markdown("""
    <div class='footer'>
        © 2025 MovieBox — Built for Demo. Only “Recommend” is functional.
    </div>
""", unsafe_allow_html=True)
