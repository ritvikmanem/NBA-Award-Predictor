import os
import sqlite3
from scraper import scrape_combined_stats  # Import the scraper function
from nba_api.stats.static import players
import time

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
    conn.close()

def insert_all_players_stats(season):
    """Fetch and insert stats for all active players into the database."""
    all_players = players.get_active_players()
    total_players = len(all_players)
    for i, player in enumerate(all_players):
        player_id = player['id']
        player_name = player['full_name']
        print(f"Scraping stats for {player_name} ({i + 1}/{total_players})")
        insert_player_stats(player_id, player_name, season)
        time.sleep(5)  # Add a 5-second delay between requests to avoid rate limits
    print(f"Processed {total_players} players.")

# Example usage
if __name__ == "__main__":
    create_db()  # Ensure the database and table are created

    # Insert stats for all active players for the current season
    current_season = "2025"  # Update this to the current season format used by Basketball Reference
    insert_all_players_stats(current_season)
