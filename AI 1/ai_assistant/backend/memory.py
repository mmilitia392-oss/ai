import sqlite3

conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
)
""")
conn.commit()

def save_memory(text):
    cursor.execute("INSERT INTO memory (content) VALUES (?)", (text,))
    conn.commit()

def get_memories():
    cursor.execute("SELECT content FROM memory")
    return [row[0] for row in cursor.fetchall()]

def should_save(text):
    keywords = ["remember", "my goal", "important", "i like", "i prefer"]
    return any(k in text.lower() for k in keywords)
