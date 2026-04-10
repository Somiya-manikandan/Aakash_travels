🌍 3. templates/index.html
<!DOCTYPE html>
<html>
<head>
<title>Aakash Travels</title>
<style>
body { font-family:Arial; background:#f4f6f8; text-align:center; }
h1 { background:#007bff; color:white; padding:15px; }

.card {
    background:white;
    width:300px;
    margin:20px auto;
    padding:15px;
    border-radius:10px;
}

.btn {
    background:#ff5722;
    color:white;
    padding:8px;
    text-decoration:none;
    border-radius:5px;
}
</style>
</head>
<body>

<h1>Aakash Travels</h1>

<a href="/login">Login</a> |
<a href="/register">Register</a> |
<a href="/logout">Logout</a>

<h2>Packages</h2>

{% for p in packages %}
<div class="card">
    <h3>{{ p[1] }}</h3>
    <p>₹{{ p[2] }}</p>
    <a class="btn" href="/payment/{{ p[0] }}">Book Now</a>
</div>
{% endfor %}

</body>
</html>
💳 4. templates/payment.html
<!DOCTYPE html>
<html>
<head>
<title>Payment</title>
</head>
<body>

<h2>Payment</h2>

<form method="post">
    <input type="radio" name="method" value="UPI" required> UPI<br>
    <input type="radio" name="method" value="Card"> Card<br>
    <input type="radio" name="method" value="Cash"> Cash<br><br>

    <button>Pay Now</button>
</form>

</body>
</html>
🔐 5. login.html
<h2>Login</h2>
<form method="post">
<input type="email" name="email" placeholder="Email"><br>
<input type="password" name="password" placeholder="Password"><br>
<button>Login</button>
</form>
📝 6. register.html
<h2>Register</h2>
<form method="post">
<input type="text" name="name" placeholder="Name"><br>
<input type="email" name="email"><br>
<input type="password" name="password"><br>
<button>Register</button>
</form>
👨‍💼 7. admin.html
<h2>Admin</h2>

<form method="post" action="/add_package">
<input name="place" placeholder="Place">
<input name="price" placeholder="Price">
<button>Add</button>
</form>

<h3>Packages</h3>
{% for p in packages %}
{{ p[1] }} - {{ p[2] }}
<a href="/delete/{{ p[0] }}">Delete</a><br>
{% endfor %}

<h3>Bookings</h3>
{% for b in bookings %}
{{ b[1] }} booked {{ b[2] }} ({{ b[3] }})<br>
{% endfor %}
✏️ 8. edit_package.html
<h2>Edit</h2>

<form method="post" action="/update/{{ package[0] }}">
<input name="place" value="{{ package[1] }}">
<input name="price" value="{{ package[2] }}">
<button>Update</button>
</form>
📦 9. requirements.txt
flask
gunicorn
🚀 10. Procfile
web: gunicorn app:app
