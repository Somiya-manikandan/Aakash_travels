✅ STEP 1: FIX DATABASE (VERY IMPORTANT)

Run this once:

import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# recreate bookings table safely
c.execute("DROP TABLE IF EXISTS bookings")

c.execute("""
CREATE TABLE bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
place TEXT,
payment TEXT)
""")

conn.commit()
conn.close()
✅ STEP 2: FIX app.py PAYMENT ROUTE (SAFE VERSION)

Replace your payment function with this 👇

@app.route('/payment/<int:id>', methods=['GET','POST'])
def payment(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # get package safely
    c.execute("SELECT * FROM packages WHERE id=?", (id,))
    package = c.fetchone()

    if not package:
        return "Package not found"

    if request.method == 'POST':
        method = request.form.get('method')

        if not method:
            return "Select payment method"

        email = session['user']

        # get user name safely
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

        return redirect(url_for('success'))

    conn.close()
    return render_template('payment.html', package=package)
✅ STEP 3: ADD SUCCESS PAGE ROUTE

Add this in app.py 👇

@app.route('/success')
def success():
    return render_template('success.html')
💳 STEP 4: UPDATE payment.html (WITH UI)
<!DOCTYPE html>
<html>
<head>
<title>Payment</title>
<style>
body { text-align:center; font-family:Arial; }

.box {
    margin-top:50px;
}

button {
    background:#28a745;
    color:white;
    padding:10px;
    border:none;
    border-radius:5px;
}
</style>
</head>
<body>

<h2>💳 Choose Payment Method</h2>

<div class="box">
<form method="post">

<input type="radio" name="method" value="UPI" required> UPI<br><br>
<input type="radio" name="method" value="Card"> Card<br><br>
<input type="radio" name="method" value="Cash"> Cash<br><br>

<button type="submit">Pay Now</button>

</form>
</div>

</body>
</html>
🎉 STEP 5: CREATE success.html
<!DOCTYPE html>
<html>
<head>
<title>Success</title>
<style>
body { text-align:center; font-family:Arial; }

.success {
    margin-top:100px;
    color:green;
}
</style>
</head>
<body>

<div class="success">
<h1>✅ Payment Successful</h1>
<p>Your booking is confirmed 🎉</p>

<a href="/">Go Home</a>
</div>

</body>
</html>
📱 STEP 6: ADD UPI QR SCANNER (DEMO)

Update payment.html (add below form):

<h3>Scan UPI QR</h3>
<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=demo@upi&pn=AakashTravels&am=500" />

👉 This shows QR code for demo payment (Viva perfect 💯)
