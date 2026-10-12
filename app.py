

import streamlit as st
import pickle
import pandas as pd
import requests
import base64

def fetch_poster(movie_id):
    url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b1f5e37a64473be910b84012e5a33bad&language=en-US"
    response=requests.get(url)
    data=response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data["poster_path"]

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies=[]
    recommend_posters = []
    for i in movies:
        movie_id=movies_list.iloc[i[0]].movie_id
        recommend_movies.append(movies_list.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
    return recommend_movies,recommend_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies_list = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

with open("movie_bg.jpg", "rb") as f:
    encoded_image = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(
                rgba(10, 10, 20, 0.80),
                rgba(10, 10, 20, 0.90)
            ),
            url("data:image/jpeg;base64,{encoded_image}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    h1 {{
        color: white;
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Movie Recommender System")
selected_movie_name=st.selectbox('Search your Movie',movies_list['title'].values)


if st.button('Recommend'):
    names,poster = recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])