from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- HOME ----------------
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM packages")
    packages = c.fetchall()

    conn.close()

    return render_template('index.html', packages=packages)

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                  (name,email,password))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email=? AND password=?",
                  (email,password))

        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = email
            return redirect(url_for('home'))

    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# ---------------- PAYMENT ----------------
@app.route('/payment/<int:id>', methods=['GET','POST'])
def payment(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        method = request.form['method']
        email = session['user']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # user name
        c.execute("SELECT name FROM users WHERE email=?", (email,))
        name = c.fetchone()[0]

        # package
        c.execute("SELECT place FROM packages WHERE id=?", (id,))
        place = c.fetchone()[0]

        # insert booking
        c.execute("INSERT INTO bookings (name, place, payment) VALUES (?,?,?)",
                  (name, place, method))

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('payment.html')

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM packages")
    packages = c.fetchall()

    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()

    conn.close()

    return render_template('admin.html', packages=packages, bookings=bookings)

# ---------------- ADD PACKAGE ----------------
@app.route('/add_package', methods=['POST'])
def add_package():
    place = request.form['place']
    price = request.form['price']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO packages (place,price) VALUES (?,?)",
              (place,price))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete_package(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("DELETE FROM packages WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

# ---------------- EDIT ----------------
@app.route('/edit/<int:id>')
def edit_package(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM packages WHERE id=?", (id,))
    package = c.fetchone()

    conn.close()

    return render_template('edit_package.html', package=package)

@app.route('/update/<int:id>', methods=['POST'])
def update_package(id):
    place = request.form['place']
    price = request.form['price']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("UPDATE packages SET place=?, price=? WHERE id=?",
              (place,price,id))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
