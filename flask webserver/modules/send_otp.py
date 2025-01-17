import random
from twilio.rest import Client

class OTP:
    def generate_otp(length=6):
        """
        Generate a random numeric OTP.
        
        Args:
            length (int): Length of the OTP. Default is 6.
            
        Returns:
            str: The generated OTP.
        """
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    def send_sms_otp(phone_number, otp):
        """
        Send an OTP to a user's phone number using Twilio.
        
        Args:
            phone_number (str): The recipient's phone number (e.g., "+1234567890").
            otp (str): The OTP to send.
            
        Returns:
            None
        """
        
        account_sid = 'your_actual_account_sid'
        auth_token = 'your_actual_auth_token'
        twilio_phone_number = '+1234567890'  # Replace with your Twilio phone number
        
        client = Client(account_sid, auth_token)
        
        message_body = f"Your password reset OTP is: {otp}. This OTP is valid for 5 minutes."

        try:
            message = client.messages.create(
                body=message_body,
                from_=twilio_phone_number,
                to=phone_number
            )
            print(f"Message sent successfully! Message SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send message: {str(e)}")



if __name__ == "__main__":
    recipient_phone = input("Enter the recipient's phone number (e.g., +1234567890): ")

    otp = OTP.generate_otp()
    print(f"Generated OTP: {otp}")

    OTP.send_sms_otp('recipient phone number', otp) #Replace with recipient phone number