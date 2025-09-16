import streamlit as st
import pandas as pd
import plotly.express as px

# Main page configuration
st.set_page_config(page_title="🎬 Movie Dashboard Analysis", layout='wide')

@st.cache_data
def load_data():
    """
    Loads the movie data from a CSV file via URL and caches it.
    Rows with any missing values are dropped.
    """
    data = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")
    data.dropna(inplace=True)
    return data

def setup_sidebar(data):
    """
    Sets up the sidebar widgets for filtering and returns the selected values.
    """
    st.sidebar.header("Filter Options")

    score_range = st.sidebar.slider(
        label="Select a score range:",
        min_value=1.0,
        max_value=10.0,
        value=(3.0, 4.0)
    )

    genre_list = sorted(data['genre'].unique().tolist())
    selected_genres = st.sidebar.multiselect(
        'Choose preferred genres:',
        genre_list,
        default=genre_list
    )

    min_year = int(data['year'].min())
    max_year = int(data['year'].max())
    selected_year_range = st.sidebar.slider(
        'Choose a Year Range:',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    return score_range, selected_genres, selected_year_range

def get_filtered_data(data, score_range, genres, year_range):
    """
    Filters the dataframe based on the selected criteria from the sidebar.
    """
    return data[
        data['score'].between(*score_range) &
        data['genre'].isin(genres) &
        data['year'].between(year_range[0], year_range[1])
    ]

def display_visualizations(data):
    """
    Displays the data visualizations in a tabbed interface.
    """
    st.header("📊 Data Visualizations")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Filtered Data View", "📈 Movies per Genre", "💰 Average Budget by Genre", "💸 Score vs. Budget"])

    with tab1:
        st.write("#### Detailed Movie Data")
        cols_to_display = ['name', 'genre', 'year', 'score', 'budget']
        st.dataframe(data[cols_to_display], use_container_width=True)

    with tab2:
        st.write("#### Number of Movies per Genre")
        movies_per_genre = data.groupby('genre')['name'].count().reset_index().rename(columns={'name': 'count'})
        fig_bar_genre = px.bar(movies_per_genre, x='genre', y='count', title='Number of Movies per Genre')
        st.plotly_chart(fig_bar_genre, use_container_width=True)

    with tab3:
        st.write("#### Average Movie Budget by Genre")
        avg_budget = data.groupby('genre')['budget'].mean().reset_index()
        avg_budget['budget_in_millions'] = (avg_budget['budget'] / 1_000_000).round(2)
        fig_bar_budget = px.bar(
            avg_budget,
            x='genre',
            y='budget_in_millions',
            title='Average Movie Budget by Genre (in Millions)',
            labels={'budget_in_millions': 'Average Budget (Millions)'}
        )
        st.plotly_chart(fig_bar_budget, use_container_width=True)

    with tab4:
        st.write("#### Score vs. Budget Analysis")
        fig_scatter = px.scatter(
            data,
            x='budget',
            y='score',
            hover_name='name',
            size='score',
            color='genre',
            title='Movie Score vs. Budget'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

def main():
    """
    Main function to run the Streamlit application.
    """
    st.title("🎬 Movie Dashboard Analysis")
    st.subheader("Interact with this dashboard using the widgets on the sidebar")

    movies_data = load_data()
    score_range, selected_genres, year_range = setup_sidebar(movies_data)
    filtered_data = get_filtered_data(movies_data, score_range, selected_genres, year_range)

    st.markdown("---")
    display_visualizations(filtered_data)

if __name__ == '__main__':
    main()
