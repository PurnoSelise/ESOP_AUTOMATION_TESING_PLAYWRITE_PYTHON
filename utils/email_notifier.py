import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailNotifier:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "seliseautomation@gmail.com"
        self.sender_password = "ztoyfrfehvwqcqhz"
        self.recipient_email = "purna.ghosh@selisegroup.com"
    
    def send_test_result(self, test_name, result, environment="stage", tester="Purno"):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"Test Result: {test_name}"
            
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            body = f"""
Test Case: {test_name}
Date: {current_date}
Environment: {environment}
Test By: {tester}
Result: {result}

This is an automated test result notification.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.recipient_email, text)
            server.quit()
            
            print(f"✅ Email sent successfully to {self.recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False
