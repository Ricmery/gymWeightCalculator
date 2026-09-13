import sqlite3

DATABASE = "gyms.db"

# =========================================================
# Database Connection
# =========================================================
def get_connection():
    return sqlite3.connect(DATABASE)

# =========================================================
# Create Database Tables
# =========================================================
def create_tables():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gyms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
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
                ON DELETE CASCADE
        )
    """)
    connection.commit()
    connection.close()

# =========================================================
# Gym Functions
# =========================================================
def add_gym(name, default_unit):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO gyms (name, default_unit)
        VALUES (?, ?)
        """,
        (name, default_unit.upper())
    )
    connection.commit()
    gym_id = cursor.lastrowid
    connection.close()
    return gym_id

def get_gyms():
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, name, default_unit
        FROM gyms
        ORDER BY name
        """
    )
    gyms = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return gyms

def get_gym(gym_id):
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, name, default_unit
        FROM gyms
        WHERE id = ?
        """,
        (gym_id,)
    )
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return dict(row)

def delete_gym(gym_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM plates WHERE gym_id = ?",
        (gym_id,)
    )
    cursor.execute(
        "DELETE FROM gyms WHERE id = ?",
        (gym_id,)
    )
    connection.commit()
    connection.close()

# =========================================================
# Plate Functions
# =========================================================
def add_plate(gym_id, weight, unit, color, quantity):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO plates
        (gym_id, weight, unit, color, quantity)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            gym_id,
            weight,
            unit.upper(),
            color,
            quantity
        )
    )
    connection.commit()
    plate_id = cursor.lastrowid
    connection.close()
    return plate_id

def get_plates(gym_id):
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            id,
            gym_id,
            weight,
            unit,
            color,
            quantity
        FROM plates
        WHERE gym_id = ?
        ORDER BY weight
        """,
        (gym_id,)
    )
    plates = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return plates

def get_plates_by_unit(gym_id, unit):
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            id,
            gym_id,
            weight,
            unit,
            color,
            quantity
        FROM plates
        WHERE gym_id = ?
        AND unit = ?
        ORDER BY weight
        """,
        (gym_id, unit.upper())
    )
    plates = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return plates

def delete_plate(plate_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM plates
        WHERE id = ?
        """,
        (plate_id,)
    )
    connection.commit()
    connection.close()

# =========================================================
# Test Gym
# =========================================================
def create_test_gym():
    existing_gyms = get_gyms()
    for gym in existing_gyms:
        if gym["name"] == "Test Gym LB":
            return gym["id"]
    gym_id = add_gym(
        "Test Gym LB",
        "LB"
    )
    test_plates = [
        (2.5, "none", 2),
        (5, "none", 4),
        (10, "none", 2),
        (25, "none", 2),
        (35, "none", 2),
        (45, "none", 2)
    ]
    for weight, color, quantity in test_plates:
        add_plate(
            gym_id,
            weight,
            "LB",
            color,
            quantity
        )
    return gym_id

# =========================================================
# Initialize Database
# =========================================================
create_tables()