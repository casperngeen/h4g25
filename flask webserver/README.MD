User Management APIs

 1. /register (POST) (Require JWT)
    INPUT -> {'username':str, 'password':str, 'mobile':str, 'isadmin':int, 'Adminid':str} 
        Username - username
        Password - user's password
        Mobile - Mobile number for sms otp
        isadmin - 1 for admin, 0 for normal user
        Adminid - userid of the admin registering new user

    OUTPUT -> 'Message' (200) / 'Error' (400/401)

 2. /login (POST)
    INPUT -> {'username':str, 'password':str}
        Username - username
        Password - user's password
    
    OUTPUT -> {'access_token': access_token, 'isadmin': 0/1} (200) / 'Error' (400/401)

 3. /logout (POST) (Require JWT)
    INPUT -> {'Username':str}
        Username - username
    
    OUTPUT -> 'Message' (200) / 'Error' (400)

 4. /reset_password (POST)     [Sends OTP]
    INPUT -> {'Username':str}
        Username - username
    
    OUTPUT -> 'Message' (200) / 'Error' (400)

 5. /validate_reset (POST)      [Validates OTP and reset]
    INPUT -> {'Username':str, 'New_Password':str, 'OTP':str}
        Username - username
        New_Password - user new password
        OTP - OTP send to user's mobile

    OUTPUT -> 'Message' (200) / 'Error' (400/401)

 6. /suspend (POST) (Require JWT)       [Suspends a user]
    INPUT -> {'Username':str, 'Adminid':str}
        Username - username
        Adminid -> Userid of admin performing this action
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)

 7. /unsuspend (POST)  (Require JWT)       [Unsuspends a user]
    INPUT -> {'Username':str, 'Adminid':str}
        Username - username
        Adminid -> Userid of admin performing this action
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)

 8. /delete_user (POST)  (Require JWT)
    INPUT -> {'Username':str, 'Adminid':str}
        Username - username
        Adminid -> Userid of admin performing this action
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)



Voucher System APIs

 1. /view_vouchers (POST)  (Require JWT)     [Retrieves all vouchers under one person]
    INPUT -> {'Username':str}
        Username - username

    OUTPUT -> {"User": str, "Available_Vouchers": list} (200) / 'Error' (400)

 2. /transaction_history (POST) (Require JWT)     [Retrieves all transaction under a person]
    INPUT -> {'Username':str}
        Username - username

    OUTPUT -> {"User": str, "Transactions": list} (200) / 'Error' (400)

 3. /get_voucher_tasks (POST) (Require JWT)
    INPUT -> {'Username':str}
        Username - username
    
    OUTPUT -> {"Voucher_Tasks": list}, (200) / 'Error' (400/401)

 4. /create_voucher_task (POST) (Require JWT)
    INPUT -> {'Username':str, 'Description':str, 'Amount':real}
        Username - username
        Description - What the task entails
        Amount - Voucher value to be awarded upon completion
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)

 5. /update_voucher_task (POST) (Require JWT)
    INPUT -> {'Username':str, 'Requestid':str, 'Action':str}
        Username - username
        Requestid - Unique identifer for request
        Action - 'approved' or 'rejected'
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)



Inventory Management

 1. /view_products (GET) (Require JWT)
    OUTPUT -> {"Products": list} (200) / 'Error' (400/401)

 2. /create_product (POST) (Require JWT)
    INPUT -> {'Username':str, 'Productname':str, 'Stock':int, 'Price':real}
        Username - username
        Productname - Name of Product
        Stock - No of product left
        Price - price per product item
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)

 3. /update_product (POST) (Require JWT)
    INPUT -> {'Username':str, 'Productid':str, 'Productname':str, 'Stock':int, 'Price':real}
        Username - username
        Productid - Unique identifier of product
        Productname - Name of Product
        Stock - No of product left
        Price - price per product item
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)

 4. /delete_product (POST) (Require JWT)
    INPUT -> {'Username':str, 'Productid':str}
        Username - username
        Productid - Unique identifier of product
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)



Product Requesting

 1. /view_product_requests (POST) (Require JWT)
    INPUT -> {'Username':str}
        Username - username

    OUTPUT -> {"Product_Requests": list} (200) / 'Error' (400/401)

 2. /request_product (POST) (Require JWT)
    INPUT -> {'Username':str, 'Productid':str, 'Quantity':int, 'Amount':real, 'Vouchers':str}
        Username - username
        Productid - Unique identifier of product
        Quantity - No of products requested
        Amount - total value of products requested
        Vouchers - Voucherids of vouchers to be used
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)

 3. /update_product_request (POST) (Require JWT)
    INPUT -> {'Username':str, 'Requestid':str, 'Action':str}
        Username - username
        Requestid - Unique identifer for request
        Action - 'approved' or 'rejected'
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)



Preorder System

 1. /view_preorders (POST) (Require JWT)
    INPUT -> {'Username':str}
        Username - username

    OUTPUT -> {"Preorders": list} (200) / 'Error' (400/401)

 2. /preorder (POST) (Require JWT)
    INPUT -> {'Username':str, 'Productid':str, 'Quantity':int, 'Amount':real, 'Vouchers':str}
        Username - username
        Productid - Unique identifier of product
        Quantity - No of products preordered
        Amount - total value of products preordered
        Vouchers - Voucherids of vouchers to be used
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)

 3. /update_peorder (POST) (Require JWT)
    INPUT -> {'Username':str, 'Preorderid':str, 'Action':str}
        Username - username
        Preorderid - Unique identifer for preorder
        Action - 'approved' or 'rejected'
    
    OUTPUT -> 'Message' (200) / 'Error' (400/401)



Report Generating

 1. /generate_request_report (POST)     [Generates weekly report of all requests]
    INPUT -> {'Username':str}
        Username - username
    
    OUTPUT -> PDF File to be downloaded

 2. /generate_inventory_report (POST)       [Generates report for all inventory]
    INPUT -> {'Username':str}
        Username - username
    
    OUTPUT -> PDF File to be downloaded