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

    with smtplib.SMTP(smtp_server, port) as server:
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

def get_mail(email_address, password, last_email_id):
    try:
        # Connect to the server
        imap = imaplib.IMAP4_SSL("imap.gmail.com")

        # Login to the account
        imap.login(email_address, password)

        # Select the mailbox you want to read from
        imap.select("inbox")

        # Search for all emails in the mailbox
        status, messages = imap.search(None, "ALL")

        # Convert messages to a list of email IDs
        email_ids = messages[0].split()

        # Get the latest email ID
        latest_email_id = email_ids[-1]

        if latest_email_id != last_email_id:
            # Fetch the latest email by ID
            status, msg_data = imap.fetch(latest_email_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parse the email content
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # If the subject is encoded, decode it
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    print("Subject:", subject)
                    print("From:", from_)
                    
                    # If the email message is multipart
                    if msg.is_multipart():
                        for part in msg.walk():
                            # Extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                # Get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # Print text/plain emails and skip attachments
                                print("Body:", body)
                    else:
                        # Extract content type of email
                        content_type = msg.get_content_type()

                        # Get the email body
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            # Print only text email parts
                            print("Body:", body)
                    print("="*100)

        # Close the connection and logout
        imap.close()
        imap.logout()

        return latest_email_id
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
        return last_email_id

def email_listen(email_address, password):
    # email_address = input("Enter your email: ")
    # password = input("Enter your password: ")
    last_email_id = None

    while True:
        last_email_id = get_mail(email_address, password, last_email_id)
        time.sleep(10)  # Check for new emails every 60 seconds

def main():
    pass

if __name__ == "__main__":
    # send_email("alywalaa@gmail.com", "unkp vsig kfum garb", ["aly.khalil2026@gmail.com"], "Test Email", "This is a test email")
    email_listen("alywalaa@gmail.com", "unkp vsig kfum garb")