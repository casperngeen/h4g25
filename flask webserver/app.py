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


#Register Path
@app.route('/register', methods=['POST'])
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
        return {'error': 'User already exists'}, 400


    #Register User
    conn.execute(
        'INSERT INTO User (username, password, mobile, isadmin, status) VALUES (?, ?, ?, ?, ?)',
        (username, password, mobile, isadmin, status)
    )
    conn.commit()
    conn.close()
    
    
    return {'message': 'User registered successfully'}, 201


#Login Path
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    #Retreive User
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM User WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    #Validate User
    if user and user['password'] == password:
        #Check if account is active
        if user['status'] == 1:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token, 'isadmin': user['isadmin']}, 200
        else:
            return {'error': 'Account Suspeneded'}, 401
    else:
        return {'error': 'Invalid credentials'}, 401


#Logout Path
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']  # JWT ID
    blacklist.add(jti)  # Add the token's jti to the blacklist
    return {'message': 'Successfully logged out'}, 200



@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {'message': f'Hello, {current_user}!'}, 200





if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    #app.debug = False
    
    #for normal local testing use this run
    app.run(ssl_context="adhoc",host='127.0.0.1', port=port, debug=True)
    
    #For Deployment
    #app.run(host='0.0.0.0', port=port, debug=True)