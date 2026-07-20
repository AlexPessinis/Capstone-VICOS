# modules/database.py

import sqlite3

def init_db():
    conn = sqlite3.connect("vicos.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        rpm INTEGER,
        speed REAL,
        coolant REAL,
        voltage REAL
    )
    """)

    conn.commit()
    conn.close()
