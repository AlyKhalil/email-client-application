import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import time
import sys

import random
import string

# def generate_random_string(length=10):
#     letters = string.ascii_lowercase
#     return ''.join(random.choice(letters) for i in range(length))

# def get_temp_email():
#     url = 'https://api.mail.tm/accounts'
#     email = f"{generate_random_string()}@mail.tm"
#     password = generate_random_string(12)
#     payload = {
#         "address": email,
#         "password": password
#     }
#     response = requests.post(url, json=payload)
#     if response.status_code == 201:
#         return response.json()
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#         return None

def login_temp_email(address, password):
    url = 'https://api.mail.tm/token'
    payload = {'address': address, 'password': password}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['token']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_mail(token):
    url = 'https://api.mail.tm/messages'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def send_email(sender_email, password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    smtp_server = 'smtp.mail.tm'
    port = 587

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")

def email_listen(token):
    try:
        while True:
            mail = get_mail(token)
            if mail and 'hydra:member' in mail:
                for msg in mail['hydra:member']:
                    print(f"From: {msg['from']['address']}")
                    print(f"Subject: {msg['subject']}")
                    print(f"Body: {msg.get('text', 'No text body available')}")
                    print("\n\n")
            time.sleep(10)  # Increased interval to avoid rate limits
    except KeyboardInterrupt:
        print("Stopping email listener...")
        sys.exit(0)

if __name__ == '__main__':
    temp_email = get_temp_email()
    if temp_email:
        print("New Email Address: ", temp_email["address"])
        print("New Password: ", temp_email['password'])
        token = login_temp_email(temp_email['address'], temp_email['password'])
        if token:
            email_listen(token)

        # token = login_temp_email("37literary@indigobook.com", ")`33B?L;n~")
        # if token:
        #     print("Logged in successfully")
        #     email_listen(token)