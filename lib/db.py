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

def export():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT player_name, chest_type, count(1) FROM chests_log GROUP BY player_name, chest_type ORDER BY player_name ASC")
        rows = cur.fetchall()

        output = "# TBP chests 16/04/2025 - 20/04/2025\n\n"
        output += "| Player  | Chest Type | Count |\n"
        output += "| --- | --- | --- |\n"
        for row in rows:
            output += f"| {row[0]} | {row[1]} | {row[2]} |\n"
        
        with open("output.md", "w", encoding="utf-8") as f:
            f.write(output)
    except Error as e:
        print(e)
