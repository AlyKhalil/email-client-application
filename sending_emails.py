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

    server = smtp_server.smtplib.SMTP(smtp_server, port)
    server.starttls()

    while True:
        try:
            server.login(sender_email, password)
            break
        except:
            print("Login failed. Please try again.")
            print()
            sender_email = input("Enter your email: ")
            password = input("Enter your password: ") 

    for recipient in recipients:
        msg['To'] = recipient
        server.sendmail(sender_email, recipient, msg.as_string())
    print("Email(s) sent successfully.")

    server.close()


def main():
    pass

if __name__ == "__main__":
    send_email("alywalaa@gmail.com", "unkp vsig kfum garb", ["aly.khalil2026@gmail.com"], "Test Email", "This is a test email")
    