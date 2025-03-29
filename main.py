from flask import Flask, render_template, request, redirect, url_for, session, g
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

@app.before_request
def load_logged_in_user():
    g.firstname = session.get('FirstName', None)
    g.id = session.get('CustomerID', None)
    g.isOwner = session.get('isOwner', False)
    g.isEmp = session.get('isEmp', False)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/register1')
def register1():
    return render_template('register.html')


@app.route('/seasonal')
def seasonal():

    return render_template('seasonal.html')

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


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        if request.form.get('employee_button') == 'on':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM EMPLOYEES WHERE email = %s AND password = %s', (email, password))
            account = cursor.fetchone()

            if account:
                session['loggedin'] = True
                session['FirstName'] = account.get('FirstName') 
                if account.get('position') == 'admin':
                    session['isOwner'] = True
                else:
                    session['isEmp'] = True
                session['email'] = account.get('email')
                return redirect(url_for('index'))
            else:
                msg = 'Incorrect username/password or you are not an employee!'
                return render_template('login.html', msg=msg)  
            

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM CUSTOMERS WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['FirstName'] = account.get('FirstName') 
            session['CustomerID'] = account.get('CustomerID') 
            session['email'] = account.get('email')
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)  






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
            cursor.execute('INSERT INTO CUSTOMERS (firstname,lastname, email, password) VALUES (%s, %s, %s, %s)', 
                           (firstname, lastname, email, password,))
            mysql.connection.commit()
            cursor.close()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

  

    return render_template('register.html', msg=msg)

@app.route('/getproducts')
def get_products():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    customer_id = session.get('CustomerID')
    if customer_id:  
        cursor.execute("""
            SELECT p.*, 
                   CASE WHEN f.CustomerID IS NOT NULL THEN 1 ELSE 0 END as is_favorited
            FROM PRODUCTS p
            LEFT JOIN FAVORITES f 
            ON p.ProductID = f.ProductID AND f.CustomerID = %s
        """, (customer_id,))
    else:  
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()  # Fetch all products without is_favorited
        return render_template('products.html', products=products)

    products = cursor.fetchall()  
    cursor.close()
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    cursor = mysql.connection.cursor()
    name = request.form['name']
    price = request.form['price']
    if request.form.get('currently_available') == 'on':
        currently_available = 1
    else:
        currently_available = 0


    cursor.execute("INSERT INTO products (name, price, CurrentlyAvailable, ImageLink) VALUES (%s, %s, %s, %s)",
                   (name, price, currently_available, None))

    mysql.connection.commit()
    return redirect(url_for('products'))

    #if request.form.get[product_type_id] == 1:
    #   product_type= 'Flowers'

    #elif request.form.get[product_type_id] == 2:
    #  product_type= 'Honey'

    #elif request.form.get[product_type_id] == 3:
    #   product_type= 'Produce'

    #elif request.form.get[product_type_id] == 4:
    #   product_type= 'Seasonal'

    #elif request.form.get[product_type_id] == 5:
    #   product_type= 'Vegetable Plants'

app.route('/addProduct_2', methods =['POST'])
def add_product_2():
     selectedOption = request.form.get['product_type_id'];

@app.route('/favorite', methods=['POST'])
def favorite_product():
    cursor_favorites = mysql.connection.cursor()  # Creating a cursor for interacting with the database
    customer_id = session.get('CustomerID')  # Ensure CustomerID is set in the session
    
    product_id = request.form.get('product_id')  # Get the product_id from the form data
    
    if customer_id and product_id:
        # Check if the product is already in favorites
        cursor_favorites.execute("SELECT * FROM FAVORITES WHERE CustomerID = %s AND ProductID = %s", (customer_id, product_id))
        favorite = cursor_favorites.fetchone()  # If the product is already in favorites, it will return a row
        
        if favorite:
            # If it's favorited, unfavorite the product (remove from FAVORITES table)
            cursor_favorites.execute("DELETE FROM FAVORITES WHERE CustomerID = %s AND ProductID = %s", (customer_id, product_id))
        else:
            # If it's not favorited, favorite the product (add to FAVORITES table)
            cursor_favorites.execute("INSERT INTO FAVORITES (CustomerID, ProductID) VALUES (%s, %s)", (customer_id, product_id))
        
        mysql.connection.commit()  # Commit the transaction to the database
    
    cursor_favorites.close()  # Close the cursor to free up the database resource
    
    return redirect(url_for('get_products'))  


if __name__ == '__main__':
    app.run(debug=True)
