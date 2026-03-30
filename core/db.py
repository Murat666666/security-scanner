import sqlite3
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE_DIR, "scans.db")


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY,
        host TEXT,
        ports TEXT,
        result TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_scan(host, ports, result):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    INSERT INTO scans (host, ports, result, created_at)
    VALUES (?, ?, ?, ?)
    """, (host, ports, json.dumps(result), datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_scans():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM scans ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "host": r[1],
            "ports": r[2],
            "result": json.loads(r[3]),
            "created_at": r[4]
        }
        for r in rows
    ]