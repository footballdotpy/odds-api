import requests
import json
import pandas as pd

api_key = "#############"  # replace with own API
market = 'h2h'
region = 'eu,uk'
sport_key = "soccer_epl"

# Build the URL for the API request
url = f'https://api.the-odds-api.com/v4/sports/{sport_key}/odds/'


# Add the parameters for the API request
params = {
    'apiKey': api_key,
    'regions': region,
    'markets': market,
    'oddsFormat':'decimal',
    'bookmakers':['pinnacle']
}

# Make the API request using the built URL and parameters
odds_response = requests.get(url, params=params)

print(odds_response)

# Parse the JSON response text into Python data structures (a list of dictionaries)
odds_data = json.loads(odds_response.text)


data_lists = []

# Check if every item in odds_data is a dictionary
if all(isinstance(item, dict) for item in odds_data) :

    # If they are, then loop through each game in odds_data
    for game in odds_data:

        # Loop through each bookmaker in the current game
        for bookmaker in game['bookmakers']:

            # Loop through each market in the current bookmaker
            for market_ in bookmaker['markets']:

                # Loop through each outcome in the current market
                for outcome in market_['outcomes']:

                    # Create a dictionary for the current outcome with relevant details
                    row = {
                        'game_id': game['id'],
                        'sport_key': game['sport_key'],
                        'sport_title': game['sport_title'],
                        'home_team': game['home_team'],
                        'away_team': game['away_team'],
                        'commence_time': game['commence_time'],
                        'bookmaker_key': bookmaker['key'],
                        'bookmaker_title': bookmaker['title'],
                        'bookmaker_last_update': bookmaker['last_update'],
                        'market_key': market_['key'],
                        'market_last_update': market_['last_update'],
                        'outcome_name': outcome['name'],
                        'outcome_price': outcome['price']
                    }

                    # Append the current row dictionary to the rows_list
                    data_lists.append(row)


# Create a pandas DataFrame from the rows_list
df = pd.DataFrame(data_lists)

# Use the numpy reshape function to create separate columns for each outcome
reshaped_odds = df['outcome_price'].values.reshape(-1, 3)

# Drop the original Odds and Outcome_Name columns
df = df.drop(columns=['outcome_name', 'outcome_price'],axis=1)


# Drop duplicate rows (optional)
df = df.drop_duplicates()


# Create separate columns for home odds, away odds, and draw odds
df['homeOdds'] = reshaped_odds[:, 0]
df['awayOdds'] = reshaped_odds[:, 1]
df['drawOdds'] = reshaped_odds[:, 2]


df = df[['sport_key','commence_time','bookmaker_title','home_team','away_team','bookmaker_last_update','market_key','homeOdds','drawOdds','awayOdds']]