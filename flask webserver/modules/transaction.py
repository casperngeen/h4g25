#Helper function to record transaction in transaction history

#Imports
import sqlite3


class Transactions:
    
    def get_transactions(userid:str) -> dict:
        """
        Function to grab all transaction record for a user

        Args:
            userid (str): Identifier for a user

        Returns:
            dict: JSON with key "Transactions" for all transactions
        """
        #Open connection
        conn = sqlite3.connect("../sqlite_db.db") #Path based on root folder
    
        #Grab the transactions
        transactions = conn.execute("SELECT * FROM Transactions WHERE Userid = ?",(userid,)).fetchall()
        conn.close()
        
        return {"Transactions": transactions}
    
    
    def record_transaction(userid:str, amount:float, action:str, vouchers:str, description:str="") -> dict:
        """
        Function to record transactions into the Transactions table

        Args:
            userid (str): Userid to identify the user for this action
            amount (float): Amount transacted
            action (str): To know if it is Add/Deduct
            vouchers (str): Voucherids of the vouchers used in this transaction, in csv format
            description (str, optional): Additional information if any. Defaults to "":str.

        Returns:
            dict: status of recording and error messages if any
        """
        
        #Change the Amount if action is deduct
        if action == "Deduct":
            amount = 0 - amount #flip the sign
            
        #Open connection
        conn = sqlite3.connect("../sqlite_db.db") #Path based on root folder
        
        #Insert current transaction record
        try:
            conn.execute(
                "INSERT INTO Transactions (Userid, Description, Amount, Vouchers) VALUES (?, ?, ?, ?)",
                (userid, description, amount, vouchers)
            )
            conn.commit()
            
        except: #Failed to insert
            conn.close()
            return {"Status": False, "Message": "Failed to insert into database."}
        
        
        conn.close()
        
        return {"Status": True, "Message": f"Transaction of {amount} successfully recorded."}