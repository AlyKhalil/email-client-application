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

    smtp_server = 'smtp.gmail.com' # smtp server for gmail
    port = 587 # port for gmail

    server = smtplib.SMTP(smtp_server, port) # create an smtp server object
    server.starttls() # start ttls connection

    server.login(sender_email, password)

    for recipient in recipients:
        msg['To'] = recipient
        server.sendmail(sender_email, recipient, msg.as_string()) # msg.as_string() converts the message from a dictionary to a string

    server.close()
