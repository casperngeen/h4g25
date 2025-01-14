#Helper functions for product requests

#Imports
import sqlite3

class Product_Requests:
    
    def get_requests() -> dict:
        """
        Function to get all product requests

        Returns:
            dict: JSON with key "Product_Requests" for all requests
        """
        
        #Get connection
        conn = sqlite3.connect("../sqlite_db")
        
        #Get Requests
        product_requests = conn.execute("SELECT * FROM Product_Requests").fetchall()
        conn.close()
        
        return {"Product_Requests": product_requests}
    
    
    def get_request(requestid:str) -> dict:
        """
        Function to get product request
        
        Args:
            requestid (str): Request unique identifier

        Returns:
            dict: JSON with key "Product_Request" for request
        """
        
        #Get connection
        conn = sqlite3.connect("../sqlite_db")
        
        #Get Requests
        product_request = conn.execute("SELECT * FROM Product_Requests WHERE Requestid = ?", (requestid,)).fetchone()
        conn.close()
        
        return {"Product_Request": product_request}
    
    
    def create_request(userid:str, productid:str, quantity:int, amount:float, vouchers:str, status:str) -> dict:
        """
        Function to create a new product request

        Args:
            userid (str): User unique identifier
            productid (str): Product unique identifier
            quantity (int): Number of items requested
            amount (float): total cost
            vouchers (str): Voucherids of vouchers to use, in csv
            status (str): 'pending', 'approved', 'rejected'

        Returns:
            dict: Status of creation, error message if there is.
        """
        #Get connection
        conn = sqlite3.connect("../sqlite_db")
        
        #Create request
        try:
            conn.execute(
                "INSERT INTO Product_Requests (Userid, Productid, Quantity, Amount, Vouchers, Status) VALUES (?, ?, ?, ?, ?, ?)",
                (userid, productid, quantity, amount, vouchers, status)
            )
            conn.commit()
            conn.close()
        
        except:
            conn.close()
            return {"Status": False, "Message": "Request failed to be created."}
        
        return {"Status": True, "Message": "Request created."}
    
    
    def update_request_status(requestid:str, action:str) -> dict:
        """
        Function to update request status, from pending to approved/rejected

        Args:
            requestid (str): request unique identifier
            action (str): approved/rejected

        Returns:
            dict: Status of creation, error message if there is.
        """
        #Get connection
        conn = sqlite3.connect("../sqlite_db")
        
        #Update request status
        try:
            conn.execute("UPDATE Product_Requests SET Status = ? WHERE Requestid = ?",(action, requestid))
            conn.commit()
            conn.close()
            
        except:
            conn.close()
            return {"Status": False, "Message": f"Request {requestid} failed to update."}
        
        return {"Status": True, "Message": f"Request {requestid} updated to {action}."}
        