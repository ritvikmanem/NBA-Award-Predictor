import os
import sqlite3
from scraper import scrape_combined_stats  # Import the scraper function
from nba_api.stats.static import players
import time
from active_players import get_active_players  # Import the function to get active players

# Define a fixed database path
DB_PATH = "/home/manemritvik/projects/repos/NBA-Award-Predictor/data/mvp_stats.db"

def create_db():
    """Ensure the data directory exists and create the SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Ensure 'data/' directory exists

    conn = sqlite3.connect(DB_PATH)  # Use the correct path
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mvp_stats (
        season TEXT,
        player_id INTEGER,
        player_name TEXT,
        pts_per_g REAL,
        ast_per_g REAL,
        trb_per_g REAL,
        blk_per_g REAL,
        efg_pct REAL,
        ft_pct REAL,
        stl_per_g REAL,
        usg_pct REAL,
        ast_pct REAL,
        trb_pct REAL,
        per REAL,
        ws REAL,
        ws_per_48 REAL,
        bpm REAL,
        obpm REAL,
        dbpm REAL,
        vorp REAL,
        stl_pct REAL,
        blk_pct REAL,
        tov_pct REAL,
        PRIMARY KEY (season, player_id)
    )
    """)
    
    conn.commit()
    conn.close()

def get_player_stats(player_id, season):
    """Retrieve stats for a specific player and season."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM mvp_stats
    WHERE player_id = ? AND season = ?
    """, (player_id, season))

    stats = cursor.fetchone()
    conn.close()
    return stats

def insert_player_stats(player_id, player_name, season):
    """Fetch and insert player stats from Basketball Reference into the database."""
    combined_stats = scrape_combined_stats(player_name, season)
    
    if not combined_stats:
        print(f"Could not fetch all stats for {player_name} in the {season} season.")
        return

    print(f"Combined stats for {player_name} in the {season} season: {combined_stats}")  # Debugging line

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO mvp_stats (season, player_id, player_name, pts_per_g, ast_per_g, trb_per_g, blk_per_g, efg_pct, ft_pct, stl_per_g, usg_pct, ast_pct, trb_pct, per, ws, ws_per_48, bpm, obpm, dbpm, vorp, stl_pct, blk_pct, tov_pct)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        season,
        player_id,
        player_name,
        combined_stats.get('pts_per_g'),
        combined_stats.get('ast_per_g'),
        combined_stats.get('trb_per_g'),
        combined_stats.get('blk_per_g'),
        combined_stats.get('efg_pct'),
        combined_stats.get('ft_pct'),
        combined_stats.get('stl_per_g'),
        combined_stats.get('usg_pct'),
        combined_stats.get('ast_pct'),
        combined_stats.get('trb_pct'),
        combined_stats.get('per'),
        combined_stats.get('ws'),
        combined_stats.get('ws_per_48'),
        combined_stats.get('bpm'),
        combined_stats.get('obpm'),
        combined_stats.get('dbpm'),
        combined_stats.get('vorp'),
        combined_stats.get('stl_pct'),
        combined_stats.get('blk_pct'),
        combined_stats.get('tov_pct')
    ))

    conn.commit()
    print(f"Successfully inserted stats for {player_name} in the {season} season.")
    conn.close()

def insert_all_players_stats(start_season, end_season):
    """Fetch and insert stats for all active players from start_season to end_season into the database."""
    for season in range(start_season, end_season + 1):
        #season_str = f"{season}-{str(season + 1)[-2:]}"
        print(f"Processing season {season}")
        
        # Get the list of active players for the season
        active_players = get_active_players(season)
        total_players = len(active_players)
        
        for i, player_name in enumerate(active_players):
            player = next((p for p in players.get_players() if p['full_name'] == player_name), None)
            if player:
                player_id = player['id']
                print(f"Scraping stats for {player_name} ({i + 1}/{total_players}) for season {season}")
                insert_player_stats(player_id, player_name, season)
                time.sleep(5)  # Add a 5-second delay between requests to avoid rate limits
            else:
                print(f"Player {player_name} not found in NBA API.")
        
        print(f"Processed {total_players} players for season {season}.")

# Example usage
if __name__ == "__main__":
    create_db()  # Ensure the database and table are created

    # Insert stats for all active players from the 2009-2010 season to the current season
    start_season = 2009
    end_season = 2025  # Update this to the current season format used by Basketball Reference
    insert_all_players_stats(start_season, end_season)
