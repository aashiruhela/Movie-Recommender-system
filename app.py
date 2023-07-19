# can also use flask but here using streamlit
import streamlit as st
import pickle
import pandas as pd
import requests # for requesting api's

# FETCH POSTERS :
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=cd56bdb6f226f4e36efe0f343aeea570&language=en-US'.format(movie_id))
    #  instead of 65 just put a bracket in movie id
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

# making function : to recommend BEST 5 movies for a selected movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # 0 k lie 5 most recommended movies

    recommend_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # movie_id = i[0] --- ye karoge toh error aiga kyunki 0,1,2,3 - ye id nai hai: Id voh hai jo recommend hori hai
        movie_id = movies.iloc[i[0]].movie_id  # movie id vala column dena hai
        recommend_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_posters
# now we have to bring movies list from jupyter file to here for WEBSITE code
# We will use pickle library for this

movies_list = pickle.load(open('movie_dict.pkl', 'rb'))
# movies_list = movies_list['title'].values --- other way
movies = pd.DataFrame(movies_list)
# also import for similarity
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movies-Recommender-System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    # movies_list  ---- other way
    movies['title'].values
)

# Now apply BUTTON-BOX :
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
     # for i in recommendations:
       # st.write(i)

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


