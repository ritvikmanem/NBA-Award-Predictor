from bs4 import BeautifulSoup
import requests

'''
MVP Stats:
Per Game Stats: PPG, APG, RPG, BPG, EffFG%(Probably better than TS% for this purpose), FT%, SPG
Advanced Game Stats: USG%, AST%, TRB%, PER, WS, WS/48, BPM, OBPM, DBPM, VORP, STL%, BLK%, TOV%
'''

# URL of the player's page on Basketball Reference
url = "https://www.basketball-reference.com/players/j/jamesle01.html"
req = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(req.content, "html.parser")

# Define the stats you want to scrape
data_stats = {
    "per_game_stats": [
        "pts_per_g", "ast_per_g", "trb_per_g", "blk_per_g", "efg_pct", "ft_pct", "stl_per_g"
    ],
    "advanced": [
        "usg_pct", "ast_pct", "trb_pct", "per", "ws", "ws_per_48", "bpm", "obpm", "dbpm", "vorp", "stl_pct", "blk_pct", "tov_pct"
    ]
}

# Function to scrape a table
def scrape_table(table_id, season):
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
    per_game_stats = scrape_table("per_game_stats", season)
    advanced_stats = scrape_table("advanced", season)
    
    combined_stats = {}
    if per_game_stats:
        combined_stats.update(per_game_stats)
    if advanced_stats:
        combined_stats.update(advanced_stats)
    
    return combined_stats

# Example usage
season = "2025"
combined_stats = scrape_combined_stats("LeBron James", season)
if combined_stats:
    for stat, value in combined_stats.items():
        print(f"{stat}: {value}")
else:
    print(f"No stats found for season {season}")

