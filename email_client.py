import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    smtp_server = 'smtp.gmail.com' # smtp server address for gmail
    port = 587 # port for gmail

    try:
        with smtplib.SMTP(smtp_server, port) as smtp_server:
            pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    pass    
