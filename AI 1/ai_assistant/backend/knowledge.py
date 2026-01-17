import sqlite3

conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
)
""")
conn.commit()

def save_knowledge(text):
    cursor.execute("INSERT INTO knowledge (content) VALUES (?)", (text,))
    conn.commit()

def search_knowledge(query):
    cursor.execute(
        "SELECT content FROM knowledge WHERE content LIKE ? LIMIT 5",
        (f"%{query}%",)
    )
    return [row[0] for row in cursor.fetchall()]
