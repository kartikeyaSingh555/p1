import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS User(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    reg_no TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Event(
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    event_date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Blog(
    blog_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    title TEXT,
    content TEXT,
    created_at TEXT,
    FOREIGN KEY(event_id) REFERENCES Event(event_id)
)
""")

conn.commit()
conn.close()
print("Database created successfully!")
