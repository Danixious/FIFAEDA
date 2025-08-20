import pandas as pd

goalscorer = pd.read_csv("data/goalscorers.csv")
df = pd.read_csv("data/results.csv")
shootout = pd.read_csv("data/shootouts.csv")

def preprocess():
    global df , goalscorer ,shootout

    def find_result(result):
        if result.home_score > result.away_score:
            return result.home_team
        if result.away_score > result.home_score:
            return result.away_team
        else:
            return 'tie'

    df['result'] = df.apply(find_result, axis=1)

    results = df.merge(shootout, how='left', left_on=['date', 'home_team', 'away_team'],
                       right_on=['date', 'home_team', 'away_team'])
    results = results.rename(columns={'winner': 'penalty_winner'})

    # Formatting the date column into year , month , day
    results['date'] = pd.to_datetime(results['date'], errors='coerce', format='%Y-%m-%d')

    results['year'] = results['date'].dt.year
    results['month'] = results['date'].dt.month
    results['day'] = results['date'].dt.day

    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    results['weekday'] = results['date'].map(lambda x: day_order[x.weekday()])

    return results

def scorer_data():
    global goalscorer
    return goalscorer