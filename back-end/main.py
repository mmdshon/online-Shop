from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Get a customer by ID
def get_customer(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users WHERE id = ?', (user_id))
    customer = cur.fetchone()
    final_customer = {
            "user_id": customer[0],
            "username": customer[1],
            "password_hash": customer[2],
            "email": customer[3],
            "phone_number": customer[4],
            "registration_date": customer[5],
            "role": customer[6],
            "default_shipping_address": customer[7],
        }
    conn.close()
    return final_customer

# Create a new customer
def create_customer(user_id,username,password_hash,email,phone_number,registration_date,role):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO Users (user_id, username, password_hash,email, phone_number, registration_date,role) VALUES (?, ?, ?,?, ?, ?,?)', (user_id, username, password_hash,email,phone_number,registration_date,role))
    conn.commit()
    customer_id = cur.lastrowid
    conn.close()
    return customer_id

# Create 10 customers
# for i in range(1, 11):
#     name = f'Customer {i}'
#     email = f'customer{i}@example.com'
#     phone = f'555-123-456{i}'
#     create_customer(name, email, phone)

# Update a customer
def update_customer(user_id,username,password_hash,email,phone_number,registration_date,role):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Users SET username = ?, password_hash = ?, email = ?,phone_number = ?, registration_date = ?, role = ? WHERE user_id = ?', (user_id,username,password_hash,email,phone_number,registration_date,role))
    conn.commit()
    conn.close()
    return get_customer(user_id)

# Delete a customer
def delete_customer(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Users WHERE user_id = ?', (user_id))
    conn.commit()
    conn.close()

# Get all customers
def get_all_customers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users')
    customers = cur.fetchall()
    final_customers = []
    for customer in customers:
        final_customers.append({
            "product_id": customer[0],
            "name": customer[1],
            "description": customer[2],
            "price": customer[3],
            "category_id": customer[4],
            "image": customer[5]
        })
    conn.close()
    return final_customers

#test backend
@app.route('/', methods=['GET'])
def test():
    return "ok"

# CRUD routes
@app.route('/customer', methods=['GET'])
def list_customer():
    customers = get_all_customers()
    response = jsonify(customers)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(customers)
    return response

@app.route('/customer', methods=['POST'])
def add_customer():
    username = request.json['username']
    password_hash = request.json['email']
    email = request.json['email']
    phone_number = request.json['emphone_numberail']
    registration_date = request.json['registration_date']
    role = request.json['role']
    customer_id = create_customer(username, password_hash, email,phone_number,registration_date,role)
    return jsonify(get_customer(customer_id)), 201

@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer_by_id(user_id):
    customer = get_customer(user_id)
    if customer is None:
        return '', 404
    return jsonify(customer), 200

@app.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer_by_id(user_id):
    username = request.json['username']
    password_hash = request.json['email']
    email = request.json['email']
    phone_number = request.json['emphone_numberail']
    registration_date = request.json['registration_date']
    role = request.json['role']
    updated = update_customer(user_id,username, password_hash, email,phone_number,registration_date,role)
    return jsonify(updated), 200

@app.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer_by_id(user_id):
    delete_customer(user_id)
    return jsonify({"id":user_id}), 200

def get_all_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products')
    products2 = cur.fetchmany()
    final_prod = []
    for product in products2:
        final_prod.append({
            "product_id": product[0],
            "name": product[1],
            "description": product[2],
            "price": product[3],
            "category_id": product[4],
            "image": product[5]
        })
    conn.close()
    return final_prod

@app.route('/products', methods=['GET'])
def list_customer():
    customers = get_all_products()
    response = jsonify(customers)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(customers)
    return response

if __name__ == '__main__':
    app.run(debug=True)