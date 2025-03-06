import os
import sqlite3
from scraper import scrape_combined_stats  # Import the scraper function
from nba_api.stats.static import players
import time

# Define a fixed database path
DB_PATH = "/home/manemritvik/projects/repos/NBA-Award-Predictor/data/nba_stats.db"

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
        team_abbreviation TEXT,
        games_played INTEGER,
        minutes REAL,
        points REAL,
        rebounds REAL,
        assists REAL,
        steals REAL,
        blocks REAL,
        fg_pct REAL,
        three_pt_pct REAL,
        ft_pct REAL,
        per REAL,
        ws REAL,
        ws_per_48 REAL,
        bpm REAL,
        obpm REAL,
        dbpm REAL,
        vorp REAL,
        usg_pct REAL,
        ast_pct REAL,
        trb_pct REAL,
        stl_pct REAL,
        blk_pct REAL,
        tov_pct REAL,
        efg_pct REAL,
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
    INSERT OR REPLACE INTO mvp_stats (season, player_id, player_name, team_abbreviation, games_played, minutes, points, rebounds, assists, steals, blocks, fg_pct, three_pt_pct, ft_pct, per, ws, ws_per_48, bpm, obpm, dbpm, vorp, usg_pct, ast_pct, trb_pct, stl_pct, blk_pct, tov_pct, efg_pct)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        season,
        player_id,
        player_name,
        combined_stats.get('team_abbreviation'),
        combined_stats.get('g'),
        combined_stats.get('mp'),
        combined_stats.get('pts_per_g'),
        combined_stats.get('trb_per_g'),
        combined_stats.get('ast_per_g'),
        combined_stats.get('stl_per_g'),
        combined_stats.get('blk_per_g'),
        combined_stats.get('fg_pct'),
        combined_stats.get('three_pt_pct'),
        combined_stats.get('ft_pct'),
        combined_stats.get('per'),
        combined_stats.get('ws'),
        combined_stats.get('ws_per_48'),
        combined_stats.get('bpm'),
        combined_stats.get('obpm'),
        combined_stats.get('dbpm'),
        combined_stats.get('vorp'),
        combined_stats.get('usg_pct'),
        combined_stats.get('ast_pct'),
        combined_stats.get('trb_pct'),
        combined_stats.get('stl_pct'),
        combined_stats.get('blk_pct'),
        combined_stats.get('tov_pct'),
        combined_stats.get('efg_pct')
    ))

    conn.commit()
    conn.close()

def insert_all_players_stats(season):
    """Fetch and insert stats for all active players into the database."""
    all_players = players.get_active_players()
    for player in all_players:
        player_id = player['id']
        player_name = player['full_name']
        print(f"Scraping stats for {player_name}")
        insert_player_stats(player_id, player_name, season)
        time.sleep(3)  # Add a 3-second delay between requests to avoid rate limits

# Example usage
if __name__ == "__main__":
    create_db()  # Ensure the database and table are created

    # Insert stats for all active players for the current season
    current_season = "2025"  # Update this to the current season format used by Basketball Reference
    insert_all_players_stats(current_season)
