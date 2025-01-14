#Helper Functions for preorder system

#Imports 
import sqlite3


class Preorders:
    
    
    def get_preorders() -> dict:
        """
        Function to get all preorders

        Returns:
            dict: JSON with key "Preorders" for all preorders
        """
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Get all the preorders
        preorders = conn.execute("SELECT * FROM Preorders").fetchall()
        conn.close()
        
        return {"Preorders": preorders}
    
    
    def get_preorder(preorderid:str) -> dict:
        """
        Function that takes in a preorderid and returns the preorder

        Args:
            preorderid (str): Unique identifier of a preorder

        Returns:
            dict: JSON with Preorder
        """
        
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Get Preorder
        preorder = conn.execute("SELECT * FROM Preorders WHERE Preorderid = ?", (preorderid,)).fetchone()
        conn.close()
        
        return {"Preorder": preorder}
    
    
    def create_preorder(userid:str, productid:str, quantity:int, amount:float, vouchers:str, status:str) -> dict:
        """
        Function to create a new preorder 

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
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Create request
        try:
            conn.execute(
                "INSERT INTO Preorders (Userid, Productid, Quantity, Amount, Vouchers, Status) VALUES (?, ?, ?, ?, ?, ?)",
                (userid, productid, quantity, amount, vouchers, status)
            )
            conn.commit()
            conn.close()
        
        except:
            conn.close()
            return {"Status": False, "Message": "Preorder failed to be created."}
        
        return {"Status": True, "Message": "Preorder created."}
    
    
    def update_preorder_status(preorderid:str, action:str) -> dict:
        """
        Function to update preorder status, from pending to approved/rejected

        Args:
            preorderid (str): preorder unique identifier
            action (str): approved/rejected

        Returns:
            dict: Status of creation, error message if there is.
        """
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Update preorder status
        try:
            conn.execute("UPDATE Preorders SET Status = ? WHERE Preorderid = ?",(action, preorderid))
            conn.commit()
            conn.close()
            
        except:
            conn.close()
            return {"Status": False, "Message": f"Preorder {preorderid} failed to update."}
        
        return {"Status": True, "Message": f"Preorder {preorderid} updated to {action}."}