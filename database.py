import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

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

c.execute("""
CREATE TABLE IF NOT EXISTS bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
place TEXT,
payment TEXT)
""")

conn.commit()
conn.close()
