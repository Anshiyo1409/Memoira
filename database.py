import sqlite3
from datetime import datetime

DB_PATH = "data/memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        audio_path TEXT,
        image_path TEXT,
        created_at TEXT,
        doc_path TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_memory(content, audio_path=None, image_path=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memories (content, audio_path, image_path, created_at) VALUES (?, ?, ?, ?)",
        (content, audio_path, image_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_memories():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM memories ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def search_memories(keyword):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM memories WHERE content LIKE ? ORDER BY id DESC",
        (f"%{keyword}%",)
    )
    rows = c.fetchall()
    conn.close()
    return rows
def add_memory(content, audio_path=None, image_path=None, doc_path=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memories (content, audio_path, image_path, doc_path, created_at) VALUES (?, ?, ?, ?, ?)",
        (content, audio_path, image_path, doc_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()