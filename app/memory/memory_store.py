# app/memory/memory_store.py

import sqlite3
import json
import os
from typing import Dict

DB_FILE = "memory.db"

def init_memory():
    """Initialize SQLite memory table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source TEXT,
            classification TEXT,
            agent_data TEXT,
            actions TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_entry(source: str, classification: dict, agent_data: dict, actions: dict):
    """Insert a new memory log entry."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO memory (timestamp, source, classification, agent_data, actions)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        agent_data.get("timestamp", ""),
        source,
        json.dumps(classification, ensure_ascii=False),
        json.dumps(agent_data, ensure_ascii=False),
        json.dumps(actions, ensure_ascii=False)
    ))
    conn.commit()
    conn.close()

def get_all_entries() -> list:
    """Return all stored memory log entries."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM memory')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize DB if not already present
if not os.path.exists(DB_FILE):
    init_memory()
