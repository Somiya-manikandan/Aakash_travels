import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(db_path)

c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS packages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
place TEXT,
price TEXT)
""")

# IMPORTANT: payment column included
c.execute("""
CREATE TABLE IF NOT EXISTS bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
place TEXT,
payment TEXT)
""")

conn.commit()
conn.close()
