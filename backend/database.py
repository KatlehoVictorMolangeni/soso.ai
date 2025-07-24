import sqlite3

def init_db():
    conn = sqlite3.connect("soso.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            tone TEXT,
            topics TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            query TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_user_profile(user_id):
    conn = sqlite3.connect("soso.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return {"user_id": row[0], "tone": row[1], "topics": row[2]} if row else None

def save_user_profile(user_id, tone, topics):
    conn = sqlite3.connect("soso.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, tone, topics)
        VALUES (?, ?, ?)
    """, (user_id, tone, ",".join(topics) if topics else ""))
    conn.commit()
    conn.close()

def save_interaction(user_id, query, response):
    conn = sqlite3.connect("soso.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (user_id, query, response) VALUES (?, ?, ?)", (user_id, query, response))
    conn.commit()
    conn.close()