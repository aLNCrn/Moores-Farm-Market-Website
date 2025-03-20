from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors
import re

app = Flask(__name__, template_folder='templates')  # Explicitly set templates folder

# Secret Key for session security
app.secret_key = 'mfmpass'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # The MySQL password for the person doing the demonstration
app.config['MYSQL_DB'] = 'mooresfarmmarket'

# Initialize MySQL
mysql = MySQL(app)

# Test Database Connection
@app.route('/test_db')
def test_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        return str(tables)
    except Exception as e:
        return str(e)

# Home Route
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', firstname=session['firstname'], email=session['email'])
    return redirect(url_for('login'))

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM CUSTOMERS WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['FirstName'] = account['FirstName']
            session['email'] = account['email']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)  # Ensured correct template is used

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'password' in request.form and 'email' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM CUSTOMERS WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', firstname):
            msg = 'First name must contain only characters!'
        elif not re.match(r'[A-Za-z]+', lastname):
            msg = 'Last name must contain only characters!'
        elif not firstname or not lastname or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO CUSTOMERS (firstname,lastname, emaail, password) VALUES (%s, %s, %s, %s)', 
                           (firstname, lastname, email, password,))
            mysql.connection.commit()
            mysql.connection.commit()
            cursor.close()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

  

    return render_template('register.html', msg=msg)

@app.route('/')
def index():
    # Fetch all products from the products table (select all columns)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()  # Fetch all products as a list of tuples
    # Fetch all product types to display in the dropdown (for the form)
    cursor.execute("SELECT * FROM product_types")
    product_types = cursor.fetchall()  # Fetch product types as a list of tuples
    print(products)
    return render_template('index.html', products=products, product_types=product_types)

@app.route('/add_product', methods=['POST'])
def add_product():
    cursor = mysql.connection.cursor()
    name = request.form['name']
    price = float(request.form['price'])
    currently_available = request.form.get('currently_available') == 'on'  
    cursor.execute("INSERT INTO products (name, price, currently_available) VALUES (%s, %s, %s)",
                   (name, price, currently_available))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
