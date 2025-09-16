import requests
import streamlit as st
import pickle
movies_list = pickle.load(open("movie_list.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))
movies = movies_list['title'].values

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)  # timeout in seconds
        response.raise_for_status()  # raise error for 4xx/5xx
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movies_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies_names.append(movies_list.iloc[i[0]].title)

    return recommended_movies_names,recommended_movie_posters

st.title("Movie Recommender System")
selected_movie_name = st.selectbox(
    "Select a movie to find similar ones !",
    movies,
)
if st.button('Recommend'):
     recommended_movies_names,recommended_movie_posters = recommend(selected_movie_name)
     col1,col2,col3,col4,col5 = st.columns(5)
     with col1 :
        st.text(recommended_movies_names[0])
     with col2:
        st.text(recommended_movies_names[1])
     with col3:
        st.text(recommended_movies_names[2])
     with col4:
        st.text(recommended_movies_names[3])
     with col5:
        st.text(recommended_movies_names[4])