import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="🎬 Movie Dashboard Analysis", layout='wide')
st.header("Interactive Dashboard")
st.subheader("Interact with this dashboard using the widgets on the sidebar")

# Read data
movies_data = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")
movies_data.dropna(inplace=True)

# Sidebar filters
year_list = movies_data['year'].unique().tolist()
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()

with st.sidebar:
    st.write("Select a score range")
    new_score_rating = st.slider(
        label="Score range:",
        min_value=1.0,
        max_value=10.0,
        value=(3.0, 4.0)
    )

    st.write("Select preferred genres and year")
    new_genre_list = st.multiselect(
        'Choose Genre:',
        genre_list,
        default=genre_list
    )

    year = st.selectbox('Choose a Year', year_list, 0)

# Combined filter for all widgets
combined_filter = (
    movies_data['score'].between(*new_score_rating) &
    movies_data['genre'].isin(new_genre_list) &
    (movies_data['year'] == year)
)

filtered_data = movies_data[combined_filter]

# VISUALIZATION SECTION
col1, col2 = st.columns([2, 3])

with col1:
    st.write("#### Movies filtered by Year, Genre, and Score")
    dataframe_genre_year = filtered_data[['name', 'genre', 'year']]
    st.dataframe(dataframe_genre_year, width=400)

with col2:
    st.write("#### Number of Movies per Genre")
    rating_count_year = filtered_data.groupby('genre')['score'].count().reset_index()
    figpx = px.line(rating_count_year, x='genre', y='score')
    st.plotly_chart(figpx)

st.write("Average Movie Budget (in Millions), Grouped by Genre")

avg_budget = filtered_data.groupby('genre')['budget'].mean().round() / 1_000_000
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']

fig = plt.figure(figsize=(19, 10))
plt.bar(genre, avg_bud, color='maroon')
plt.xlabel('Genre')
plt.ylabel('Average Budget (Millions)')
plt.title('Average Budget of Movies by Genre (in Millions)')
st.pyplot(fig)
