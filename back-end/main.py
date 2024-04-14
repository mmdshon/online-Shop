from flask import Flask, jsonify , request
import sqlite3
from flask_cors import CORS, cross_origin
import io
from datetime import datetime
from fileinput import filename 
from hashlib import md5
import random

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect("./data-shop.db")
    conn.row_factory = sqlite3.Row
    return conn

# back test
@app.route('/',methods=['GET'])
def test():
    return "ok"

#-----------------user---------------------------

# users crud function
def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users')
    Users = cur.fetchall()
    final_Users = []
    for User in Users:
        final_Users.append({
            "id": User[0],
            "Name": User[1],
            "Password": User[2],
            "Email": User[3],
            "Phone": User[4],
            "registration_date": User[5],
            "Role": User[6],
            "address": User[7],
        })
    conn.close()
    return final_Users
def get_users(users_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users WHERE user_id = ?', (users_id,))
    User = cur.fetchone()
    final_users = {
            "id": User[0],
            "Name": User[1],
            "Password": User[2],
            "Email": User[3],
            "Phone": User[4],
            "registration_date": User[5],
            "Role": User[6],
            "address": User[7],
        }
    conn.close()
    return final_users
def create_user(Name, Password, Email, Phone, Role,address ):
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash = md5(Password.encode()).hexdigest()
    registration_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO Users (username, password_hash,email,phone_number,registration_date,role,default_shipping_address) VALUES (?, ?, ?, ? , ?, ?, ?)', (Name, password_hash, Email, Phone, registration_date, Role,address ))
    conn.commit()
    customer_id = cur.lastrowid
    conn.close()
    return customer_id
def update_user(id,Name, Password, Email, Phone, registration_date, Role,address):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Users SET username = ?, password_hash = ?, email = ?, phone_number = ?, registration_date = ?, role = ? , default_shipping_address = ? WHERE user_id = ?', (Name, Password, Email, Phone, registration_date, Role,address,id))
    conn.commit()
    conn.close()
    return get_users(id)
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
def login_user(user_name,Password):
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash = md5(Password.encode()).hexdigest()
    cur.execute('SELECT * FROM Users WHERE username = ? and password_hash = ?', (user_name,password_hash,))
    user_data = cur.fetchone()
    if user_data:
        return "ok"
    else : 
        return "mousavi"

# users CRUD routes
@app.route('/Users', methods=['GET'])
def list_users():
    range = request.args.get('range')
    users = get_all_users()
    response = jsonify(users)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(users)
    return response
@app.route('/Users/<int:user_id>', methods=['GET'])
def get_customer_by_id(user_id):
    user = get_users(user_id)
    if user is None:
        return '', 404
    return jsonify(user), 200
@app.route('/Users', methods=['POST'])
def add_customer():
    name = request.json['Name']
    Password = request.json['Password']
    Email = request.json['Email']
    Phone = request.json['Phone']
    Role = request.json['Role']
    address = request.json['address']
    user_id = create_user(name, Password, Email, Phone, Role,address)
    if user_id:
        return jsonify(get_users(user_id)), 201
    else:
        return jsonify("NO")
@app.route('/Users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    name = request.json['Name']
    Password = request.json['Password']
    Email = request.json['Email']
    Phone = request.json['Phone']
    registration_date = request.json['registration_date']
    Role = request.json['Role']
    address = request.json['address']
    updated = update_user(user_id,name, Password, Email, Phone, registration_date, Role,address)
    return jsonify(updated), 200
@app.route('/Users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    delete_user(user_id)
    return jsonify({"id":user_id}), 200

@app.route('/Users/login', methods=['POST'])
def login_users():
    user_name = request.json['user_name']
    password = request.json['password']
    response = login_user(user_name, password)
    return jsonify(response)

#-----------------user---------------------------
#----------------category--------------------------

#category crud function
def get_all_Categories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Categories')
    Categories = cur.fetchall()
    final_Categories = []
    for Categorie in Categories:
        final_Categories.append({
            "id": Categorie[0],
            "name": Categorie[1],
            "description": Categorie[2],
            "parent_category_id": Categorie[3],
            "created_at": Categorie[4],
        })
    conn.close()
    return final_Categories
def create_Categories(name, description, parent_category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    created_at = datetime.today().strftime('%Y-%m-%d')
    cur.execute('INSERT INTO Categories (name, description,parent_category_id,created_at) VALUES (?, ?, ?, ?)', (name, description, parent_category_id, created_at))
    conn.commit()
    Category_id = cur.lastrowid
    conn.close()
    return get_Categories(Category_id)
def get_Categories(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Categories WHERE category_id = ?',(id,))
    Categorie = cur.fetchone()
    conn.close()
    final_category = {
        "id": Categorie[0],
        "name": Categorie[1],
        "description": Categorie[2],
        "parent_category_id": Categorie[3],
        "created_at": Categorie[4],
    }
    return final_category
def delete_category(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Categories WHERE category_id = ?', (id,))
    conn.commit()
    conn.close()
def update_category(name,description,parent_category_id,created_at,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Categories SET name = ?, description = ?, parent_category_id = ?, created_at = ? WHERE category_id = ?', (name,description,parent_category_id,created_at,id))
    conn.commit()
    conn.close()
    return get_Categories(id)

# category crud routes
@app.route('/Categories', methods=['GET'])
def list_Categories():
    Categories = get_all_Categories()
    response = jsonify(Categories)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(Categories)
    return response

# @app.route('/parent_categories', methods=['GET'])
# def parent_categories():
#     return "arr"

@app.route('/Categories/<int:id>', methods=['GET'])
def Category(id):
    Category = get_Categories(id)
    if Category is None:
        return '', 404
    return jsonify(Category), 200
@app.route('/Categories', methods=['POST'])
def add_Categories():
    name = request.json['name']
    description = request.json['description']
    parent_category_id = request.json['parent_category_id']
    Categories_id = create_Categories(name, description, parent_category_id)
    return Categories_id , 201
@app.route('/Categories/<int:id>', methods=['DELETE'])
def delete_category_by_id(id):
    delete_category(id)
    return jsonify({"id":id}), 200
@app.route('/Category/<int:id>', methods=['PUT'])
def update_category_by_id(id):
    name = request.json['name']
    description = request.json['description']
    parent_category_id = request.json['parent_category_id']
    created_at = request.json['created_at']
    updated = update_category(name, description, parent_category_id, created_at,id)
    return jsonify(updated), 200

#----------------category--------------------------




if __name__ == '__main__':
    app.run(debug=True)