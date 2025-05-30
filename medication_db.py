# -*- coding: utf-8 -*-
"""
@Author: Jieying Li
@Created Date: 2025-05-27 21:58:46
@Path: /medication_db.py
"""

import sqlite3

DB_FILE = "medication_tracker.db"

def init_db():
    """
    Initialize the SQLite database with medications and logs tables.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            tag_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            usage TEXT,         -- administration method
            dosage TEXT,        -- amount and frequency
            schedule TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_id TEXT NOT NULL,
            action TEXT NOT NULL,
            amount TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(tag_id) REFERENCES medications(tag_id)
        )
    """)
    conn.commit()
    conn.close()

def get_medication_info(tag_id):
    """
    Retrieve medication information by RFID tag ID.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, usage, dosage, schedule FROM medications WHERE tag_id = ?", (tag_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def seed_data():
    """
    Seed the database with initial data for medications and logs.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Seed data for medications
    medications = [
        (
            "1234567890",
            "Aspirin",
            "Reduces pain, fever, and inflammation.",
            "Take with water after meals.",
            "1 tablet, up to 3 times a day",
            "08,15,19,20,21"
        ),
        (
            "0987654321",
            "Vitamin D",
            "Supports calcium absorption and bone health.",
            "Take with food once a week.",
            "1 capsule",
            "09"
        ),
        (
            "1122334455",
            "Ibuprofen",
            "Used for pain relief and inflammation.",
            "Take with food or milk to reduce stomach upset.",
            "1 tablet every 6 hours as needed; max 4 per day",
            ""
        ),
        (
            "2233445566",
            "Metformin",
            "Helps control blood sugar levels in type 2 diabetes.",
            "Take with meals to reduce gastrointestinal side effects.",
            "500 mg, twice daily",
            "15,20"
        ),
    ]


    cursor.executemany("""
        INSERT OR IGNORE INTO medications (tag_id, name, description, usage, dosage, schedule)
        VALUES (?, ?, ?, ?, ?, ?)
    """, medications)

    # Seed data for logs
    logs = [
        (1, "1234567890", "Taken", "2025-05-27 08:00:00"),
        (2, "0987654321", "Taken", "2025-05-29 09:00:00"),
        (3, "1122334455", "Taken", "2025-05-27 14:00:00"),
        (4, "1234567890", "Skipped", "2025-05-28 08:00:00"),
        (5, "0987654321", "Taken", "2025-05-30 09:00:00"),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO logs (id, tag_id, action, timestamp)
        VALUES (?, ?, ?, ?)
    """, logs)

    conn.commit()
    conn.close()


# init_db()
# seed_data()
# info = get_medication_info("1234567890")  # Example usage to retrieve medication info
# print(info)  # Output: ('Aspirin', 'Take one tablet daily after meals', '08:00')