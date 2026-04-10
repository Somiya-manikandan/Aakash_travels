from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

# Auto create DB (for Render)
if not os.path.exists("database.db"):
    import database

app = Flask(__name__)
app.secret_key = "aakash"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- HOME ----------------
@app.route('/')
def home():
    db = get_db()
    packages = db.execute("SELECT * FROM packages").fetchall()
    return render_template('index.html', packages=packages)

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        db.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                   (request.form['name'], request.form['email'], request.form['password']))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=? AND password=?",
                          (request.form['email'], request.form['password'])).fetchone()
        if user:
            session['user'] = user['id']
            session['name'] = user['name']

            if request.form['email'] == "admin@gmail.com":
                return redirect('/admin')

            return redirect('/')
    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- BOOK ----------------
@app.route('/book/<int:id>', methods=['GET','POST'])
def book(id):
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        db = get_db()
        db.execute("INSERT INTO bookings (user_id, package_id) VALUES (?,?)",
                   (session['user'], id))
        db.commit()
        return "✅ Booking Successful!"

    return render_template('booking.html')

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    db = get_db()

    bookings = db.execute("""
        SELECT bookings.id, users.name, packages.place
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        JOIN packages ON bookings.package_id = packages.id
    """).fetchall()

    packages = db.execute("SELECT * FROM packages").fetchall()

    return render_template('admin.html', packages=packages, bookings=bookings)

# ---------------- DELETE ----------------
@app.route('/delete_package/<int:id>')
def delete_package(id):
    db = get_db()
    db.execute("DELETE FROM packages WHERE id=?", (id,))
    db.commit()
    return redirect('/admin')

# ---------------- EDIT ----------------
@app.route('/edit_package/<int:id>')
def edit_package(id):
    db = get_db()
    package = db.execute("SELECT * FROM packages WHERE id=?", (id,)).fetchone()
    return render_template('edit_package.html', package=package)

# ---------------- UPDATE ----------------
@app.route('/update_package/<int:id>', methods=['POST'])
def update_package(id):
    db = get_db()
    db.execute("UPDATE packages SET place=?, price=? WHERE id=?",
               (request.form['place'], request.form['price'], id))
    db.commit()
    return redirect('/admin')

# ---------------- ADD ----------------
@app.route('/add_package', methods=['POST'])
def add_package():
    db = get_db()
    db.execute("INSERT INTO packages (place, price) VALUES (?,?)",
               (request.form['place'], request.form['price']))
    db.commit()
    return redirect('/admin')

# ✅ IMPORTANT FOR RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
