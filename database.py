import sqlite3
import os

DB_NAME = "client_prospects.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_posts (
            post_id TEXT PRIMARY KEY,
            username TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_already_processed(post_id: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM processed_posts WHERE post_id = ?', (post_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_as_processed(post_id: str, username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO processed_posts (post_id, username) VALUES (?, ?)', (post_id, username))
    conn.commit()
    conn.close()