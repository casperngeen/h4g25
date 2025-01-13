# Python standard libraries
import json
import os
import sqlite3
from datetime import datetime, timedelta
from random import shuffle

# Third party libraries
from flask import Flask, redirect, request, url_for, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

import requests

# Internal imports 
from db import init_db_command, get_db
from user import User
import modules

# Flask app setup https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

#Configure JWT
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

# JWT Initialization
jwt = JWTManager(app)


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass



# Blacklist to store revoked tokens
blacklist = set()

# Token blacklist check
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist


#Helper function to get db connection
def get_db_connection():
    conn = sqlite3.connect("sqlite_db")
    return conn

#---------------------------------------------------------------------------------------------------------------------------
#User management stuff

#Register Path
@app.route('/register', methods=['POST'])
@jwt_required
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    mobile = data.get('mobile')
    isadmin = int(data.get('isadmin')) #1 for admin, 0 for normal user
    status = 1 #1 for active, 0 for suspended

    if not username or not password or not isadmin:
        return {'error': 'Username, password or isadmin is required'}, 400


    conn = get_db_connection()
    
    #Check if user exists
    existing_user = conn.execute('SELECT * FROM User WHERE username = ?', (username,)).fetchone()
    if existing_user:
        return {'Error': 'User already exists'}, 400


    #Register User
    try:
        conn.execute(
            'INSERT INTO User (username, password, mobile, isadmin, status) VALUES (?, ?, ?, ?, ?)',
            (username, password, mobile, isadmin, status)
        )
        conn.commit()
        conn.close()
        
    except:
        conn.close()
        return {"Error": "Failed to register user"}, 401
    
    
    #Log event
    userid = modules.get_userid(username)
    log = modules.record_log(userid, "User created")
    
    return {'Message': 'User registered successfully'}, 201


#Login Path
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    #Retreive User
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT * FROM User WHERE username = ?', (username,)).fetchone()
        conn.close()
    
    except:
        conn.close()
        return {"Error": "Failed to find user"}, 401
    
    #Validate User
    if user and user['password'] == password:
        #Check if account is active
        if user['status'] == 1:
            access_token = create_access_token(identity=username)
            
            #Log event
            log = modules.record_log(user["Userid"], "User login")
            
            return {'access_token': access_token, 'isadmin': user['isadmin']}, 200
        else:
            return {'Error': 'Account Suspeneded'}, 401
    else:
        return {'Error': 'Invalid credentials'}, 401


#Logout Path
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    data = request.json
    userid = data["Userid"]
    
    jti = get_jwt()['jti']  # JWT ID
    blacklist.add(jti)  # Add the token's jti to the blacklist
    
    #Log event
    log = modules.record_log(userid, "User logout")
    
    return {'Message': 'Successfully logged out'}, 200


#--------------------------------------------------------------------------------------------------------------------------

#Voucher system (Viewing data)

#View Vouchers
@app.route('/view_vouchers', methods=['POST'])
@jwt_required()
def view_vouchers():
    #Retrieve username from POST request
    data = request.json
    username = data['username']
    
    #Grab userid from db based on username
    userid = modules.get_userid(username)["Userid"]
    
    #Get all vouchers related to this userid
    try:
        conn = get_db_connection()
        vouchers = conn.execute("SELECT * FROM Vouchers WHERE Userid = ?",(userid,)).fetchall()
        conn.close()
        
    except:
        conn.close()
        return {"Error":"Failed to retrieve vouchers"}, 404
    
    #Collate available vouchers into one list with fields userid and amount
    all_parsed_vouchers = []
    for voucher in vouchers:
        parsed_voucher = {}
        parsed_voucher["Userid"] = voucher["Userid"]
        parsed_voucher["Amount"] = voucher["Amount"]
        
        all_parsed_vouchers.append(parsed_voucher)
        
    #Log event
    log = modules.record_log(userid, "User requested all vouchers")
    
    return {"User": username, "Available_Vouchers": all_parsed_vouchers}, 200



#View transactions
@app.route("/transaction_history", methods=["POST"])
@jwt_required
def transaction_history():
    #Retrieve username from POST request
    data = request.json
    username = data['username']
    
    #Grab userid from db based on username
    userid = modules.get_userid(username)["Userid"]
    
    #Retrieve all transactions for this user
    try:
        conn = get_db_connection()
        transactions = conn.execute("SELECT * FROM Transactions WHERE Userid = ?",(userid,)).fetchall()
        conn.close()
    
    except:
        conn.close()
        return {"Error": "Failed to retrieve transactions"}, 404
    
    #Parse transactions to contain createdtime,amount,description where description is optional
    all_parsed_transactions = []
    for transaction in transactions:
        parsed_transaction = {}
        
        #Add the required fields in
        parsed_transaction["Created"] = transaction["Created"]
        parsed_transaction["Amount"] = transaction["Amount"]
        #Try except here as description is an optional field
        try:
            parsed_transaction["Description"] = transaction["Description"]
        except:
            pass
        
        #Append parsed transaction into all transactions
        all_parsed_transactions.append(parsed_transaction)
        
    #Log event
    log = modules.record_log(userid, "User requested all transaction history")
    
    return {"User": username, "Transactions": all_parsed_transactions}



#----------------------------------------------------------------------------------------------------------------

#Viewing, ordering products

@app.route("/view_products", methods=["GET"])
@jwt_required
def view_products():
    #Get all products
    conn = get_db_connection()
    
    try:
        products = conn.execute("SELECT * FROM Products").fetchall()
        conn.close()
        
    except:
        conn.close()
        return {"Error":"Failed to retrieve products"}, 404
    
    return {"Products": products}


@app.route("/request_product", methods=["POST"])
@jwt_required
def request_product():
    #Retrieve data
    data = request.json
    userid = data["Userid"]
    productid = data["Productid"]
    quantity = data["Quantity"]

    #Check if this product still have this quantity left
    #Get current stock
    conn = get_db_connection()
    try:
        stock = conn.execute("SELECT Stock from Products WHERE Productid = ?", (productid,)).fetchone()

    except:
        conn.close()
        return {"Error": "Unable to retrieve product"}, 404
    
    #Check if stock enough
    if stock >= quantity:
        stock_left = stock - quantity
    else:
        #Trigger error, not enough stock
        return {"Error": f"Requested quantity exceeds current stock of {stock}"}, 404
    
    
    #Update product requests table
    try:
        conn.execute(
            "INSERT INTO Product_Requests (Userid, Productid, Quantity, Status) VALUES (?, ?, ?, ?)",
            (userid, productid, quantity, "pending")
        )
        conn.commit()
    
    except:
        conn.close()
        return {"Error": "Failed to update request"}, 404

    #Log this event
    log = modules.record_log(userid, f"Request product {productid} of quantity {quantity}")
    
    return {"Message": "Product request successfully updated, please await approval"}, 200
    
    

#----------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    #app.debug = False
    
    #for normal local testing use this run
    app.run(ssl_context="adhoc",host='127.0.0.1', port=port, debug=True)
    
    #For Deployment
    #app.run(host='0.0.0.0', port=port, debug=True)