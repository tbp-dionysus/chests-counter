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


def export():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT p.player_name, cl.chest_type, IFNULL(count(*), 0) as chest_count " 
            "FROM players p "
            "LEFT JOIN chests_log cl on p.player_name = cl.player_name "
            "GROUP BY p.player_name, cl.chest_type "
        )
        rows = cur.fetchall()

        output = "# TBP chests 16/04/2025 - 20/04/2025 \n"
        output += "> [!INFO]\n"
        output += "> This data is collected manually by opening chests one by one, so it may not be 100% accurate. \n"
        output += "> [!WARNING]\n"
        output += "> If you are missing from this list, please contact Dionysus. \n"
        output += "### Total: " + str(sum(row[2] for row in rows)) + "\n"
        output += "### Last refreshed: " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n\n"
        output += "| Player  | Chest Type | Count |\n"
        output += "| --- | --- | --- |\n"
        for row in rows:
            output += f"| {row[0]} | {row[1]} | {row[2]} |\n"
        
        

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(output)
    except Error as e:
        print(e)
