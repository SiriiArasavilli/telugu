import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch poster using movie name
def fetch_poster(movie_name):
    # Use The Movie Database (TMDb) Search API to get the movie ID
    response = requests.get(
        f'https://api.themoviedb.org/3/search/movie?api_key=c56ff6fab04f4dfc235ce9cfc19c14c7&query={movie_name}'
    )
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            movie_id = data['results'][0]['id']
            poster_path = data['results'][0].get('poster_path', '')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750.png?text=No+Image"

# Function to recommend movies
def recommend(movie_name):
    try:
        # Get the index of the selected movie
        movie_index = movies[movies['Movie'] == movie_name].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            # Get the movie name
            recommended_movie_name = movies.iloc[i[0]].Movie
            recommended_movies.append(recommended_movie_name)
            # Fetch poster using the movie name
            recommended_movies_posters.append(fetch_poster(recommended_movie_name))
        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("Movie not found in the dataset.")
        return [], []
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return [], []

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

# Dropdown for movie selection
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['Movie'].values
)

# Recommendation button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display recommendations in columns
    if names:
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
    else:
        st.warning("No recommendations available.")
