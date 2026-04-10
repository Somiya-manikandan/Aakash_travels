import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT)")
conn.execute("CREATE TABLE packages (id INTEGER PRIMARY KEY AUTOINCREMENT, place TEXT, price INTEGER)")
conn.execute("CREATE TABLE bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, package_id INTEGER)")

conn.execute("INSERT INTO packages (place, price) VALUES ('Goa', 5000)")
conn.execute("INSERT INTO packages (place, price) VALUES ('Manali', 8000)")
conn.execute("INSERT INTO packages (place, price) VALUES ('Kerala', 7000)")

conn.commit()
conn.close()

print("Database Created!")