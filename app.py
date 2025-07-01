import streamlit as st
import pickle
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
import requests


def recomend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    sorted_movie_lists = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:8]
    
    recomend = []

    for i in sorted_movie_lists:
        recomend.append(movies_df.iloc[i[0]].title)
        #print(movies.iloc[i[0]].title)
    
    return recomend

def fetch_poster_and_url(movie_title):
    api_key = "676e9c75f70efd7883cff8fb358c2629"
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            movie_data = data['results'][0]
            poster_path = movie_data.get('poster_path')
            movie_id = movie_data.get('id')
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/200x300?text=No+Image"
            movie_url = f"https://www.themoviedb.org/movie/{movie_id}" if movie_id else "#"
            return poster_url, movie_url
    return "https://via.placeholder.com/200x300?text=No+Image", "#"

# Load data
movies_df = pickle.load(open('movies.pkl', 'rb')) # it's the data frame
movie_titles = movies_df['title'].values # it's the name of the movies
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set page config with a custom background color
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for background and card styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fa;
    }
    .movie-card {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        padding: 1.2em 1.5em;
        margin-bottom: 1em;
        font-size: 1.1em;
    }
    .reco-title {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 1.2em;
    }
    /* Custom button styles */
    .stButton > button {
        background: linear-gradient(90deg, #ff5858 0%, #f09819 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 2em;
        font-size: 1.1em;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(255,88,88,0.15);
        transition: transform 0.1s, box-shadow 0.2s, background 0.2s;
        cursor: pointer;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #f09819 0%, #ff5858 100%);
        transform: scale(1.06);
        box-shadow: 0 4px 16px rgba(255,88,88,0.25);
    }
    .stButton > button:active {
        background: #ff5858;
        transform: scale(0.98);
        box-shadow: 0 1px 4px rgba(255,88,88,0.15);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with info
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/movie-projector.png", width=80)
    st.title("🎬 Movie Recommender")
    st.markdown("""
    **How to use:**
    1. Select a movie from the dropdown.
    2. Click **Recommend** to get similar movies.
    3. Enjoy your next watch! 🍿
    """)
    st.markdown("---")
    st.markdown("Made by **Jishnudip Saha**")
    st.markdown("""
    <div style='font-size: 0.95em; margin-top: 1em;'>
    <b>About this ML Model:</b><br>
    This movie recommender uses content-based filtering with NLP techniques to analyze movie overviews and metadata. It suggests movies similar to your selection by comparing feature vectors using cosine similarity.
    </div>
    """, unsafe_allow_html=True)

# Main header
colored_header("🔥 Movie Recommendation System", description="Find your next favorite movie!", color_name="red-70")

# Movie selection
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    selected_movie_name = st.selectbox(
        "Enter your movie name:",
        movie_titles,
        help="Start typing to search for a movie."
    )
with col2:
    st.write("")
    st.write("")
    recommend_btn = st.button("🎯 Recommend", type="primary")

st.markdown("<hr>", unsafe_allow_html=True)

if selected_movie_name:
    st.success(f"You selected: **{selected_movie_name}**")

if recommend_btn:
    recomendations = recomend(selected_movie_name)
    st.markdown('<div class="reco-title">Recommended Movies:</div>', unsafe_allow_html=True)
    reco_cols = st.columns(3)
    for idx, movie in enumerate(recomendations):
        with reco_cols[idx % 3]:
            poster_url, movie_url = fetch_poster_and_url(movie)
            st.markdown(f'<a href="{movie_url}" target="_blank"><img src="{poster_url}" width="180" style="display:block;margin-left:auto;margin-right:auto;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.08);"></a>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center;"><a href="{movie_url}" target="_blank" style="color:inherit;text-decoration:none;"><b>{movie}</b></a></div>', unsafe_allow_html=True)

