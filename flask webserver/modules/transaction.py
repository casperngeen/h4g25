#Helper function to record transaction in transaction history

#Imports
import sqlite3

def record_transaction(userid:str, amount:float, action:str, description:str="") -> dict:
    """
    Function to record transactions into the Transactions table

    Args:
        userid (str): Userid to identify the user for this action
        amount (float): Amount transacted
        action (str): To know if it is Add/Deduct
        description (str, optional): Additional information if any. Defaults to "":str.

    Returns:
        dict: status of recording and error messages if any
    """
    
    #Change the Amount if action is deduct
    if action == "Deduct":
        amount = 0 - amount #flip the sign
        
    #Open connection
    conn = sqlite3.connect("../sqlite_db") #Path based on root folder
    
    #Insert current transaction record
    try:
        conn.execute(
            "INSERT INTO Transactions (Userid, Description, Amount) VALUES (?, ?, ?)",
            (userid, description, amount)
        )
        conn.commit()
        
    except: #Failed to insert
        conn.close()
        return {"Status": False, "Message": "Failed to insert into database."}
    
    
    conn.close()
    
    return {"Status": True, "Message": f"Transaction of {amount} successfully recorded."}