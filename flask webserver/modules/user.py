#Helper function for user

#imports
import sqlite3

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
        conn = sqlite3.connect("../sqlite_db")
        
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
        conn = sqlite3.connect("../sqlite_db") #Pathing based on root directory
        
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
        conn = sqlite3.connect("../sqlite_db")
        
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
        conn = sqlite3.connect("../sqlite_db") #Based on root path
        
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
        conn = sqlite3.connect("../sqlite_db") #Based on root path
        
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