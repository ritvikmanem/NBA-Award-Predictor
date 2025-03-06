from bs4 import BeautifulSoup
import requests
from nba_api.stats.static import players as NBAAPIPlayers
import time

'''
MVP Stats:
Per Game Stats: PPG, APG, RPG, BPG, EffFG%(Probably better than TS% for this purpose), FT%, SPG
Advanced Game Stats: USG%, AST%, TRB%, PER, WS, WS/48, BPM, OBPM, DBPM, VORP, STL%, BLK%, TOV%
'''

# Define the stats you want to scrape
data_stats = {
    "per_game_stats": [
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
    
    # Handle suffixes like "Jr.", "Sr.", "III", etc.
    if last.lower() in ["jr", "sr", "ii", "iii", "iv", "v"]:
        last = parts[-2]
    
    base_url = f"https://www.basketball-reference.com/players/{last[0].lower()}/{last[:5].lower()}{first[:2].lower()}"
    
    # Try different suffixes (01, 02, 03, ...)
    for i in range(1, 10):
        url = f"{base_url}{i:02d}.html"
        req = requests.get(url)
        if req.status_code == 200:
            print(f"Generated URL for {player_name}: {url}")  # Debugging line
            return url
    
    print(f"Could not generate a valid URL for {player_name}")
    return None

# Function to scrape a table
def scrape_table(soup, table_id, season):
    table = soup.find("table", {"id": table_id})
    if table:
        row = table.find("tr", {"id": f"{table_id}.{season}"})
        if row:
            stats = {}
            # Scrape season
            season_cell = row.find("th", {"data-stat": "year_id"})
            if season_cell:
                stats["season"] = season_cell.text
                print(f"Scraped season: {season_cell.text}")  # Debugging line

            for data_stat in data_stats[table_id]:
                cell = row.find("td", {"data-stat": data_stat})
                if cell:
                    stats[data_stat] = cell.text
                    print(f"Scraped {data_stat}: {cell.text}")  # Debugging line
                else:
                    stats[data_stat] = None
                    print(f"Missing {data_stat}")  # Debugging line
            return stats
    print(f"Table {table_id} not found for season {season}")  # Debugging line
    return None

# Function to scrape per game stats
def scrape_per_game_stats(player_name, season):
    url = get_br_url(player_name)
    while True:
        req = requests.get(url)
        print(f"PER_GAME: Request status code for {player_name}: {req.status_code}")  # Print status code
        if req.status_code == 200:
            break
        elif req.status_code == 429:
            print(f"Rate limited. Sleeping for 5 seconds before retrying...")
            time.sleep(5)
        else:
            print(f"Could not find URL for {player_name}, status code: {req.status_code}")
            return None
    soup = BeautifulSoup(req.content, "html.parser")

    per_game_stats = scrape_table(soup, "per_game_stats", season)
    
    return per_game_stats

# Function to scrape advanced stats
def scrape_advanced_stats(player_name, season):
    url = get_br_url(player_name)
    while True:
        req = requests.get(url)
        print(f"ADVANCED: Request status code for {player_name}: {req.status_code}")  # Print status code
        if req.status_code == 200:
            break
        elif req.status_code == 429:
            print(f"Rate limited. Sleeping for 5 seconds before retrying...")
            time.sleep(5)
        else:
            print(f"Could not find URL for {player_name}, status code: {req.status_code}")
            return None
    soup = BeautifulSoup(req.content, "html.parser")

    advanced_stats = scrape_table(soup, "advanced", season)
    
    return advanced_stats

# Function to scrape combined stats (per game and advanced)
def scrape_combined_stats(player_name, season):
    per_game_stats = scrape_per_game_stats(player_name, season)
    time.sleep(5)  # Add a 5-second delay between requests to avoid rate limits
    advanced_stats = scrape_advanced_stats(player_name, season)
    
    if per_game_stats or advanced_stats:
        combined_stats = {**per_game_stats, **advanced_stats}
        return combined_stats
    return None

# Function to scrape stats for all active players
def scrape_all_players_stats(season):
    all_players = NBAAPIPlayers.get_active_players()
    all_stats = {}
    for player in all_players:
        player_name = player['full_name']
        print(f"Scraping stats for {player_name}")
        
        combined_stats = scrape_combined_stats(player_name, season)
        
        if combined_stats:
            all_stats[player_name] = combined_stats
        else:
            print(f"No stats found for {player_name} in season {season}")
        time.sleep(5)  # Add a 5-second delay between requests to avoid rate limits
    return all_stats

# Example usage
if __name__ == "__main__":
    current_season = "2025"  # Update this to the current season format used by Basketball Reference
    all_players_stats = scrape_all_players_stats(current_season)
    
    # Print stats for the first 5 players in a formatted way
    for i, (player_name, stats) in enumerate(all_players_stats.items()):
        if i >= 5:
            break
        print(f"\nCombined Stats for {player_name}:")
        for stat, value in stats.items():
            print(f"  {stat}: {value}")

