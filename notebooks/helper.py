import pandas as pd
import numpy as np

def total_wins_country(results):
    won_on_home_away = results["result"].value_counts()
    won_on_penelty = results["penalty_winner"].value_counts()

    total_wins = won_on_home_away.add(won_on_penelty, fill_value=0).sort_values(ascending=False)

    total_wins = pd.DataFrame(total_wins).reset_index().rename(columns={"index": "Country" , "count" : "Matches Won"})
    tie_rows = total_wins[total_wins['Country'] == "tie"]
    total_wins = total_wins.drop(tie_rows.index)

    return total_wins

def year_tournament_list(results):
    years = results["year"].unique().tolist()
    years.insert(0, "Overall")

    tournament = np.unique(results["tournament"])
    tournament = tournament.tolist()
    tournament.insert(0, "Overall")

    return years , tournament


def fetch_match_won(results ,year, tournament):
    if year == "Overall" and tournament == "Overall":
        temp_df = results
    if year != "Overall" and tournament == "Overall":
        temp_df = results[results["year"] == year]
    if year == "Overall" and tournament != "Overall":
        temp_df = results[results["tournament"] == tournament]
    if year != "Overall" and tournament != "Overall":
        temp_df = results[(results["year"] == year) & (results["tournament"] == tournament)]

    won_on_home_away = temp_df["result"].value_counts()
    won_on_penelty = temp_df["penalty_winner"].value_counts()

    total_wins = won_on_home_away.add(won_on_penelty, fill_value=0).sort_values(ascending=False)
    total_wins = pd.DataFrame(total_wins).reset_index()
    total_wins = total_wins.rename(columns={"index": "Country", "count": "Matches Won", "result": "Country"})
    total_wins = total_wins[total_wins["Country"] != "tie"]

    total_wins["Matches Won"] = total_wins["Matches Won"].astype(int)
    return total_wins

def nations(goalscorer) :
    nations = goalscorer["team"].unique().tolist()
    nations.sort()
    nations.insert(0, "Overall")
    return nations


def team_sort(goalscorer, country):
    if country == "Overall":
        team = goalscorer
    else:
        team = goalscorer[goalscorer["team"] == country]

    player_goal_scored = pd.DataFrame(team.groupby(['scorer'])[['scorer']].agg('count')).rename(
        columns={'scorer': 'goal_scored'}).sort_values('goal_scored', ascending=False).reset_index()

    return player_goal_scored

def tour_cups(results):
    top_tours = results[
        (results.tournament == 'FIFA World Cup') |
        (results.tournament == 'FIFA World Cup qualification') |
        (results.tournament == 'Copa América') |
        (results.tournament == 'UEFA Euro') |
        (results.tournament == 'African Cup of Nations') |
        (results.tournament == 'Confederations Cup') |
        (results.tournament == "King's Cup") |
        (results.tournament == 'AFC Asian Cup')
        ]
    return top_tours