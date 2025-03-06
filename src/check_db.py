import sqlite3

# Define the database path
DB_PATH = "/home/manemritvik/projects/repos/NBA-Award-Predictor/data/mvp_stats.db"

def print_all_data():
    """Print all data from the mvp_stats table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""SELECT season, player_id, player_name, pts_per_g, ast_per_g, trb_per_g, blk_per_g, efg_pct, ft_pct, stl_per_g, usg_pct, ast_pct, trb_pct, per, ws, ws_per_48, bpm, obpm, dbpm, vorp, stl_pct, blk_pct, tov_pct FROM mvp_stats""")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

def delete_all_data():
    """Delete all data from the mvp_stats table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM mvp_stats")
    conn.commit()
    print("All data deleted from mvp_stats table.")

    conn.close()




# Example usage
if __name__ == "__main__":
    # Uncomment the function you want to use
    print_all_data()
    #delete_all_data()