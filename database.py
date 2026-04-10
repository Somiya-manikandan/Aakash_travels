import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# users
c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT)
""")

# packages
c.execute("""
CREATE TABLE IF NOT EXISTS packages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
place TEXT,
price TEXT)
""")

# bookings
c.execute("""
CREATE TABLE IF NOT EXISTS bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
place TEXT,
payment TEXT)
""")

conn.commit()
conn.close()
