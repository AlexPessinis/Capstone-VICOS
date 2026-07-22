# modules/database.py

import sqlite3

def init_db():
    conn = sqlite3.connect("vicos.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        rpm REAL,
        coolant REAL,
        speed REAL,
        iat REAL,
        maf REAL,
        fuel_level REAL,
        mpg REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trip (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT,
        end_time TEXT,
        miles REAL,
        avg_speed REAL,
        max_speed REAL,
        avg_mpg REAL
    )
    """)

    conn.commit()
    conn.close()

def insert_telemetry(data):
    conn = sqlite3.connect("vicos.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO telemetry (timestamp, rpm, coolant, speed, iat, maf, fuel_level, mpg)
    VALUES (datetime('now'), ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["rpm"],
        data["coolant"],
        data["speed"],
        data["iat"],
        data["maf"],
        data["fuel_level"],
        data.get("mpg")
    ))

    conn.commit()
    conn.close()
