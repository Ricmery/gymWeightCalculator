import sqlite3

DATABASE = "gyms.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gyms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            default_unit TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gym_id INTEGER NOT NULL,
            weight REAL NOT NULL,
            unit TEXT NOT NULL,
            color TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (gym_id)
                REFERENCES gyms(id)
        )
    """)

    connection.commit()
    connection.close()

STANDARD_LB_PLATES = [
    (2.5, "none", 2),
    (5, "none", 4),
    (10, "none", 2),
    (25, "none", 2),
    (35, "none", 2),
    (45, "none", 2)
]

STANDARD_KG_PLATES = [
    (1.25, "white", 2),
    (2.5, "red", 2),
    (5, "blue", 2),
    (10, "green", 2),
    (15, "yellow", 2),
    (20, "blue", 2),
    (25, "red", 2)
]