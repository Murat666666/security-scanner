import sqlite3
import json
import os

DB = "scans.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY,
        host TEXT,
        ports TEXT,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_scan(host, ports, result):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "INSERT INTO scans (host, ports, result) VALUES (?, ?, ?)",
        (host, ports, json.dumps(result))
    )

    conn.commit()
    conn.close()
