#Helper function for user

#imports
import sqlite3
import modules

class User:
    
    def user_exists(username:str) -> bool:
        """
        Function that takes in a username and checks if that user exists

        Args:
            username (str): Username of the user

        Returns:
            bool: True if user exists, else False
        """
        #Get Connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Try to retrieve user
        existing_user = conn.execute('SELECT * FROM User WHERE Name = ?', (username,)).fetchone()
        conn.close()
        
        if existing_user:
            return True
        
        return False
    
        
    def get_userid(username:str) -> dict:
        """
        Function that takes in a username and returns the userid

        Args:
            username (str): Username of the user, which should be unique
            
        Returns:
            userid (dict): userid labelled by 'Userid', the unique identifier of the user
        """
        
        #Open connection to db
        conn = sqlite3.connect("../sqlite_db.db") #Pathing based on root directory
        
        #Retrieve userid
        userid = conn.execute("SELECT Userid from User where Name = ?",(username,)).fetchone()
        
        #Close connection
        conn.close()
        
        return {"Userid": userid}



    def get_user(userid:str) -> dict:
        """
        Function that takes in a userid and returns that user

        Args:
            userid (str): unique identifier of that user

        Returns:
            dict: json format with user
        """

        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Get username
        user = conn.execute("SELECT * FROM User WHERE Userid = ?", (userid,)).fetchone()
        conn.close()
        
        return {"User": user}



    def isadmin(userid:str) -> bool:
        """
        Function to validate if a user of this userid is an admin

        Args:
            userid (str): Userid of this user

        Returns:
            bool: True if this guy is admin, False if not
        """
        
        #Get connection to db
        conn = sqlite3.connect("../sqlite_db.db") #Based on root path
        
        #Get Isadmin field
        user = conn.execute("SELECT Isadmin FROM User where Userid = ?", (userid,)).fetchone()
        isadmin = user["Isadmin"]
        
        if isadmin: #User is admin
            return True
        
        return False #User is not an admin
    
    
    def register_user(username:str, password:str, mobile:str, is_admin:int, status:int) -> dict:
        """
        Function to register a user

        Args:
            username (str): Username of the user, must be unique
            password (str): User password
            mobile (str): Mobile number to be used in resestting
            is_admin (int): 1 for admin, 0 for normal user
            status (int): 1 for active, 0 for suspended

        Returns:
            dict: status of this action, and error message if any
        """
        
        #Get connection to db
        conn = sqlite3.connect("../sqlite_db.db") #Based on root path
        
        #Create user
        try:
            conn.execute(
                'INSERT INTO User (username, password, mobile, isadmin, status) VALUES (?, ?, ?, ?, ?)',
                (username, password, mobile, is_admin, status)
            )
            conn.commit()
            conn.close()
            
        except:
            conn.close()
            return {"Status": False, "Message": "Failed to register user"}
        
        return {"Status":True, "Message": f"Successfully created user {username}"}
    
    
    def delete_user(userid:str) -> dict:
        """
        Function to delete a user

        Args:
            userid (str): Unique identifier of the user

        Returns:
            dict: deletion status
        """
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")

        #Delete the user
        try:
            conn.execute("DELETE FROM User WHERE Userid = ?", (userid,))
            conn.commit()
            conn.close()
        
        except:
            conn.close()
            return {"Status": False, "Message": "Failed to delete user"}

        return {"Status": True, "Message": "User successfully deleted"}
    
    
    
    def issuspended(userid:str) -> bool:
        """
        Function that checks if a user is suspended

        Args:
            userid (str): Userid of the user to check

        Returns:
            bool: Status of the user
        """
        
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Get Status (1 for active, 0 for suspended)
        status = conn.execute("SELECT Status FROM User WHERE Userid = ?", (userid,))["Status"]
        conn.close()
        
        if status:
            return False
        
        return True
    
    
    
    def suspend_user(userid:str) -> dict:
        """
        Function to suspend a user

        Args:
            userid (str): Identifier of the user to suspend

        Returns:
            dict: Status of the suspension
        """
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Suspend the user
        try:
            conn.execute("UPDATE User SET Status = 0 WHERE Userid = ?", (userid,))
            conn.commit()
            conn.close()
        
        except:
            conn.close()
            return {"Status": False, "Message": "Failed to suspend user"}
    
        return {"Status": True, "Message": "User suspended"}
    
    
    def unsuspend_user(userid:str) -> dict:
        """
        Function to unsuspend a user

        Args:
            userid (str): Unique Identifier

        Returns:
            dict: Unsuspension status
        """
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Suspend the user
        try:
            conn.execute("UPDATE User SET Status = 1 WHERE Userid = ?", (userid,))
            conn.commit()
            conn.close()
        
        except:
            conn.close()
            return {"Status": False, "Message": "Failed to unsuspend user"}
    
        return {"Status": True, "Message": "User unsuspended"}
    
    
    def reset_password(userid:str, new_password:str) -> dict:
        """
        Function to reset password for a user

        Args:
            userid (str): User unique identifier
            new_password (str): New password

        Returns:
            dict: Password reset status
        """
        
        #Get Conenction
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Reset password
        try:
            conn.execute(
                "UPDATE User SET Password = ? WHERE Userid = ?",
                (new_password, userid)
            )
            conn.commit()
            conn.close()
            
        except:
            conn.close()
            return {"Status": False, "Message": "Password failed to reset"}
        
        return {"Status": True, "Message": "Password reset"}
    
    
    def send_otp(userid:str) -> dict:
        """
        

        Args:
            userid (str): User identifier

        Returns:
            dict: Status
        """
        
        #Get Conenction
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Get Phone Number
        phone_number = conn.execute("SELECT Mobile FROM User WHERE Userid = ?", (userid,))["Mobile"]
        
        
        try:
            otp = modules.OTP.generate_otp()
            
            #Save the otp
            conn.execute(
                "INSERT INTO Otps (Userid, Otp) VALUES (?, ?)",
                (userid, otp)
            )
            conn.commit()
            
            modules.OTP.send_sms_otp(phone_number, otp)
            
        except:
            conn.close()
            return {"Status": False, "Message": "OTP Failed to send"}
        
        
        conn.close()
        return {"Status": True, "Message": "OTP sent"}
    
    
    def validate_otp(userid:str, otp:str) -> bool:
        """
        Function to valid otp for password reset

        Args:
            userid (str): user identifier
            otp (str): user input otp

        Returns:
            bool: If OTP is valid 
        """
        #Get Conenction
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Get the user otp
        valid_otp = conn.execute("SELECT * FROM Otps WHERE Userid = ?", (userid,))
        
        if valid_otp != otp:
            conn.close()
            return False
        
        #Delete otp entry since it is now valid
        conn.execute("DELETE FROM Otps WHERE Userid = ?", (userid,))
        conn.commit()
        conn.close()
        
        return True