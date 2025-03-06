from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Secret Key for session security
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'  # Ensure this is correct
app.config['MYSQL_DB'] = 'mooresfarmmarket'

# Initialize MySQL
mysql = MySQL(app)


# Test Database Connection
@app.route('/test_db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        cur.close()
        return str(tables)
    except Exception as e:
        return str(e)


# Home Route
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['email'], email=session['email'])
    return redirect(url_for('login'))


# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        username = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Customer WHERE email = %s AND password = %s', (username, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['Customerid'] = account['Customerid']
            session['FirstName'] = account['FirstName']
            session['email'] = account['email']

            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'FirstName' in request.form and 'LastName' in request.form and 'Password' in request.form and 'email' in request.form:
        firstname = request.form['FirstName']
        lastname=request.form['LastName']
        password = request.form['Password']
        email = request.form['Email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM CUSTOMERS WHERE Email = %s', (email,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not firstname or not lastname or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO CUSTOMERS (FirstName, LastName, Email, Password) VALUES (%s, %s, %s, %s)', 
                           (firstname, lastname, email, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
