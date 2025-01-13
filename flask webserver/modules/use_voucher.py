#Helper function to spend vouchers, add into transaction history

#Imports
import sqlite3


def use_voucher(voucherid:str) -> dict:
    """
    Function that takes in a voucherid and uses it, returns status of transaction

    Args:
        voucherid (str): voucherid of the voucher to use

    Returns:
        dict: status of transaction, error message if any
    """
    
    #Get connection to db
    conn = sqlite3.connect("../sqlite_db")
    
    #Check if voucher exists first
    voucher = conn.execute("SELECT * FROM Vouchers WHERE Voucherid = ?",(voucherid,)).fetchone()
    if not voucher: #Does not exist
        return {"Status": False, "Message": "Error, voucher does not exist."}
    
    
    #Delete voucher from voucher table
    conn.execute("DELETE FROM Vouchers WHERE Voucherid = ?",(voucherid,))
    conn.commit()
    conn.close()
    
    return {"Status": True, "Message": f"Voucher {voucherid} successfully deleted."}