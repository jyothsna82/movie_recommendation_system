import streamlit as st
import requests
import pickle as pkl
import time

# TMDb API Key (Replace with your actual API key)
API_KEY = "bb5703d2991d4b48df385f4e268c44c9"

# Headers to prevent API blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to fetch movie poster
def fetch_poster(movie_title):
    """Fetch movie poster with retries to avoid API disconnection."""
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"

    with requests.Session() as session:
        for _ in range(3):  # Retry up to 3 times
            try:
                response = session.get(search_url, headers=HEADERS, timeout=5)
                response.raise_for_status()
                data = response.json()

                if data.get("results"):
                    poster_path = data["results"][0].get("poster_path", "")
                    if poster_path:
                        return f"https://image.tmdb.org/t/p/w500{poster_path}"
                return "https://via.placeholder.com/150?text=No+Image"

            except requests.exceptions.RequestException:
                time.sleep(2)  # Wait before retrying

    return "https://via.placeholder.com/150?text=Error"

# Function to fetch Telugu movie recommendations
def fetch_tmdb_recommendations(movie_title, num=5):
    """Fetch similar Telugu movie recommendations from TMDb API"""
    
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    
    with requests.Session() as session:
        try:
            response = session.get(search_url, headers=HEADERS, timeout=5)
            response.raise_for_status()
            data = response.json()

            if not data.get("results"):
                return []

            movie_id = data["results"][0]["id"]
            genre_ids = data["results"][0].get("genre_ids", [])  # Extract genres

            # ✅ **Step 1: Try fetching similar movies**
            similar_url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={API_KEY}"
            similar_response = session.get(similar_url, headers=HEADERS, timeout=5).json()

            tmdb_movies = []
            for movie in similar_response.get("results", []):
                if movie["original_language"] == "te":  # Ensure it's Telugu
                    tmdb_movies.append((movie["title"], fetch_poster(movie["title"])))

            # ✅ If similar Telugu movies are found, return them
            if tmdb_movies:
                return tmdb_movies[:num]

            # ✅ **Step 2: Fallback to Discover API with genre filtering**
            genre_filter = f"&with_genres={','.join(map(str, genre_ids))}" if genre_ids else ""
            discover_url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_original_language=te{genre_filter}&sort_by=popularity.desc"
            discover_response = session.get(discover_url, headers=HEADERS, timeout=5).json()

            for movie in discover_response.get("results", [])[:num]:
                tmdb_movies.append((movie["title"], fetch_poster(movie["title"])))

            return tmdb_movies

        except requests.RequestException as e:
            st.error(f"API Error: {e}")
            return []
    
    return []

# Load dataset & similarity matrix
movies = pkl.load(open('movies.pkl', 'rb'))  # Keep as a DataFrame
similarity = pkl.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("🎬 Movie Recommendation System")

movie_name = st.text_input("Enter a Movie Name (Telugu or English)")

if st.button("Show Recommendation"):
    if movie_name:
        recommendations = fetch_tmdb_recommendations(movie_name)

        if recommendations:
            cols = st.columns(len(recommendations))  # Adjust layout dynamically
            for idx, col in enumerate(cols):
                with col:
                    st.text(recommendations[idx][0])
                    st.image(recommendations[idx][1])
        else:
            st.warning("⚠️ No Telugu recommendations found. Try another movie!")
    else:
        st.warning("🔎 Please enter a movie name.")
