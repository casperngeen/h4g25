# Python standard libraries
import os
import sqlite3
from random import shuffle

# Third party libraries
from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt


# Internal imports 
import modules
import modules.products
import modules.user

# Flask app setup https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

#Configure JWT
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

# JWT Initialization
jwt = JWTManager(app)



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
    is_admin = int(data.get('isadmin')) #1 for admin, 0 for normal user
    status = 1 #1 for active, 0 for suspended

    if not username or not password or not is_admin:
        return {'error': 'Username, password or isadmin is required'}, 400

    
    #Check if user exists
    existing_user = modules.User.user_exists(username)
    if existing_user:
        return {'Error': 'User already exists'}, 400


    #Register User
    register_status = modules.User.register_user(username,password,mobile,is_admin,status)
    if not register_status["Status"]:
        return {'Error': 'Failed to register user'}, 400
    
    #Log event
    userid = modules.User.get_userid(username)["Userid"]
    log = modules.Audit.record_log(userid, f"User {username} created.")
    
    return {'Message': 'User registered successfully'}, 201


#Login Path
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    #Retreive User
    userid = modules.User.get_userid(username)["Userid"]
    if not userid:
        return {"Error": "Failed to find user"}, 400
    user = modules.User.get_user(userid)["User"]
    
    
    #Validate User
    if user and user['password'] == password:
        #Check if account is active
        if user['status'] == 1:
            access_token = create_access_token(identity=username)
            
            #Log event
            log = modules.Audit.record_log(user["Userid"], "User login")
            
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
    username = data["Username"]
    
    jti = get_jwt()['jti']  # JWT ID
    blacklist.add(jti)  # Add the token's jti to the blacklist
    
    #Log event
    log = modules.Audit.record_log(modules.User.get_userid(username)["Userid"], "User logout")
    
    return {'Message': 'Successfully logged out'}, 200


#--------------------------------------------------------------------------------------------------------------------------

#Voucher system (Viewing data)

#View Vouchers (Need more security)
@app.route('/view_vouchers', methods=['POST'])
@jwt_required()
def view_vouchers():
    #Retrieve username from POST request
    data = request.json
    username = data['username']
    
    #Grab userid from db based on username
    userid = modules.User.get_userid(username)["Userid"]
    
    #Get all vouchers related to this userid
    vouchers = modules.Vouchers.get_vouchers(userid)["Vouchers"]
    if not vouchers:
        return {"Error":"Failed to retrieve vouchers"}, 400
    
    #Log event
    log = modules.Audit.record_log(userid, "User requested all vouchers")
    
    return {"User": username, "Available_Vouchers": vouchers}, 200



#View transactions (Need for security)
@app.route("/transaction_history", methods=["POST"])
@jwt_required
def transaction_history():
    #Retrieve username from POST request
    data = request.json
    username = data['username']
    
    #Grab userid from db based on username
    userid = modules.User.get_userid(username)["Userid"]
    
    #Retrieve all transactions for this user
    transactions = modules.Transactions.get_transactions(userid)["Transactions"]
    if not transactions:
        return {"Error": "Failed to retrieve transactions"}, 400
    
    
    #Parse transactions to contain createdtime,amount,vouchers,description where description is optional
    all_parsed_transactions = []
    for transaction in transactions:
        parsed_transaction = {}
        
        #Add the required fields in
        parsed_transaction["Created"] = transaction["Created"]
        parsed_transaction["Amount"] = transaction["Amount"]
        parsed_transaction["Vouchers"] = ",".join([modules.Vouchers.check_value(voucherid)["Amount"] for voucherid in transaction["Vouchers"].strip().split(",")])
        #Try except here as description is an optional field
        try:
            parsed_transaction["Description"] = transaction["Description"]
        except:
            pass
        
        #Append parsed transaction into all transactions
        all_parsed_transactions.append(parsed_transaction)
        
    #Log event
    log = modules.Audit.record_log(userid, "User requested all transaction history")
    
    return {"User": username, "Transactions": all_parsed_transactions}



#----------------------------------------------------------------------------------------------------------------

#Inventory Management


#View all products
@app.route("/view_products", methods=["GET"])
@jwt_required
def view_products():
    
    #Get all products
    products = modules.Products.get_products()["Products"]
    if not products:
        return {"Error":"Failed to retrieve products"}, 400
    
    return {"Products": products}, 200



#----------------------------------------------------------------------------------------------------------------

#Ordering (Requests)

#Admin view all product requests
@app.route("/view_product_requests", methods=["POST"])
@jwt_required
def view_product_requests():
    #Get user id
    data = request.json
    username = data["Username"]
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Check if user is an admin
    if not modules.User.isadmin(userid):
        return {"Error": "Access Forbidden"}, 401
    
    #Retrieve all product requests
    product_requests = modules.Product_Requests.get_requests()["Product_Requests"]
    
    
    #Add Username and Productname of each user into the data and change voucherids into values 
    for product_request in product_requests:
        #Add Username
        username = modules.User.get_user(product_request["Userid"])["Name"]
        product_request["Username"] = username
        
        #Add Productname
        productname = modules.Products.get_product(product_request["Productid"])["Name"]
        product_request["Productname"] = productname    
        
        #Change voucherids into voucher values
        voucherids = product_request["Vouchers"].strip().split(",")
        product_request["Vouchers"] = ",".join([modules.Vouchers.check_value(voucherid)["Amount"] for voucherid in voucherids])
       
    
    #Returns all product requests with fields: Requestid, Userid, Username, Productid, Productname, Quantity, Status, Created
    return {"Product_Requests": product_requests}



#Request product
@app.route("/request_product", methods=["POST"])
@jwt_required
def request_product():
    #Retrieve data
    data = request.json
    username = data["Username"]
    productid = data["Productid"]
    quantity = data["Quantity"]
    amount = data["Amount"] #Total amount to pay
    vouchers = data["Vouchers"] #Voucherids of vouchers to be used in csv format
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]

    #Check if this product still have this quantity left
    #Get current stock
    product = modules.Products.get_product(productid)["Product"]
    if not product:
        return {"Error": "Unable to retrieve product"}, 400
    
    stock = product["Stock"]
    
    #Check if stock enough
    if stock < quantity:
        return {"Error": f"Requested quantity exceeds current stock of {stock}"}, 404
    
    
    #Update product requests table
    request_status = modules.Product_Requests.create_request(userid, productid, quantity, amount, vouchers, "pending")
    if not request_status["Status"]:
        return {"Error": "Failed to create request"}, 400

    #Log this event
    log = modules.Audit.record_log(userid, f"Request product {productid} of quantity {quantity}")
    
    return {"Message": "Product request successfully updated, please await approval"}, 200
    


#Admin approve/reject request
@app.route("/update_product_request")
@jwt_required
def update_product_request():
    #Retrieve data
    data = request.json
    username = data["Username"]
    requestid = data["Requestid"]
    action = data["Action"] #Should be 'approved'/'rejected'
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Confirm that user performing action is an admin
    if not modules.User.isadmin(userid):
        return {"Error": "Access Forbidden"}, 401
    
    #Update the request status in the Product_Requests Table
    update_status = modules.Product_Requests.update_request_status(requestid, action)
    if not update_status["Status"]:
        return {"Error": "Failed to update request"}, 400
    
    #Log this update
    log = modules.Audit.record_log(userid, f"Product Request {requestid}: {action}")
    
    
    #Update various tables if approved, else no need care
    if action == "approved":
        #Retrieve needed fields from db
        product_request = modules.Product_Requests.get_request(requestid)["Product_Request"]
        productid = product_request["Productid"]
        quantity = product_request["Quantity"]
        vouchers = product_request["Vouchers"]
        
        #Update inventory (Stock in Products Table)
        #First get current stock
        product = modules.Products.get_product(productid)["Product"]
        if not product:
            return {"Error": "Failed to find product"}, 400
        
        #Calculate stock left
        stock_left = product["Stock"] - quantity
        
        #Update stock left
        update_stock_status = modules.Products.update_product(productid, product["Name"], stock_left, product["Price"])
        if not update_stock_status["Status"]:
            return {"Error": "Failed to update stock"}, 400
        
        
        #Update Transactions (New record in Transaction Table)



#----------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    #app.debug = False
    
    #for normal local testing use this run
    app.run(ssl_context="adhoc",host='127.0.0.1', port=port, debug=True)
    
    #For Deployment
    #app.run(host='0.0.0.0', port=port, debug=True)