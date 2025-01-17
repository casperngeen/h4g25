# Python standard libraries
import os
from random import shuffle

# Third party libraries
from flask import Flask, request, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt


# Internal imports 
import modules

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
        if not modules.User.issuspended(userid):
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


#Suspend user
@app.route("/suspend", methods=["POST"])
@jwt_required
def suspend():
    #Retrieve data
    data = request.json
    username = data["Username"]
    admin_id = data["Adminid"]
    
    #Confirm that user performing action is an admin
    if not modules.User.isadmin(admin_id):
        return {"Error": "Access Forbidden"}, 401
    
    #Get the user's userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Suspend the user
    suspend_status = modules.User.suspend_user(userid)["Status"]
    if not suspend_status:
        return {"Error": "Failed to suspend user"}, 400
    
    return {"Message": "User suspended successfully"}, 200


#Unsuspend user
@app.route("/unsuspend", methods=["POST"])
@jwt_required
def unsuspend():
    #Retrieve data
    data = request.json
    username = data["Username"]
    admin_id = data["Adminid"]
    
    #Confirm that user performing action is an admin
    if not modules.User.isadmin(admin_id):
        return {"Error": "Access Forbidden"}, 401
    
    #Get the user's userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #unsuspend the user
    suspend_status = modules.User.unsuspend_user(userid)["Status"]
    if not suspend_status:
        return {"Error": "Failed to unsuspend user"}, 400
    
    return {"Message": "User unsuspended successfully"}, 200


#Delete User
@app.route("/delete_user", methods=["POST"])
@jwt_required
def delete_user():
    #Retrieve data
    data = request.json
    username = data["Username"]
    admin_id = data["Adminid"]
    
    #Confirm that user performing action is an admin
    if not modules.User.isadmin(admin_id):
        return {"Error": "Access Forbidden"}, 401
    
    #Get the user's userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Delete the user
    delete_status = modules.User.delete_user(userid)["Status"]
    if not delete_status:
        return {"Error": "Failed to delete user"}, 400
    
    return {"Message": "User successfuly deleted"}, 200
    
#--------------------------------------------------------------------------------------------------------------------------

#Voucher system 

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



@app.route("get_voucher_tasks", methods=["POST"])
@jwt_required
def get_voucher_tasks():
    #Get Data
    data = request.json
    username = data["Username"]
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Check if user is an admin
    if not modules.User.isadmin(userid):
        return {"Error": "Access Forbidden"}, 401
    
    #Get the tasks
    voucher_tasks = modules.Vouchers_Task.get_tasks()
    if not voucher_tasks:
        return {"Error": "Failed to retrieve tasks"}, 400
    
    return {"Voucher_Tasks": voucher_tasks}, 200
    


@app.route("/create_voucher_task", methods=["POST"])
@jwt_required
def create_voucher_task():
    #Get Data
    data = request.json
    username = data["Username"]
    description = data["Description"]
    amount = data["Amount"]
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Create the task
    create_status = modules.Vouchers_Task.request_voucher(userid, description, amount)["Status"]
    if not create_status:
        return {"Error": "Failed to create task"}, 400
    
    #Log this event
    log = modules.Audit.record_log(userid, f"Voucher task created")
    
    
    return {"Message": "Task Successfully Created"}, 200



@app.route("/update_voucher_task", methods=["POST"])
@jwt_required
def update_voucher_task():
    #Get Data
    data = request.json
    username = data["Username"]
    requestid = data["Requestid"]
    action = data["Action"]
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Check if user is an admin
    if not modules.User.isadmin(userid):
        return {"Error": "Access Forbidden"}, 401
    
    
    #Update the voucher_task
    update_status = modules.Vouchers_Task.approve_reject_voucher(requestid, action)["Status"]
    if not update_status:
        return {"Error": "Failed to update task"}, 400
    
    #Log this event
    log = modules.Audit.record_log(userid, f"Voucher task {requestid} updated")
    
    
    return {"Message": "Task Successfully Updated"}, 200
    
    
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



#Create Product
@app.route("/create_product", methods=["POST"])
@jwt_required
def create_product():
    
    #Retrieve data
    data = request.json
    username = data["Username"]
    productname = data["Productname"]
    stock = data["Stock"]
    price = data["Price"]
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Check if user is an admin
    if not modules.User.isadmin(userid):
        return {"Error": "Access Forbidden"}, 401
    
    
    #Create the product
    update_status = modules.Products.create_product(productname, stock, price)["Status"]
    if not update_status:
        return {"Error": "Failed to create product"}, 400
    
    #Log this event
    log = modules.Audit.record_log(userid, f"Product {productname} created")
    
    return {"Message": "Successfully create product"}, 200



#Update Product
@app.route("/update_product", methods=["POST"])
@jwt_required
def update_product():
    
    #Retrieve data
    data = request.json
    username = data["Username"]
    productid = data["Productid"]
    productname = data["Productname"]
    stock = data["Stock"]
    price = data["Price"]
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Check if user is an admin
    if not modules.User.isadmin(userid):
        return {"Error": "Access Forbidden"}, 401
    
    
    #Update the product
    update_status = modules.Products.update_product(productid, productname, stock, price)["Status"]
    if not update_status:
        return {"Error": "Failed to update product"}, 400
    
    #Log this event
    log = modules.Audit.record_log(userid, f"Product {productid} of updated")
    
    
    return {"Message": "Successfully updated product"}, 200
    
    

#Delete Product
@app.route("/delete_product", methods=["POST"])
@jwt_required
def delete_product():
    
    #Retrieve data
    data = request.json
    username = data["Username"]
    productid = data["Productid"]
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Check if user is an admin
    if not modules.User.isadmin(userid):
        return {"Error": "Access Forbidden"}, 401
    
    #Delete the product
    delete_status = modules.Products.delete_product(productid)["Status"]
    if not delete_status:
        return {"Error": "Failed to delete product"}, 400
    
    #Log this event
    log = modules.Audit.record_log(userid, f"Product {productid} deleted")
    
    return {"Message": "Delete success"}, 200
    

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
    
    return {"Message": "Product request successfully created, please await approval"}, 200
    


#Admin approve/reject product request
@app.route("/update_product_request", methods=["POST"])
@jwt_required
def update_product_request():
    #Retrieve data
    data = request.json
    username = data["Username"]
    requestid = data["Requestid"]
    action = data["Action"] #Should be 'approved'/'rejected'
    
    #Get userid
    admin_userid = modules.User.get_userid(username)["Userid"]
    
    #Confirm that user performing action is an admin
    if not modules.User.isadmin(admin_userid):
        return {"Error": "Access Forbidden"}, 401
    
    #Get userid of the user of the request
    userid = modules.Product_Requests.get_request(requestid)["Userid"]
    
    #Update the request status in the Product_Requests Table
    update_status = modules.Product_Requests.update_request_status(requestid, action)
    if not update_status["Status"]:
        return {"Error": "Failed to update request"}, 400
    
    #Log this update
    log = modules.Audit.record_log(admin_userid, f"Product Request {requestid}: {action}")
    
    
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
        
        #Log this update
        log = modules.Audit.record_log(admin_userid, f"Product {productid} updated")
        
        
        #Update Transactions (New record in Transaction Table)
        amount = product["Price"] * quantity
        transaction_status = modules.Transactions.record_transaction(userid, amount, "Deduct", vouchers)
        if not transaction_status["Status"]:
            return {"Error": "Failed to update transaction"}, 400
        
        #Log this update
        log = modules.Audit.record_log(admin_userid, f"Transaction created")
        
        #Remove used vouchers
        voucherids = vouchers.split(",")
        for voucherid in voucherids:
            #Delete the voucher
            use_status = modules.Vouchers.use_voucher(voucherid)
            if not use_status["Status"]:
                return {"Error": "Failed to delete used voucher"}, 400
            
            #Log this update
            log = modules.Audit.record_log(admin_userid, f"Voucher {voucherid} deleted")
        
    
    return {"Message": "Product Request Successfully updated."}, 200



#-----------------------------------------------------------------------------------------------------------------

#Preorder System

@app.route("/view_preorders", methods=["POST"])
@jwt_required
def view_preorders():
    #Get user id
    data = request.json
    username = data["Username"]
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]
    
    #Check if user is an admin
    if not modules.User.isadmin(userid):
        return {"Error": "Access Forbidden"}, 401
    
    preorders = modules.Preorders.get_preorders()["Preorders"]
    if not preorders:
        return {"Error": "Cannot find preorders"}, 400
    
    #Add more fields 
    for preorder in preorders:
        #Add Username
        username = modules.User.get_user(preorder["Userid"])["Name"]
        preorder["Username"] = username
        
        #Add Productname
        product = modules.Products.get_product(preorder["Productid"])
        preorder["Productname"] = product["Name"]
        
        #Change voucherids into voucher values
        voucherids = preorder["Vouchers"].strip().split(",")
        preorder["Vouchers"] = ",".join([modules.Vouchers.check_value(voucherid)["Amount"] for voucherid in voucherids])
       
        #Add Current Quantity
        preorder["Available_Quantity"] = product["Quantity"]
        
    #Returns all product requests with fields: Requestid, Userid, Username, Productid, Productname, Quantity, Available_Quantity, Status, Created
    return {"Preorders": preorders}, 200
    


#Preorder
@app.route("/preorder", methods=["POST"])
@jwt_required
def preorder():
    #Retrieve data
    data = request.json
    username = data["Username"]
    productid = data["Productid"]
    quantity = data["Quantity"]
    amount = data["Amount"] #Total amount to pay
    vouchers = data["Vouchers"] #Voucherids of vouchers to be used in csv format
    
    #Get userid
    userid = modules.User.get_userid(username)["Userid"]

    
    #Update preorder requests table
    preorder_status = modules.Preorders.create_preorder(userid, productid, quantity, amount, vouchers, "pending")
    if not preorder_status["Status"]:
        return {"Error": "Failed to create preorder"}, 400

    #Log this event
    log = modules.Audit.record_log(userid, f"Preorder of product {productid} of quantity {quantity}")
    
    return {"Message": "Preorder successfully created, please await approval"}, 200



#Admin approve/reject preorder
@app.route("/update_preorder", methods=["POST"])
@jwt_required
def update_preorder():
    #Retrieve data
    data = request.json
    username = data["Username"]
    preorderid = data["Preorderid"]
    action = data["Action"] #Should be 'approved'/'rejected'
    
    #Get userid
    admin_userid = modules.User.get_userid(username)["Userid"]
    
    #Confirm that user performing action is an admin
    if not modules.User.isadmin(admin_userid):
        return {"Error": "Access Forbidden"}, 401
    
    #Get userid of the user of the request
    userid = modules.Preorders.get_preorder(preorderid)["Userid"]
    
    #Update the request status in the Product_Requests Table
    update_status = modules.Preorders.update_preorder_status(preorderid, action)
    if not update_status["Status"]:
        return {"Error": "Failed to update request"}, 400
    
    #Log this update
    log = modules.Audit.record_log(admin_userid, f"Preorder {preorderid}: {action}")
    
    
    #Update various tables if approved, else no need care
    if action == "approved":
        #Retrieve needed fields from db
        preorder = modules.Preorders.get_preorder(preorderid)["Preorder"]
        productid = preorder["Productid"]
        quantity = preorder["Quantity"]
        vouchers = preorder["Vouchers"]
        

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
        
        #Log this update
        log = modules.Audit.record_log(admin_userid, f"Product {productid} updated")
        
        
        #Update Transactions (New record in Transaction Table)
        amount = product["Price"] * quantity
        transaction_status = modules.Transactions.record_transaction(userid, amount, "Deduct", vouchers)
        if not transaction_status["Status"]:
            return {"Error": "Failed to update transaction"}, 400
        
        #Log this update
        log = modules.Audit.record_log(admin_userid, f"Transaction created")
        
        #Remove used vouchers
        voucherids = vouchers.split(",")
        for voucherid in voucherids:
            #Delete the voucher
            use_status = modules.Vouchers.use_voucher(voucherid)
            if not use_status["Status"]:
                return {"Error": "Failed to delete used voucher"}, 400
            
            #Log this update
            log = modules.Audit.record_log(admin_userid, f"Voucher {voucherid} deleted")
        
    
    return {"Message": "Preorder Successfully updated."}, 200

#----------------------------------------------------------------------------------------------------------------
#Generate reports
@app.route("/generate_request_report", methods=["POST"])
@jwt_required
def generate_request_report():
    #Retrieve data
    data = request.json
    username = data["Username"]
    
    #Get userid
    admin_userid = modules.User.get_userid(username)["Userid"]
    
    #Confirm that user performing action is an admin
    if not modules.User.isadmin(admin_userid):
        return {"Error": "Access Forbidden"}, 401
    
    #Get report path
    report_path = modules.Reports.generate_weekly_requests()["Report Path"]
    
    #Log this update
    log = modules.Audit.record_log(admin_userid, f"Weekly request report generated")
        
    
    #Send the report back
    return send_file(
            report_path,
            as_attachment=True,  # Prompts download
            download_name="Weekly Requests Report",  # Use the requested filename for download
            mimetype="application/pdf"  # Correct MIME type
        )



@app.route("/generate_inventory_report", methods=["POST"])
@jwt_required
def generate_inventory_report():
    #Retrieve data
    data = request.json
    username = data["Username"]
    
    #Get userid
    admin_userid = modules.User.get_userid(username)["Userid"]
    
    #Confirm that user performing action is an admin
    if not modules.User.isadmin(admin_userid):
        return {"Error": "Access Forbidden"}, 401
    
    #Get report path
    report_path = modules.Reports.view_inventory()["Report Path"]
    
    #Log this update
    log = modules.Audit.record_log(admin_userid, f"Inventory report generated")
        
    
    #Send the report back
    return send_file(
            report_path,
            as_attachment=True,  # Prompts download
            download_name="Inventory Report",  # Use the requested filename for download
            mimetype="application/pdf"  # Correct MIME type
        )

#----------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    #app.debug = False
    
    #for normal local testing use this run
    app.run(ssl_context="adhoc",host='127.0.0.1', port=port, debug=True)
    
    #For Deployment
    #app.run(host='0.0.0.0', port=port, debug=True)