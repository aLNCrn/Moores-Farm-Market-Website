from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import mysql.connector
import MySQLdb.cursors
import re
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename



app = Flask(__name__, template_folder='templates')  # Explicitly set templates folder

# Secret Key for session security
app.secret_key = 'mfmpass'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # The MySQL password for the person doing the demonstration
app.config['MYSQL_DB'] = 'mooresfarmmarket'

#Email configuration 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'mooresfarmm@gmail.com'  
app.config['MAIL_PASSWORD'] = 'vqsi corv gwow mbbs'  
app.config['MAIL_DEFAULT_SENDER'] = 'mooresfarmm@gmail.com'  

mail = Mail(app)


# Initialize MySQL
mysql = MySQL(app)

UPLOAD_FOLDER = os.path.join('static', 'product_images')
app.config['UPLOAD_FOLDER'] = 'static/product_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
TEXT_BUBBLE_FILE_PATH = os.path.join(app.root_path, 'static', 'textBubbles.txt')

def getTextBubbles():
    textBubbles = {}
    fileReader = open(TEXT_BUBBLE_FILE_PATH, "r")
    for line in fileReader:
        lineArray = line.strip("\n").split("|*|")
        if len(lineArray) == 2:
            textBubbles[lineArray[0]] =  lineArray[1]
        else:
            print(f"There was an error loading line '{line}' from {TEXT_BUBBLE_FILE_PATH}: "
                  f"Expected Size 2 Received {len(lineArray)}")
    fileReader.close()
    return textBubbles

def editTextBubble(header: str, body: str):
    textBubbles = {}
    fileReader = open(TEXT_BUBBLE_FILE_PATH, "r")
    for line in fileReader:
        lineArray = line.strip("\n").split("|*|")
        if len(lineArray) == 2:
            if not lineArray[0] == header:
                textBubbles[lineArray[0]] = lineArray[1]
            #print(textBubbles)
        else:
            print(f"There was an error loading line '{line}' from {TEXT_BUBBLE_FILE_PATH}: "
                  f"Expected Size 2 Received {len(lineArray)}")
    fileReader.close()
    textBubbles[header] = body
    fileWriter = open(TEXT_BUBBLE_FILE_PATH, "w")
    fileWriter.writelines(f"{key}|*|{textBubbles[key]}\n" for key in textBubbles)
    fileWriter.close()

@app.before_request
def load_logged_in_user():
    g.firstname = session.get('FirstName', None)
    g.id = session.get('CustomerID', None)
    g.isOwner = session.get('isOwner', False)
    g.isEmp = session.get('isEmp', False)

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', textBubbles=getTextBubbles())


@app.route('/edit_text', methods=['POST'])
def edit_text():
    if not session.get('isOwner'):
        return "Unauthorized", 403

    text_id = request.form.get('text_id')
    text_body = request.form.get('textBody')
    redirect_to = request.form.get('redirect_to') or '/'

    if text_id and text_body:
        editTextBubble(text_id, text_body)  # <- Your custom function
    else:
        print("Missing input!")

    return redirect(redirect_to)

@app.route('/index', methods=['GET', 'POST'])
def index():
    
    #if the user is logged in and not made a review today, allow them to make a review
    reviewMade = False
    if 'loggedin' in session and session['loggedin'] and 'CustomerID' in session:
        today = datetime.today().strftime('%Y-%m-%d')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT ReviewDate, CustomerID  FROM reviews')
        dateCheckReviews = cursor.fetchall() 
        for review in dateCheckReviews:
            review_date = review['ReviewDate'].strftime('%Y-%m-%d')  # Extract the date part
            if review['CustomerID'] == session['CustomerID'] and review_date == today:
                # If the user has already submitted a review today
                reviewMade = True
                break

        if not reviewMade:     
            if request.method == 'POST':
                rating = request.form['rating']
                reviewText = request.form['review']
                customerID = session['CustomerID']
                writeCursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                writeCursor.execute("INSERT INTO reviews (Rating, ReviewText, CustomerID) VALUES (%s, %s, %s)",
                            (rating, reviewText, customerID))
                mysql.connection.commit()
                session['reviewMade'] = True    
                return redirect(url_for('index'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT Rating, ReviewDate, ReviewText, ReviewID, CustomerID  FROM reviews')
    reviews = cursor.fetchall() 
    reviews = reviews[::-1]
    #print(reviews)
    # Render the review form if the user is logged in
    return render_template('index.html', reviews=reviews, reviewMade=reviewMade, textBubbles=getTextBubbles())

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/getproducts',methods=['GET', 'POST'])
def get_products():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    selected_table = request.form.get('table_name', 'PRODUCTS')
    customer_id = session.get('CustomerID')
    if selected_table == 'IN_STOCK':
        if customer_id:
            cursor.execute("""
                    SELECT p.*, 
                           CASE WHEN f.CustomerID IS NOT NULL THEN 1 ELSE 0 END as is_favorited
                    FROM PRODUCTS p
                    LEFT JOIN FAVORITES f ON p.ProductID = f.ProductID AND f.CustomerID = %s
                    WHERE p.CurrentlyAvailable = 1
                """, (customer_id,))
        else:
            cursor.execute("""
                    SELECT * FROM PRODUCTS
                    WHERE CurrentlyAvailable = 1
                """)
        products = cursor.fetchall()
        cursor.close()
        return render_template('products.html', products=products, selected_table=selected_table)
    if selected_table == 'PRODUCTS':
        if customer_id:
            cursor.execute("""
                   SELECT p.*, 
                          CASE WHEN f.CustomerID IS NOT NULL THEN 1 ELSE 0 END as is_favorited
                   FROM PRODUCTS p
                   LEFT JOIN FAVORITES f 
                   ON p.ProductID = f.ProductID AND f.CustomerID = %s
               """, (customer_id,))
        else:
            cursor.execute("SELECT * FROM PRODUCTS")
    else:
        if customer_id:
            cursor.execute(f"""
                   SELECT p.ProductID, prod.Name, prod.Price, prod.CurrentlyAvailable, prod.Imagelink,
                          p.*, 
                          CASE WHEN f.CustomerID IS NOT NULL THEN 1 ELSE 0 END as is_favorited
                   FROM {selected_table} p
                   JOIN PRODUCTS prod ON p.ProductID = prod.ProductID
                   LEFT JOIN FAVORITES f 
                   ON p.ProductID = f.ProductID AND f.CustomerID = %s
               """, (customer_id,))
        else:
            cursor.execute(f"""
                   SELECT p.ProductID, prod.Name, prod.Price, prod.CurrentlyAvailable, prod.Imagelink, p.*
                   FROM {selected_table} p
                   JOIN PRODUCTS prod ON p.ProductID = prod.ProductID
               """)
        if selected_table == 'FAVORITES':
            if not customer_id:
                Flask("You need to be logged in to see favorites.")
                return redirect(url_for('login'))  # or show an empty list
            else:
                # This fetches all favorited products from all sub-tables
                cursor.execute("""
                        SELECT prod.ProductID, prod.Name, prod.Price, prod.CurrentlyAvailable,prod.Imagelink, 1 as is_favorited
                        FROM FAVORITES f
                        JOIN PRODUCTS prod ON f.ProductID = prod.ProductID
                        WHERE f.CustomerID = %s
                    """, (customer_id,))
                products = cursor.fetchall()
                cursor.close()
                return render_template('products.html', products=products, selected_table=selected_table)

    products = cursor.fetchall()
    cursor.close()
    return render_template('products.html', products=products, selected_table=selected_table)

@app.route('/add_product', methods=['POST'])
def add_product():
    cursor = mysql.connection.cursor()
    name = request.form['name']
    price = request.form['price']
    if request.form.get('currently_available') == 'on':
        currently_available = 1
    else:
        currently_available = 0
    image_path = request.form['image']


    product_type_id = request.form['product_type_id']
    cursor.execute("INSERT INTO products (name, price, CurrentlyAvailable, ImageLink) VALUES (%s, %s, %s, %s)",
                   (name, price, currently_available, image_path))

    mysql.connection.commit()

    cursor.execute("SELECT LAST_INSERT_ID()")
    product_id = cursor.fetchone()[0]

    if product_type_id == 'Flowers':
        annual = request.form.get('annual')
        sun_or_shade = request.form.get('sun_or_shade')
        cursor.execute(
            "INSERT INTO FLOWERS (ProductID, Annual, SunOrShade) VALUES (%s, %s, %s)",
            (product_id, annual, sun_or_shade)
        )

    elif product_type_id == 'Produce':
        storage_instructions = request.form.get('storage_instructions')
        produce_type = request.form.get('Fruit/Vegetable')
        location = request.form.get('location')
        cursor.execute(
            "INSERT INTO PRODUCE (ProductID, StorageInstructions, Type, Location) VALUES (%s, %s, %s, %s)",
            (product_id, storage_instructions, produce_type, location)
        )

    elif product_type_id == 'Honey':
        source = request.form.get('source')
        raw = 'raw' in request.form
        cursor.execute(
            "INSERT INTO HONEY (ProductID, Source, Raw) VALUES (%s, %s, %s)",
            (product_id, source, raw)
        )

    elif product_type_id == 'Seasonal':
        season = request.form.get('season')
        cursor.execute(
            "INSERT INTO Seasonal (ProductID, Season) VALUES (%s, %s)",
            (product_id, season)
        )

    elif product_type_id == 'Vegetable Plants':
        season = request.form.get('season')
        plant_type = request.form.get('plant_type')
        cursor.execute(
            "INSERT INTO VegetablePlant (ProductID, Season, PlantType) VALUES (%s, %s, %s)",
            (product_id, season, plant_type)
        )

    mysql.connection.commit()
    cursor.close()


    return redirect(url_for('products'))




@app.route('/favorite', methods=['POST'])
def favorite_product():
    cursor_favorites = mysql.connection.cursor()  
    customer_id = session.get('CustomerID')  
    product_id = request.form.get('product_id')  
    if customer_id and product_id:
        cursor_favorites.execute("SELECT * FROM FAVORITES WHERE CustomerID = %s AND ProductID = %s", (customer_id, product_id))
        favorite = cursor_favorites.fetchone()  
        if favorite:
            cursor_favorites.execute("DELETE FROM FAVORITES WHERE CustomerID = %s AND ProductID = %s", (customer_id, product_id))
        else:
            cursor_favorites.execute("INSERT INTO FAVORITES (CustomerID, ProductID) VALUES (%s, %s)", (customer_id, product_id))
        mysql.connection.commit()  
    cursor_favorites.close() 
    return redirect(url_for('get_products'))


@app.route('/delete_product', methods=['POST'])
def delete_product():
    product_id = request.form['id']  # Getting the product ID from the form data
    if product_id:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM FLOWERS WHERE ProductID = %s", (product_id,))
        cursor.execute("DELETE FROM PRODUCE WHERE ProductID = %s", (product_id,))
        cursor.execute("DELETE FROM HONEY WHERE ProductID = %s", (product_id,))
        cursor.execute("DELETE FROM Seasonal WHERE ProductID = %s", (product_id,))
        cursor.execute("DELETE FROM VegetablePlant WHERE ProductID = %s", (product_id,))
        cursor.execute("DELETE FROM PRODUCTS WHERE ProductID = %s", (product_id,))

        mysql.connection.commit()
        cursor.close()

    return redirect(url_for('get_products'))

@app.route('/delete_review', methods=['POST'])
def delete_review():
    review_id = request.form['reviewid']  # Getting the product ID from the form data
    print("Review ID received:", review_id)
    if review_id:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM REVIEWS WHERE ReviewID = %s", (review_id,))

        mysql.connection.commit()
        cursor.close()

    return redirect(url_for('index'))


@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT EmployeeID, FirstName, LastName, Email, Position, Phone, Wage, HireDate FROM employees")
    employees = cursor.fetchall()

    today = datetime.today()
    current_year = today.year
    current_month = today.month
    days_in_advance = [(today + timedelta(days=i)).day for i in range(0, 14)]

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        year = request.form['year']
        month = request.form['month']

        for day in days_in_advance:
            time_in = request.form.get(f'timein-{day}')
            time_out = request.form.get(f'timeout-{day}')

            if time_in and time_out:
                cursor.execute("""
                    INSERT INTO employeeschedule (EmployeeID, Year, Month, Day, TimeIn, TimeOut)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (employee_id, year, month, day, time_in, time_out))

        mysql.connection.commit()
        return redirect('/add_schedule')

    # Always fetch all schedules if no filter is applied
    employee_id = request.args.get('employee_id')
    year = request.args.get('year')
    month = request.args.get('month')

    if employee_id and year and month:
        cursor.execute("""
            SELECT EmployeeID, Year, Month, Day, TimeIn, TimeOut, Shiftid FROM employeeschedule 
            WHERE EmployeeID = %s AND Year = %s AND Month = %s
        """, (employee_id, year, month))
    elif employee_id:
        cursor.execute("""
            SELECT EmployeeID, Year, Month, Day, TimeIn, TimeOut, Shiftid FROM employeeschedule 
            WHERE EmployeeID = %s
        """, (employee_id,))
    else:
        # Fetch ALL if no filter is provided
        cursor.execute("SELECT EmployeeID, Year, Month, Day, TimeIn, TimeOut, Shiftid FROM employeeschedule")

    schedules = cursor.fetchall()
    cursor.close()

    return render_template('add_schedule.html',
                           employees=employees,
                           current_year=current_year,
                           current_month=current_month,
                           days_in_advance=days_in_advance,
                           schedules=schedules)

    
@app.route('/add_employee', methods=['POST'])
def add_employee():
    if not session.get('isOwner'):
        return "Unauthorized", 403

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    phone = int(request.form['phone']) if request.form['phone'].isdigit() else None
    wage = int(request.form['wage']) if request.form['wage'].isdigit() else None
    hiredate_raw = request.form['hiredate']

    try:
        hiredate = datetime.strptime(hiredate_raw, "%Y-%m-%d").date()
    except ValueError:
        hiredate = None

    position = request.form['position']

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO employees (FirstName, LastName, Email, Password, Phone, Wage, HireDate, Position)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (firstname, lastname, email, password, phone, wage, hiredate, position))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('add_schedule'))




@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    if not session.get('isOwner'):
        return "Unauthorized", 403

    employee_id = request.form['employee_id']

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM employeeschedule WHERE EmployeeID = %s", (employee_id,))
    cursor.execute("DELETE FROM employees WHERE EmployeeID = %s", (employee_id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('add_schedule'))




@app.route('/eschedule', methods=['GET'])
def eschedule():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employeeschedule")
    schedule = cursor.fetchall()
    cursor.close()
    return render_template('eschedule.html', schedule=schedule)


@app.route('/edit_product1', methods=['POST'])
def edit_product1():
    cursor = mysql.connection.cursor()
    product_id = request.form['ProductID']
    name = request.form['name']
    price = request.form['price']

    if request.form.get('currently_available') == 'on':
        currently_available = 1
    else:
        currently_available = 0

    image_path = request.form['image']

    product_type_id = request.form['product_type_id']

    cursor.execute("UPDATE products SET name = %s, price = %s, CurrentlyAvailable = %s, ImageLink = %s WHERE ProductID = %s",
                   ( name, price, currently_available, image_path, product_id))

    mysql.connection.commit()

    if product_type_id == 'Flowers':
        annual = request.form.get('annual')
        sun_or_shade = request.form.get('sun_or_shade')
        cursor.execute(
            "UPDATE FLOWERS SET Annual = %s, SunOrShade = %s WHERE ProductID = %s",
            (annual, sun_or_shade, product_id,)
        )

    elif product_type_id == 'Produce':
        storage_instructions = request.form.get('storage_instructions')
        produce_type = request.form.get('produce_type')
        location = request.form.get('location')
        cursor.execute(
            "UPDATE PRODUCE SET StorageInstructions = %s, Type = %s, Location = %s WHERE ProductID = %s",
            ( storage_instructions, produce_type, location, product_id,)
        )

    elif product_type_id == 'Honey':
        source = request.form.get('source')
        raw = 'raw' in request.form
        cursor.execute(
            "UPDATE HONEY SET Source = %s, Raw= %s WHERE ProductID = %s",
            (source, raw, product_id,)
        )

    elif product_type_id == 'Seasonal':
        season = request.form.get('season')
        cursor.execute(
            "UPDATE Seasonal SET Season = %s WHERE ProductID = %s",
            ( season, product_id,)
        )

    elif product_type_id == 'Vegetable Plants':
        season = request.form.get('season')
        plant_type = request.form.get('plant_type')
        cursor.execute(
            "UPDATE VegetablePlant SET Season = %s, PlantType= %s WHERE ProductID = %s",
            (season, plant_type, product_id,)
        )

    mysql.connection.commit()
    cursor.close()


    return redirect(url_for('products'))


    
@app.route('/delete_shift', methods=['POST'])
def delete_shift():
    shiftId = request.form['shiftId']  # Getting the product ID from the form data
    print("Review ID received:", shiftId)
    if shiftId:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM employeeschedule WHERE shiftId = %s", (shiftId,))

        mysql.connection.commit()
        cursor.close()

    return redirect(url_for('add_schedule'))

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.form['email']
        subject = 'Your Subject'
        body = 'This is the body of the automated email.'
        
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        
        try:
            mail.send(msg)
            return 'Email sent successfully!'
        except Exception as e:
            return str(e)

    return render_template('send_email.html')

@app.route('/email', methods=['GET', 'POST'])
def email():
    print("Email route loaded!")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    

    cursor.execute('SELECT Email FROM customers')
    customers = cursor.fetchall()
    
 
    cursor.execute('SELECT Email FROM employees')
    employees = cursor.fetchall()
    if request.method == 'POST':
        subject = request.form['subject']
        body = request.form['body']
        selected_recipients = request.form.getlist('recipients')

        if not selected_recipients:
            flash("⚠️ No recipients selected.")
            return redirect(url_for('email'))

        for email in selected_recipients:
            msg = Message(subject, recipients=[email])
            msg.body = body
            try:
                mail.send(msg)
            except Exception as e:
                flash(f"❌ Error sending to {email}: {e}")
                return redirect(url_for('email'))

        flash("✅ Emails sent successfully!")
        return redirect(url_for('email'))



    cursor.close()
    return render_template('email.html', customers=customers, employees=employees)
    









if __name__ == '__main__':
    app.run(debug=True)


