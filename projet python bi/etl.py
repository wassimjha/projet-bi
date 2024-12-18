import pandas as pd

def clean_daily_scores(input_file, output_file):
    """Clean and transform daily scores data."""
    df = pd.read_csv(input_file)
    df['Away Score'] = pd.to_numeric(df['Away Score'], errors='coerce')
    df['Home Score'] = pd.to_numeric(df['Home Score'], errors='coerce')
    df.dropna(inplace=True)
    df.to_csv(output_file, index=False)
    print("Daily scores cleaned and saved.")

def clean_league_standings(input_file, output_file):
    """Clean and transform league standings data."""
    df = pd.read_csv(input_file)
    df['Wins'] = pd.to_numeric(df['Wins'], errors='coerce')
    df['Losses'] = pd.to_numeric(df['Losses'], errors='coerce')
    df.to_csv(output_file, index=False)
    print("League standings cleaned and saved.")

def clean_player_stats(input_file, output_file):
    """Clean and transform player stats data."""
    # Read the input CSV file
    df = pd.read_csv(input_file)
    
    # Convert columns to numeric values (where appropriate), handling errors as NaN
    df['G'] = pd.to_numeric(df['G'], errors='coerce')
    df['MP'] = pd.to_numeric(df['MP'], errors='coerce')
    df['FG'] = pd.to_numeric(df['FG'], errors='coerce')
    df['FGA'] = pd.to_numeric(df['FGA'], errors='coerce')
    df['FG%'] = pd.to_numeric(df['FG%'], errors='coerce')
    df['3P'] = pd.to_numeric(df['3P'], errors='coerce')
    df['3PA'] = pd.to_numeric(df['3PA'], errors='coerce')
    df['3P%'] = pd.to_numeric(df['3P%'], errors='coerce')
    df['2P'] = pd.to_numeric(df['2P'], errors='coerce')
    df['2PA'] = pd.to_numeric(df['2PA'], errors='coerce')
    df['2P%'] = pd.to_numeric(df['2P%'], errors='coerce')
    df['FT'] = pd.to_numeric(df['FT'], errors='coerce')
    df['FTA'] = pd.to_numeric(df['FTA'], errors='coerce')
    df['FT%'] = pd.to_numeric(df['FT%'], errors='coerce')
    df['ORB'] = pd.to_numeric(df['ORB'], errors='coerce')
    df['DRB'] = pd.to_numeric(df['DRB'], errors='coerce')
    df['TRB'] = pd.to_numeric(df['TRB'], errors='coerce')
    df['AST'] = pd.to_numeric(df['AST'], errors='coerce')
    df['STL'] = pd.to_numeric(df['STL'], errors='coerce')
    df['BLK'] = pd.to_numeric(df['BLK'], errors='coerce')
    df['TOV'] = pd.to_numeric(df['TOV'], errors='coerce')
    df['PF'] = pd.to_numeric(df['PF'], errors='coerce')
    df['PTS'] = pd.to_numeric(df['PTS'], errors='coerce')
    
    # Drop rows with any missing or invalid data (NaN values)
    df.dropna(inplace=True)
    
    # Rename the columns to match the desired naming convention
    df.rename(columns={
        'Tm': 'Team',
        'Rk': 'Rank',
        'Player': 'Player Name',
    }, inplace=True)
    
    # Save the cleaned dataframe to a new CSV file
    df.to_csv(output_file, index=False)
    print("Player stats cleaned and saved to", output_file)

def main():
    clean_daily_scores('daily_scores.csv', 'daily_scores_clean.csv')
    clean_league_standings('league_standings.csv', 'league_standings_clean.csv')
    clean_player_stats('player_stats.csv', 'player_stats_clean.csv')

if __name__ == "__main__":
    main()
