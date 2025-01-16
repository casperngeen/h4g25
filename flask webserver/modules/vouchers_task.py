import sqlite3

class Vouchers_Task:
    

    def request_voucher(userid: str, description: str, amount: float) -> dict:
        """
        Function for a user to request a voucher.

        Args:
            userid (str): Unique identifier of the user requesting the voucher.
            description (str): Description of the voucher request.
            amount (float): Requested voucher amount.

        Returns:
            dict: Status of the request.
        """
        # Open connection to database
        conn = sqlite3.connect("../sqlite_db")

        try:
            # Insert voucher request into a pending table
            conn.execute(
                "INSERT INTO PendingVouchers (Userid, Description, Amount, Status) VALUES (?, ?, ?, ?)",
                (userid, description, amount, "pending"),
            )
            conn.commit()
            conn.close()
            return {"Status": True, "Message": f"Voucher request for {amount} submitted successfully."}
        except Exception as e:
            conn.close()
            return {"Status": False, "Message": f"Failed to request voucher: {str(e)}"}

    
    def approve_reject_voucher(requestid: str, action: str) -> dict:
        """
        Function for an admin to approve or reject a voucher request.

        Args:
            requestid (str): Unique identifier for the voucher request.
            action (str): Either 'approve' or 'reject'.

        Returns:
            dict: Status of the action.
        """
        # Open connection to database
        conn = sqlite3.connect("../sqlite_db")

        try:
            if action == "approve":
                # Move the request to the Vouchers table
                voucher = conn.execute(
                    "SELECT Userid, Description, Amount FROM PendingVouchers WHERE Requestid = ? AND Status = 'pending'",
                    (requestid,),
                ).fetchone()

                if not voucher:
                    conn.close()
                    return {"Status": False, "Message": f"No pending voucher found for Request ID {requestid}."}

                userid, description, amount = voucher
                conn.execute(
                    "INSERT INTO Vouchers (Userid, Description, Amount) VALUES (?, ?, ?)",
                    (userid, description, amount),
                )
                conn.execute("DELETE FROM PendingVouchers WHERE Requestid = ?", (requestid,))
                conn.commit()
                conn.close()
                return {"Status": True, "Message": f"Voucher {requestid} approved and added to Vouchers table."}

            elif action == "reject":
                # Reject the voucher request by updating the status
                conn.execute(
                    "UPDATE PendingVouchers SET Status = 'rejected' WHERE Requestid = ? AND Status = 'pending'",
                    (requestid,),
                )
                conn.commit()
                conn.close()
                return {"Status": True, "Message": f"Voucher {requestid} rejected successfully."}

            else:
                conn.close()
                return {"Status": False, "Message": "Invalid action. Use 'approve' or 'reject'."}
        except Exception as e:
            conn.close()
            return {"Status": False, "Message": f"Failed to process voucher: {str(e)}"}

    
    def add_voucher(userid: str, description: str, amount: float) -> dict:
        """
        Function to add a voucher directly to the Vouchers table.

        Args:
            userid (str): Unique identifier of the user.
            description (str): Description of the voucher.
            amount (float): Amount for the voucher.

        Returns:
            dict: Status of the action.
        """
        # Open connection to database
        conn = sqlite3.connect("../sqlite_db")

        try:
            conn.execute(
                "INSERT INTO Vouchers (Userid, Description, Amount) VALUES (?, ?, ?)",
                (userid, description, amount),
            )
            conn.commit()
            conn.close()
            return {"Status": True, "Message": f"Voucher for {userid} added successfully."}
        except Exception as e:
            conn.close()
            return {"Status": False, "Message": f"Failed to add voucher: {str(e)}"}