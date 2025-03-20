import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import requests
import time

def send_email(sender_email, password, recipients, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    smtp_server = 'smtp.gmail.com'
    port = 587

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()

    server.login(sender_email, password)

    for recipient in recipients:
        msg['To'] = recipient
        server.sendmail(sender_email, recipient, msg.as_string())

    server.close()


if __name__ == "__main__":
    # send_email("alywalaa@gmail.com", "unkp vsig kfum garb", ["aly.khalil2026@gmail.com"], "Test Email", "This is a test email")
    pass
    