#Helper function to get userid from username

#imports
import sqlite3

def get_userid(username) -> dict:
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
    userid = conn.execute("SELECT Userid from User where username = ?",(username,)).fetchone()
    
    #Close connection
    conn.close()
    
    return {"Userid": userid}