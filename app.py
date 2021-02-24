import sqlite3 as sql
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Open Database and creates tables registration and products
@app.route('/')
def init_sqlite_db():
    with sql.connect("database.db") as conn:
        conn.cursor()
        conn.execute(
            'CREATE TABLE IF NOT EXISTS registration (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, email TEXT, address TEXT, suburb TEXT,  city TEXT, zipcode TEXT, password TEXT)')
        conn.execute(
            'CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price TEXT, Quantity TEXT, image BLOB, description TEXT,)')
        conn.commit()

def products():
    with sql.connect("database.db") as conn:
        conn.cursor()
       
        conn.execute(
            'INSERT INTO Products(name, price, Quantity, image, description) VALUES (Nike Air Presto, 850.00, 10, image, Takkies)')
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)'
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)'
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)'
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)'
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)'
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)'
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)'
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)'
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)'
            # 'INSERT INTO Products(Nike, 350.00, 10, image, Takkies)')
        conn.commit()
        # init_sqlite_db()

    return render_template('index.html')

#Opens Registration Form
@app.route('/registration/', methods=['GET'])
def enter_new_user():
    return render_template('registration.html')


#Adding User to Registration database according to user inputs
@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            address = request.form['address']
            suburb = request.form['suburb']
            city = request.form['city']
            zipcode = request.form['zipcode']
            password = request.form['password']

            with sql.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO registration (name, surname, email, address, suburb, city, zipcode, pin_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, surname, email, address, suburb, city, zipcode, password))
                con.commit()
                msg = name + " was successfully added to the database."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + e
        finally:
            return jsonify(msg=msg)

#Displays records saved in Database
@app.route('/show-records/', methods=["GET"])
def show_records():
    con = sql.connect("database.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select * from registration")
    rows = cur.fetchall()
    con.execute("select * from Products")
    products = cur.fetchall()
    return jsonify(rows, products)

#Deletes user from Database
@app.route('/delete-user/<int:registration_id>/', methods=["GET"])
def delete_user(registration_id):
    msg = None
    try:
        with sql.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM registration WHERE id=" + str(registration_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return render_template('deleted.html', msg=msg)


if __name__ == "__main__":
    app.run(debug="true")
