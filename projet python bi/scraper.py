import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

from datetime import timedelta

# ----------------- Function to Get Team Totals from Boxscore URL -----------------
def get_team_totals(boxscore_url, away_team_abbr, home_team_abbr):
    response = requests.get(boxscore_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        team_totals = {}

        # Scrape Away Team "Team Totals"
        away_team_table = soup.find("table", {"id": f"box-{away_team_abbr}-game-basic"})
        if away_team_table:
            rows = away_team_table.find_all("tr")
            for row in rows:
                if row.find("th") and row.find("th").text.strip() == "Team Totals":
                    cols = row.find_all("td")
                    if len(cols) > 0:
                        team_totals.update({
                            "Away FG": cols[1].text.strip(),
                            "Away FGA": cols[2].text.strip(),
                            "Away FG%": cols[3].text.strip(),
                            "Away 3P": cols[4].text.strip(),
                            "Away 3PA": cols[5].text.strip(),
                            "Away 3P%": cols[6].text.strip(),
                            "Away FT": cols[7].text.strip(),
                            "Away FTA": cols[8].text.strip(),
                            "Away FT%": cols[9].text.strip(),
                            "Away ORB": cols[10].text.strip(),
                            "Away DRB": cols[11].text.strip(),
                            "Away TRB": cols[12].text.strip(),
                            "Away AST": cols[13].text.strip(),
                            "Away STL": cols[14].text.strip(),
                            "Away BLK": cols[15].text.strip(),
                            "Away TOV": cols[16].text.strip(),
                            "Away PF": cols[17].text.strip(),
                            "Away PTS": cols[18].text.strip(),
                        })

        # Scrape Home Team "Team Totals"
        home_team_table = soup.find("table", {"id": f"box-{home_team_abbr}-game-basic"})
        if home_team_table:
            rows = home_team_table.find_all("tr")
            for row in rows:
                if row.find("th") and row.find("th").text.strip() == "Team Totals":
                    cols = row.find_all("td")
                    if len(cols) > 0:
                        team_totals.update({
                            "Home FG": cols[1].text.strip(),
                            "Home FGA": cols[2].text.strip(),
                            "Home FG%": cols[3].text.strip(),
                            "Home 3P": cols[4].text.strip(),
                            "Home 3PA": cols[5].text.strip(),
                            "Home 3P%": cols[6].text.strip(),
                            "Home FT": cols[7].text.strip(),
                            "Home FTA": cols[8].text.strip(),
                            "Home FT%": cols[9].text.strip(),
                            "Home ORB": cols[10].text.strip(),
                            "Home DRB": cols[11].text.strip(),
                            "Home TRB": cols[12].text.strip(),
                            "Home AST": cols[13].text.strip(),
                            "Home STL": cols[14].text.strip(),
                            "Home BLK": cols[15].text.strip(),
                            "Home TOV": cols[16].text.strip(),
                            "Home PF": cols[17].text.strip(),
                            "Home PTS": cols[18].text.strip(),
                        })

        return team_totals
    else:
        print(f"Failed to fetch boxscore data. Status: {response.status_code}")
    return None


def get_daily_scores():
    url = "https://www.basketball-reference.com/"
    boxscores_url = "https://www.basketball-reference.com/boxscores/"
    response = requests.get(url)
    response2 = requests.get(boxscores_url)
    daily_scores = [] 

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        scores_section = soup.find("div", {"id": "scores"})
        soup2 = BeautifulSoup(response2.text, "html.parser")

        if scores_section:
            print("----- Daily Scores -----")
            games = scores_section.find_all("div", class_="game_summary")

            # Extract the game date (handle the new format)
            date_header = soup2.find("h1")
            if date_header:
                raw_date = date_header.text.strip()  # "NBA Games Played on December 16, 2024"
                game_date = raw_date.replace("NBA Games Played on ", "").strip()
                print(f"Game Date: {game_date}")
            else:
                print("Could not find game date. Using today's date as fallback.")
                game_date = datetime.now().strftime("%B %d, %Y")  # Fallback format

            # Format the extracted date to YYYYMMDD
            formatted_date = datetime.strptime(game_date, "%B %d, %Y").strftime("%Y%m%d")

            for game in games:
                # Teams are displayed in two rows: first for Away, second for Home
                teams = game.find_all("tr")

                if len(teams) >= 2:  # Ensure both rows exist
                    away_team_row = teams[0]  # First team is Away
                    home_team_row = teams[1]  # Second team is Home

                    # Extract names and scores
                    away_team_name = away_team_row.find("a").text.strip()
                    away_team_score = away_team_row.find_all("td")[1].text.strip()
                    home_team_name = home_team_row.find("a").text.strip()
                    home_team_score = home_team_row.find_all("td")[1].text.strip()

                    # Extract team abbreviations using the get_team_abbr function
                    away_team_abbr = get_team_abbr(away_team_row)
                    home_team_abbr = get_team_abbr(home_team_row)

                    # Construct the boxscore URL using the home team's abbreviation
                    boxscore_url = f"https://www.basketball-reference.com/boxscores/{formatted_date}0{home_team_abbr}.html"

                    away_team_table_url = f"{boxscore_url}#box-{away_team_abbr}-game-basic"

                    home_team_table_url = f"{boxscore_url}#box-{home_team_abbr}-game-basic"
                    # Scrape the box score stats for "Team Totals"
                    boxscore_stats = get_team_totals(boxscore_url, away_team_abbr, home_team_abbr)

                    if boxscore_stats:
                        daily_scores.append({
                            "Date": game_date,
                            "Away Team": away_team_name,
                            "Away Score": away_team_score,
                            "Home Team": home_team_name,
                            "Home Score": home_team_score,
                            **boxscore_stats
                        })
                        print(f"{away_team_name}: {away_team_score} - {home_team_name}: {home_team_score}")
                    else:
                        print(f"No team totals found for the game between {away_team_name} and {home_team_name}")
        else:
            print("No scores available today.")
    else:
        print(f"Failed to fetch scores. Status: {response.status_code}")
    return daily_scores

def get_team_abbr(team_row):
    team_link = team_row.find("a")
    if team_link:
        href = team_link.get("href", "")
        # Team abbreviations are typically included after /teams/ in the URL
        try:
            # Example href: /teams/LAC/2024.html -> Split and pick the abbreviation
            team_abbr = href.split("/")[2]  # Extract team abbreviation
            print(f"Extracted team abbreviation: {team_abbr}")
            return team_abbr.upper()
        except IndexError:
            print("Error extracting team abbreviation.")
            return ""
    return ""



# ----------------- Function to Get League Standings -----------------
def get_league_standings():
    url = "https://www.basketball-reference.com/leagues/NBA_2025_standings.html"
    response = requests.get(url)
    standings = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        print("\n----- League Standings -----")

        for conference_id, conference_name in [
            ("confs_standings_E", "Eastern Conference"),
            ("confs_standings_W", "Western Conference")
        ]:
            print(f"\n{conference_name}:")
            table = soup.find("table", {"id": conference_id})
            if table:
                rows = table.find("tbody").find_all("tr")
                for row in rows:
                    if "class" in row.attrs and "thead" in row.attrs["class"]:
                        continue  # Skip headers
                    team = row.find("a")
                    if team:
                        team_name = team.text.strip()
                        cells = row.find_all("td")
                        wins = cells[0].text.strip()
                        losses = cells[1].text.strip()
                        print(f"{team_name}: {wins} Wins, {losses} Losses")
                        standings.append({
                            "Conference": conference_name,
                            "Team": team_name,
                            "Wins": wins,
                            "Losses": losses
                        })
    else:
        print(f"Failed to fetch standings. Status: {response.status_code}")
    return standings

# ----------------- Function to Get Player Stats -----------------
def get_player_stats():
    url = "https://www.basketball-reference.com/leagues/NBA_2025_per_game.html"
    response = requests.get(url)
    player_stats = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        print("\n----- Player Stats -----")
        
        # Find the player stats table
        table = soup.find("table")
        
        # Read the table into a DataFrame
        df = pd.read_html(str(table), header=0)[0]
        
        # Clean up any extra header rows (repeated every 25 rows)
        #df_cleaned = df[~df['Rk'].str.contains('Rk', na=False)]
        
        # Loop through the cleaned DataFrame and create a list of dictionaries
        for index, row in df.iterrows():
            player_stats.append({
                "Rk": row['Rk'],
                "Player": row['Player'],
                "Team": row['Team'],
                "G": row['G'],
                "MP": row['MP'],
                "FG": row['FG'],
                "FGA": row['FGA'],
                "FG%": row['FG%'],
                "3P": row['3P'],
                "3PA": row['3PA'],
                "3P%": row['3P%'],
                "2P": row['2P'],
                "2PA": row['2PA'],
                "2P%": row['2P%'],
                "FT": row['FT'],
                "FTA": row['FTA'],
                "FT%": row['FT%'],
                "ORB": row['ORB'],
                "DRB": row['DRB'],
                "TRB": row['TRB'],
                "AST": row['AST'],
                "STL": row['STL'],
                "BLK": row['BLK'],
                "TOV": row['TOV'],
                "PF": row['PF'],
                "PTS": row['PTS']
            })
    else:
        print(f"Failed to fetch player stats. Status: {response.status_code}")
    
    return player_stats

# ----------------- Main Script -----------------
def main():
    # Get Daily Scores
    daily_scores = get_daily_scores()

    # Get League Standings
    standings = get_league_standings()

    player_stats = get_player_stats()

    # Save Data to CSV Files
    pd.DataFrame(daily_scores).to_csv("daily_scores.csv", index=False)
    pd.DataFrame(standings).to_csv("league_standings.csv", index=False)
    pd.DataFrame(player_stats).to_csv("player_stats.csv", index=False)

    print("\nData saved to 'daily_scores.csv' , 'league_standings.csv' and 'player_stats.csv'.")

if __name__ == "__main__":
    main()