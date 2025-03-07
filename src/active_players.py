import requests
from bs4 import BeautifulSoup
import unicodedata

def normalize_name(name):
    """Normalize player names by removing special characters."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )

def get_active_players(season):
    """Scrapes the active NBA player list for a given season from Basketball Reference."""
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_per_game.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for {season}")
        return []
    print(f"Request status code for {season}: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "per_game_stats"})
    
    if not table:
        print(f"No table found for {season}")
        return []

    players = set()  # Use a set to avoid duplicates
    for row in table.find_all("tr"):
        player_cell = row.find("td", {"data-stat": "name_display"})
        if player_cell:
            player_name = normalize_name(player_cell.text.strip())
            players.add(player_name)

    return list(players)

# Example usage
if __name__ == "__main__":
    seasons = range(2009, 2026)  # From 2009 to 2025
    all_players = {}
    for season in seasons:
        players = get_active_players(season)
        all_players[season] = players
        print(f"Season {season}: {len(players)} players")
