# Python standard libraries
import json
import os
import sqlite3
from datetime import datetime, timedelta
from random import shuffle

# Third party libraries
from flask import Flask, redirect, request, url_for, render_template


import requests

# Internal imports 
from db import init_db_command, get_db
from user import User
year = str(datetime.today().year)
year = year[2:]

# Flask app setup https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass


@app.route("/login")
def login(username, password):
    
    connection = sqlite3.connect("sqlite_db")
    cursor = connection.cursor()
    cursor.execute("SELECT Name,Password,Isadmin FROM User WHERE Name={}".format(username))
    user = cursor.fetchone()

    cursor.fetchall() #clear the cursor
    
    
    return {"Username":user[0], "Password":user[1], "Isasmin":user[2]}
    








if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    #app.debug = False
    
    #for normal local testing use this run
    app.run(ssl_context="adhoc",host='127.0.0.1', port=port, debug=True)
    
    #For Deployment
    #app.run(host='0.0.0.0', port=port, debug=True)