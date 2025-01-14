#Helper functions for vouchers

#Imports
import sqlite3


class Vouchers:

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



    def check_value(voucherid:str) -> dict:
        """
        Function to return the value of a certain voucher given its voucherid

        Args:
            voucherid (str): Unique identifier of the voucher

        Returns:
            dict: JSON containing value of voucher as 'Amount'
        """
        
        #Get db connection
        conn = sqlite3.connect("../sqlite_db")
        
        #Check if voucher exists first
        voucher = conn.execute("SELECT Amount FROM Vouchers WHERE Voucherid = ?",(voucherid,)).fetchone()
        if not voucher: #Does not exist
            return {"Status": False, "Message": "Error, voucher does not exist."}
        
        #Get voucher value
        amount = voucher["Amount"]
        
        return {"Amount": amount}
    
    
    def get_vouchers(userid:str) -> dict:
        """
        Function to get all vouchers under a userid

        Args:
            userid (str): Unique identifier of a user

        Returns:
            dict: JSON with "Vouchers" for all the vouchers
        """
        #Get db connection
        conn = sqlite3.connect("../sqlite_db")
        
        #Get vouchers
        vouchers = conn.execute("SELECT * FROM Vouchers WHERE Userid = ?",(userid,)).fetchall()
        conn.close()
        
        return {"Vouchers":vouchers}