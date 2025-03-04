import os
import sqlite3
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

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
        PRIMARY KEY (season, player_id)
    )
    """)
    
    conn.commit()
    conn.close()

def get_player_stats(player_name, season):
    """Retrieve stats for a specific player and season."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM mvp_stats
    WHERE player_name = ? AND season = ?
    """, (player_name, season))

    stats = cursor.fetchone()
    conn.close()
    return stats

def insert_player_stats(player_name, season):
    """Fetch and insert player stats from NBA API into the database."""
    player_dict = players.find_players_by_full_name(player_name)
    if not player_dict:
        print(f"Player {player_name} not found.")
        return

    player_id = player_dict[0]['id']
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    stats = career.get_data_frames()[0]

    season_stats = stats[stats['SEASON_ID'] == season]
    if season_stats.empty:
        print(f"No stats found for {player_name} in the {season} season.")
        return

    season_stats = season_stats.iloc[0]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO mvp_stats (season, player_id, player_name, team_abbreviation, games_played, minutes, points, rebounds, assists, steals, blocks, fg_pct, three_pt_pct, ft_pct)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        season,
        player_id,
        player_name,
        season_stats['TEAM_ABBREVIATION'],
        int(season_stats['GP']),
        float(season_stats['MIN']),
        float(season_stats['PTS']),
        float(season_stats['REB']),
        float(season_stats['AST']),
        float(season_stats['STL']),
        float(season_stats['BLK']),
        float(season_stats['FG_PCT']),
        float(season_stats['FG3_PCT']),
        float(season_stats['FT_PCT'])
    ))

    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    create_db()  # Ensure the database and table are created

    # Insert LeBron's stats for the current season
    current_season = "2024-25"  # Update this to the current season format used by NBA API
    insert_player_stats("LeBron James", current_season)

    # Retrieve and print LeBron's stats for the current season
    lebron_stats = get_player_stats("LeBron James", current_season)
    
    if lebron_stats:
        print(f"LeBron's stats for the {current_season} season:")
        print(f"Team: {lebron_stats[3]}")
        print(f"Games Played: {lebron_stats[4]}")
        print(f"Minutes: {lebron_stats[5]}")
        print(f"Points: {lebron_stats[6]}")
        print(f"Rebounds: {lebron_stats[7]}")
        print(f"Assists: {lebron_stats[8]}")
        print(f"Steals: {lebron_stats[9]}")
        print(f"Blocks: {lebron_stats[10]}")
        print(f"Field Goal Percentage: {lebron_stats[11]}")
        print(f"Three-Point Percentage: {lebron_stats[12]}")
        print(f"Free Throw Percentage: {lebron_stats[13]}")
    else:
        print("No stats found for LeBron in the current season.")
