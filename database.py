import sqlite3

DATABASE = "gyms.db"

# =========================================================
# Standard Plate Templates
# =========================================================
STANDARD_LB_PLATES = [
    (2.5, 2),
    (5, 4),
    (10, 2),
    (25, 2),
    (35, 2),
    (45, 2)
]

STANDARD_KG_PLATES = [
    (1.25, 2),
    (2.5, 2),
    (5, 2),
    (10, 2),
    (15, 2),
    (20, 2),
    (25, 2)
]

# =========================================================
# Database Connection
# =========================================================
def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

# =========================================================
# Create / Update Database Tables
# =========================================================
def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Create gyms table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gyms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            default_unit TEXT NOT NULL,
            bar_weight REAL NOT NULL DEFAULT 45
        )
    """)

    # Create plates table if it does not exist
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

    # =====================================================
    # Database Migration
    # =====================================================
    # Check whether an older database is missing bar_weight
    cursor.execute("PRAGMA table_info(gyms)")
    columns = [row[1] for row in cursor.fetchall()]

    if "bar_weight" not in columns:
        cursor.execute("""
            ALTER TABLE gyms
            ADD COLUMN bar_weight REAL NOT NULL DEFAULT 45
        """)

        # Existing KG gyms should use a 20 KG bar
        cursor.execute("""
            UPDATE gyms
            SET bar_weight = 20
            WHERE UPPER(default_unit) = 'KG'
        """)

    connection.commit()
    connection.close()

# =========================================================
# Gym Functions
# =========================================================
def add_gym(name, default_unit, bar_weight):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO gyms
        (name, default_unit, bar_weight)
        VALUES (?, ?, ?)
        """,
        (
            name,
            default_unit.upper(),
            bar_weight
        )
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
        SELECT
            id,
            name,
            default_unit,
            bar_weight
        FROM gyms
        ORDER BY name
        """
    )

    gyms = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return gyms

def get_gym(gym_id):
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            default_unit,
            bar_weight
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

def update_gym(
    gym_id,
    name,
    default_unit,
    bar_weight
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE gyms
        SET
            name = ?,
            default_unit = ?,
            bar_weight = ?
        WHERE id = ?
        """,
        (
            name,
            default_unit.upper(),
            bar_weight,
            gym_id
        )
    )

    connection.commit()
    connection.close()

def delete_gym(gym_id):
    connection = get_connection()
    cursor = connection.cursor()

    # Delete all plates belonging to the gym
    cursor.execute(
        """
        DELETE FROM plates
        WHERE gym_id = ?
        """,
        (gym_id,)
    )

    # Delete the gym
    cursor.execute(
        """
        DELETE FROM gyms
        WHERE id = ?
        """,
        (gym_id,)
    )

    connection.commit()
    connection.close()

# =========================================================
# Plate Functions
# =========================================================
def add_plate(
    gym_id,
    weight,
    unit,
    color,
    quantity
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO plates
        (
            gym_id,
            weight,
            unit,
            color,
            quantity
        )
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

    plates = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return plates

def get_plates_by_unit(
    gym_id,
    unit
):
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
        (
            gym_id,
            unit.upper()
        )
    )

    plates = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return plates

def update_plate(
    plate_id,
    weight,
    unit,
    color,
    quantity
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE plates
        SET
            weight = ?,
            unit = ?,
            color = ?,
            quantity = ?
        WHERE id = ?
        """,
        (
            weight,
            unit.upper(),
            color,
            quantity,
            plate_id
        )
    )

    connection.commit()
    connection.close()

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
# Standard Plate Set
# =========================================================
def add_standard_plates(
    gym_id,
    unit
):
    unit = unit.upper()

    if unit == "LB":
        standard_plates = STANDARD_LB_PLATES
    elif unit == "KG":
        standard_plates = STANDARD_KG_PLATES
    else:
        raise ValueError(
            "Unit must be LB or KG"
        )

    for weight, quantity in standard_plates:
        add_plate(
            gym_id,
            weight,
            unit,
            "none",
            quantity
        )

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
        "LB",
        45
    )

    add_standard_plates(
        gym_id,
        "LB"
    )

    return gym_id

# =========================================================
# Initialize Database
# =========================================================
create_tables()