from datetime import datetime
import sqlite3
from sqlite3 import Error

CONNECTION_STRING = r".\data\chests.db"


def create_connection():
    """create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(CONNECTION_STRING)
        return conn
    except Error as e:
        print(e)


def add_chest(player_name, chest_type):
    """
    Create a new chest into the chests table
    :param conn:
    :param chest:
    :return: None
    """
    conn = create_connection()
    sql = """ INSERT INTO chests_log(player_name, chest_type)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, (player_name, chest_type))
    conn.commit()
    return


def add_chest_type(chest_type):
    """
    Create a new chest type into the chests_type table
    :param conn:
    :param chest_type:
    :return: None
    """
    conn = create_connection()
    sql = """ INSERT INTO chests_type(name, points, required)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, (chest_type, 0, 0))
    conn.commit()
    return


def get_chest_type(chest_type):
    """
    Get a chest type from the chests_type table
    :param conn:
    :param chest_type:
    :return: chest_type
    """
    conn = create_connection()
    sql = """ SELECT * FROM chests_type WHERE name=? """
    cur = conn.cursor()
    cur.execute(sql, (chest_type,))
    row = cur.fetchone()
    return row


def add_player(player_name):
    """
    Create a new player into the players table
    :param conn:
    :param player_name:
    :return: None
    """
    conn = create_connection()
    sql = """ INSERT INTO players(player_name)
              VALUES(?) """
    cur = conn.cursor()
    cur.execute(sql, (player_name,))
    conn.commit()
    return


def get_player(player_name):
    """
    Get a player from the players table
    :param conn:
    :param player_name:
    :return: player
    """
    conn = create_connection()
    sql = """ SELECT * FROM players WHERE player_name=? """
    cur = conn.cursor()
    cur.execute(sql, (player_name,))
    row = cur.fetchone()
    return row


def get_all_players():
    """
    Get all players from the players table
    :param conn:
    :return: players
    """
    conn = create_connection()
    sql = """ SELECT * FROM players order by player_name ASC """
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows


def get_all_chest_types():
    """
    Get all chest types from the chests_type table
    :param conn:
    :return: chest_types
    """
    conn = create_connection()
    sql = """ SELECT * FROM chests_type ORDER BY order_by DESC """
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows


def get_player_chest_count(player_name, chest_type):
    """
    Get the count of a specific chest type for a specific player
    :param conn:
    :param player_name:
    :param chest_type:
    :return: count
    """
    conn = create_connection()
    sql = """ SELECT COUNT(*) FROM chests_log WHERE player_name=? AND chest_type=? """
    cur = conn.cursor()
    cur.execute(sql, (player_name, chest_type))
    row = cur.fetchone()
    return row[0]


def export():
    try:        
        output = "# TBP chests 16/04/2025 - 20/04/2025 \n"
        output += ">[!NOTE]\n"
        output += ">This data is collected manually by opening chests one by one, so it may not be 100% accurate. \n\n"
        output += ">[!WARNING]\n"
        output += ">If you are missing from this list, please contact Dionysus. \n\n"
        output += "### Last refreshed: " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n\n"

        players = get_all_players()
        chest_types = get_all_chest_types()
        
        all_chest_types = ""
        all_separators = ""

        for chest in chest_types:
            all_chest_types += f"{chest[0]} ({chest[1]}) | "
            all_separators += "--- | "

        output += f"| Player | {all_chest_types.rstrip(' | ')} | Total Chests | Total Points |\n"
        output += f"| --- | {all_separators.rstrip(' | ')} | --- | --- |\n"

        for player in players:
            output += f"| {player[1]} |"
            total = 0
            total_points = 0
            for chest in chest_types:
                count = get_player_chest_count(player[1], chest[0])
                output += f" {count} |"
                total += count
                total_points += count * chest[1]
            output += f" {total} | {total_points} |\n"

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(output)
    except Error as e:
        print(e)
