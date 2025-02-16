import smtplib
from email.mime.text import MIMEText
from config import config

def send_email(recipient_email, subject, body):
    try:
        # Set up email message
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = config.EMAIL_SENDER
        msg["To"] = recipient_email

        # Connect to SMTP server
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
        server.sendmail(config.EMAIL_SENDER, recipient_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
