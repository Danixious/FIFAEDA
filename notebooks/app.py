import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessing,helper

results = preprocessing.preprocess()
goalscorer = preprocessing.scorer_data()

st.sidebar.title("Internatinal Football Analysis")

st.sidebar.image(
    "https://i.pinimg.com/564x/b9/8a/ec/b98aecd652d202842fb3e5e48d4eecd1.jpg"
)

user_menu = st.sidebar.radio(
    'Select an option',
    ('Top Winning Team' , 'FIFA World Cup Analysis' , 'Top Scoring players' , 'EDA')
)

if user_menu == 'Top Winning Team':
    st.sidebar.header("TOP WINNERS")
    years,tournament = helper.year_tournament_list(results)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_tournament = st.sidebar.selectbox("Select Tournament", tournament)

    total_wins = helper.fetch_match_won(results ,selected_year , selected_tournament)

    if selected_year == "Overall" and selected_tournament == "Overall":
        st.title("Top Teams in International Football Overall")
    if selected_year != "Overall" and selected_tournament == "Overall":
        st.title("Top Teams in Year " + str(selected_year))
    if selected_year == "Overall" and selected_tournament != "Overall":
        st.title(selected_tournament + "'s Top Winning Team")
    if selected_year != "Overall" and selected_tournament != "Overall":
        st.title(selected_tournament + "'s Top Team in Year " + str(selected_year))

    st.table(total_wins)

if user_menu == 'FIFA World Cup Analysis':
    tournament_played = results["tournament"].unique().shape[0]-1
    fifa = results[results["tournament"] == "FIFA World Cup"]
    years_hosted = fifa["year"].unique().shape[0]
    countries_hosted = fifa["country"].unique().shape[0]
    most_appeared = fifa["home_team"].value_counts().index[0]
    most_goal = fifa["home_score"].max()
    max_penalty = fifa["penalty_winner"].value_counts().index[0]

    st.title("Top Statistics")
    col1,col3 = st.columns(2)
    with col3:
        st.header("Tournament other than FIFA")
        st.title(tournament_played)
    with col1:
        st.header("Year's FIFA Hosted")
        st.title(years_hosted)

    col2, col4= st.columns(2)
    with col2:
        st.header("FIFA Hosting Countries")
        st.title(countries_hosted)
    with col4:
        st.header("Most appeared team")
        st.title(most_appeared)

    col5, col6 = st.columns(2)

    with col5:
        st.header("Most goal scored")
        st.title(most_goal)
    with col6:
        st.header("Most Wins in Penalty")
        st.title(max_penalty)

    x = fifa.groupby("year").count()["date"]
    fig = px.line(x)
    st.header("Matches played in FIFA")
    st.plotly_chart(fig)

    month_name = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov',
        12: 'Dec'
    }
    fifa["months"] = fifa["month"].map(month_name)
    fig = px.histogram(fifa,
                       x="months",
                       text_auto=True,
                       title='Number of matches played per month in FIFA',
                       )
    fig.update_layout(bargap=0.2)
    fig.update_xaxes(type='category', title_text='Months')
    fig.update_yaxes(title_text='Matches played')
    st.plotly_chart(fig)

if user_menu == "Top Scoring players" :
    st.header("TOP SCORER")
    country = helper.nations(goalscorer)
    selected_country = st.selectbox("Select Country", country)

    scorer = helper.team_sort(goalscorer , selected_country)
    st.table(scorer)

if user_menu == "EDA" :
    st.header("Exploratory Data Analysis")
    month_name = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov',
        12: 'Dec'
    }
    results["months"] = results["month"].map(month_name)
    results = results.sort_values("month")
    fig = px.histogram(results,
                       x="months",
                       text_auto=True,
                       title='Number of matches played per month',
                       )
    fig.update_layout(bargap=0.2)
    fig.update_xaxes(type='category', title_text='Number of months')
    fig.update_yaxes(title_text='Matches played')
    st.plotly_chart(fig)
    st.text("On June , august, september most matches are played")

    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fig = px.histogram(results,
                       x="weekday",
                       text_auto=True,
                       title='Number of matches played per weekday',
                       category_orders={"weekday" : day_order})
    fig.update_layout(bargap=0.2)
    fig.update_xaxes(type='category', title_text='Number of months')
    fig.update_yaxes(title_text='matches played')
    st.plotly_chart(fig)

    top_tour = helper.tour_cups(results)
    tournaments_count_over_years = pd.DataFrame(top_tour.groupby(['year', 'tournament'])['tournament'].count()).rename(columns={'tournament': 'matches_played'})
    tournaments_count_over_years = tournaments_count_over_years.reset_index().sort_values('year', ascending=False)

    fig = px.line(tournaments_count_over_years,
                  x="year", y=["matches_played"],
                  color='tournament',
                  labels={'matches_played': 'number of matches'})

    fig.update_layout(title='Number of matches played in each tournament over the years',
                      yaxis_title='Matches played')
    st.plotly_chart(fig)

    not_participated_matches = results[(results.neutral == True)]['country'].value_counts().reset_index().rename(
        columns={'count': 'matches_hosted'})

    fig = px.bar(not_participated_matches[:25],
                 x='country',
                 y='matches_hosted',
                 color='country',
                 title='Top 50 countries that hosted matches in which it not participated',
                 text_auto=True,
                 )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig)

    goalscorer['half'] = goalscorer['minute'].apply(lambda x: 'first_half' if (x < 45.0) else 'second_half')
    team_goal_in_halfs = goalscorer.groupby(['team', 'half'])[['scorer']].agg('count').sort_values('scorer',ascending=False).reset_index().rename(
        columns={'scorer': 'goals_scored'})

    fig = px.bar(team_goal_in_halfs[:25],
                 x='team',
                 y='goals_scored',
                 color="half",
                 title="Most goals scored in first and second halfs by teams(starting from highest)",
                 text_auto=True)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig)

    player_goal_scored_in_halfs = pd.DataFrame(goalscorer.groupby(['scorer', 'half'])[['scorer']].agg('count')).rename(
        columns={'scorer': 'goal_scored'}).sort_values('goal_scored', ascending=False).reset_index()

    fig = px.bar(player_goal_scored_in_halfs[:25],
                 x='scorer',
                 y='goal_scored',
                 color="half",
                 title="Most goals scored in first and second halfs by individual players(starting from highest)",
                 text_auto=True)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig)