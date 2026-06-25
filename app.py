import pickle
import streamlit as st
import requests

def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = "https://via.placeholder.com/500x750?text=No+Poster"
    return full_path, data.get('overview', 'No description available.')

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_overviews = []
    for i in distances[1:6]:
        # fetch the movie poster and details
        movie_id = movies.iloc[i[0]].movie_id
        poster, overview = fetch_movie_details(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_overviews.append(overview)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_overviews

st.header('Movie Recommender System')
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    names, posters, overviews = recommend(selected_movie)
    cols = st.columns(5)
    
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
            with st.expander("Description"):
                st.write(overviews[i])
