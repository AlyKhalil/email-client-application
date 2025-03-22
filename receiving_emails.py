import imaplib
import email
from email.header import decode_header
import time

def get_mail(email_address, password):
    content = []
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

                content += [from_, subject]

                # print("Subject:", subject)
                # print("From:", from_)
                
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
                            content += [body]
                            # print("Body:", body)
                else:
                    # Extract content type of email
                    content_type = msg.get_content_type()

                    # Get the email body
                    body = msg.get_payload(decode=True).decode()
                    # if content_type == "text/plain":
                    #     # Print only text email parts
                    #     print("Body:", body)
                    content += [body]
                # print("="*100)

        # Close the connection and logout
        imap.close()
        imap.logout()

        return content
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
        return content
