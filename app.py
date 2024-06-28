import streamlit as st
import joblib
import pandas as pd
import requests

# Load data
movies = joblib.load("df.pkl")
similarity = joblib.load("similarity.pkl")
st.set_page_config(layout="wide")
def poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=0cd0181a7e0c2be38a8a37717b6f8b92&language=en-US".format(movie_id)
     data=requests.get(url)
     data=data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
     overview = data["overview"]
     return [full_path,overview]

st.markdown("""
<style>
.stColumnStyle {
    margin-right: 1000px;  /* Adjust as needed */
}
</style>
""", unsafe_allow_html=True)

# Function to recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    # Sort movies based on similarity
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_movie=[]
    recommend_poster=[]
    overview = []
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        k = poster(movies_id)
        recommend_poster.append(k[0])
        overview.append(k[1])
    return recommend_movie, recommend_poster,overview
# Streamlit app
st.markdown("""
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Displaying centered text
st.markdown('<h1 class=centered-text >Movie Reccomendation System</h1>', unsafe_allow_html=True)
st.image("/Users/yashahuja/Documents/Movie Reccomendation System/Movie Recommendation.png",width=1200)
# Dropdown to select a movie
selected_movie = st.selectbox("Select your favourite movie", options=movies["title"])

# Button to trigger recommendations
if st.button("Show more movies like this"):
    recommendations,posters,overview = recommend(selected_movie)
    # Display recommendations in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(recommendations[0])
        st.image(posters[0])
        st.write(overview[0])
    with col2:
        st.write(recommendations[1])
        st.image(posters[1])
        st.write(overview[1])
    with col3:
        st.write(recommendations[2])
        st.image(posters[2])
        st.write(overview[2])
    with col4:
        st.write(recommendations[3])
        st.image(posters[3])
        st.write(overview[3])
    with col5:
        st.write(recommendations[4])
        st.image(posters[4])
        st.write(overview[4])
