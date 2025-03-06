from bs4 import BeautifulSoup
import requests
from nba_api.stats.static import players
import time

'''
MVP Stats:
Per Game Stats: PPG, APG, RPG, BPG, EffFG%(Probably better than TS% for this purpose), FT%, SPG
Advanced Game Stats: USG%, AST%, TRB%, PER, WS, WS/48, BPM, OBPM, DBPM, VORP, STL%, BLK%, TOV%
'''

# Define the stats you want to scrape
data_stats = {
    "per_game": [
        "pts_per_g", "ast_per_g", "trb_per_g", "blk_per_g", "efg_pct", "ft_pct", "stl_per_g"
    ],
    "advanced": [
        "usg_pct", "ast_pct", "trb_pct", "per", "ws", "ws_per_48", "bpm", "obpm", "dbpm", "vorp", "stl_pct", "blk_pct", "tov_pct"
    ]
}

# Function to get the Basketball Reference URL for a player
def get_br_url(player_name):
    parts = player_name.split()
    first, last = parts[0], parts[-1]
    url = f"https://www.basketball-reference.com/players/{last[0].lower()}/{last[:5].lower()}{first[:2].lower()}01.html"
    print(f"Generated URL for {player_name}: {url}")  # Debugging line
    return url

# Function to scrape a table
def scrape_table(soup, table_id, season):
    table = soup.find("table", {"id": table_id})
    if table:
        row = table.find("tr", {"id": f"{table_id}.{season}"})
        if row:
            stats = {}
            for data_stat in data_stats[table_id]:
                cell = row.find("td", {"data-stat": data_stat})
                if cell:
                    stats[data_stat] = cell.text
                else:
                    stats[data_stat] = None
            return stats
    return None

# Function to scrape combined stats
def scrape_combined_stats(player_name, season):
    url = get_br_url(player_name)
    while True:
        req = requests.get(url)
        print(f"Request status code for {player_name}: {req.status_code}")  # Print status code
        if req.status_code == 200:
            break
        elif req.status_code == 429:
            print(f"Rate limited. Sleeping for 15 seconds before retrying...")
            time.sleep(15)
        else:
            print(f"Could not find URL for {player_name}, status code: {req.status_code}")
            return None
    soup = BeautifulSoup(req.content, "html.parser")

    per_game_stats = scrape_table(soup, "per_game", season)
    advanced_stats = scrape_table(soup, "advanced", season)
    
    combined_stats = {}
    if per_game_stats:
        combined_stats.update(per_game_stats)
    if advanced_stats:
        combined_stats.update(advanced_stats)
    
    return combined_stats

# Function to scrape stats for the first active player
def scrape_first_player_stats(season):
    all_players = players.get_active_players()
    if all_players:
        player = all_players[0]
        player_name = player['full_name']
        print(f"Scraping stats for {player_name}")
        combined_stats = scrape_combined_stats(player_name, season)
        if combined_stats:
            print(f"\nStats for {player_name}:")
            for stat, value in combined_stats.items():
                print(f"  {stat}: {value}")
        else:
            print(f"No stats found for {player_name} in season {season}")
    else:
        print("No active players found.")

# Example usage
if __name__ == "__main__":
    current_season = "2025"  # Update this to the current season format used by Basketball Reference
    scrape_first_player_stats(current_season)

