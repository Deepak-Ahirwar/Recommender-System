import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MjMwY2Y3NWU2NDgzMzcwMjNmOTIxYWI5ZGM2MDBmNCIsInN1YiI6IjY1MzI1NmQ5NmY4ZDk1MDEwYmJkMDAyNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.iSOaWuZcnEhH0P3aT0TJ_zI1-aIQD3v-pQzhL_Q3T88"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return "https://image.tmdb.org/t/p/w780/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']== movie].index[0]  
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6:]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # Get poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

movies_list = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movies Recommender System')

selected_movie_name = st.selectbox('Movies',movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1,col2,col3,col4,col5 = st.columns(5)
    
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
