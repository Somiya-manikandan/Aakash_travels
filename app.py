from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- HOME ----------
@app.route('/')
def home():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM packages")
    packages = c.fetchall()

    conn.close()
    return render_template('index.html', packages=packages)

# ---------- REGISTER ----------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':

        name = request.form['name']   # 👈 ADD THIS LINE HERE
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                  (name,email,password))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email=? AND password=?",
                  (email,password))

        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = email        # for login check
            session['name'] = user[1]      # 👈 store NAME

            return redirect(url_for('home'))
        else:
            return "Invalid login"

    return render_template('login.html')

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# ---------- PAYMENT ----------
@app.route('/payment/<int:id>', methods=['GET','POST'])
def payment(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # get package
    c.execute("SELECT * FROM packages WHERE id=?", (id,))
    package = c.fetchone()

    if not package:
        return "Package not found"

    if request.method == 'POST':
        method = request.form.get('method')

        if not method:
            return "Select payment method"

        email = session['user']

        c.execute("SELECT name FROM users WHERE email=?", (email,))
        user = c.fetchone()

        if not user:
            return "User not found"

        name = user[0]
        place = package[1]

        c.execute("INSERT INTO bookings (name, place, payment) VALUES (?,?,?)",
                  (name, place, method))

        conn.commit()
        conn.close()

        # ✅ 👉 PUT HERE (VERY IMPORTANT)
        return redirect(url_for('success'))

    conn.close()
    return render_template('payment.html', package=package)
# ---------- SUCCESS ----------
@app.route('/success')
def success():
    return render_template('success.html')

# ---------- ADMIN ----------
@app.route('/admin')
def admin():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM packages")
    packages = c.fetchall()

    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()

    conn.close()
    return render_template('admin.html', packages=packages, bookings=bookings)

# ---------- ADD PACKAGE ----------
@app.route('/add_package', methods=['POST'])
def add_package():
    place = request.form['place']
    price = request.form['price']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("INSERT INTO packages (place,price) VALUES (?,?)",
              (place,price))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

# ---------- DELETE ----------
@app.route('/delete/<int:id>')
def delete_package(id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("DELETE FROM packages WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

# ---------- EDIT ----------
@app.route('/edit/<int:id>')
def edit_package(id):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM packages WHERE id=?", (id,))
    package = c.fetchone()

    conn.close()
    return render_template('edit_package.html', package=package)

@app.route('/update/<int:id>', methods=['POST'])
def update_package(id):
    place = request.form['place']
    price = request.form['price']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("UPDATE packages SET place=?, price=? WHERE id=?",
              (place,price,id))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
