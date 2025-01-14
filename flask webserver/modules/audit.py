#Helper function to audit action

#Imports
import sqlite3

class Audit:
        
    def record_log(userid:str, action:str, details:str="") -> dict:
        """
        Function to log any action taken by a user for auditing

        Args:
            userid (str): Userid of the user who performed this action
            action (str): action of the user
            details (str, optional): Additional details of specified action. Defaults to "".

        Returns:
            dict: Status of the recording, and error messages if any.
        """
        
        #Get db connection
        conn = sqlite3.connect("../sqlite_db.db") #Path based on the root folder
        
        #Add the log in
        try:
            conn.execute(
                "INSERT INTO Audit_Logs (Userid, Action, Details) VALUES (?, ?, ?)",
                (userid, action, details)
            )
            conn.commit()
        
        except:
            conn.close()
            return {"Status": False, "Message": f"Action related to user {userid} failed to log."}
        
        
        conn.close()
        
        return {"Status": True, "Message": f"Action related to user {userid} successfully logged."}