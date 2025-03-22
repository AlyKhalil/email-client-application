import imaplib
import email
from email.header import decode_header

class email_receiver:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.last_email_id = ""
        self.is_new = True

    def get_mail(self):
        content = []
        try:
            # Connect to the server
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login(self.email, self.password)

            # mailbox
            imap.select("inbox")

            # Search for all emails in the mailbox
            status, messages = imap.search(None, "ALL")

            if status == "OK":
                # Convert first message containing space seperated byte string IDs to a list of email IDs
                email_ids = messages[0].split() # email IDs are unique byte strings that identify each email in the mailbox
            else:
                print("Failed to search emails")
                return content # return an empty list if fails

            # Fetch the latest email by ID
            status, msg_data = imap.fetch(email_ids[-1], "(RFC822)") # returns a tuple with the status and the message data
            # RFC822 is the internet message format standard for email messages

            if status != "OK":
                print("Failed to fetch latest email")
                return content  

            # Get the latest email ID and convert it to a string 
            latest_email_id = email_ids[-1].decode('utf-8')
            
            if latest_email_id == self.last_email_id:
                self.is_new = False
            else:
                self.is_new = True
                self.last_email_id = latest_email_id

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
                    else:
                        # Extract content type of email
                        content_type = msg.get_content_type()

                        # Get the email body
                        body = msg.get_payload(decode=True).decode()
                        content += [body]

            # Close the connection and logout
            imap.close()
            imap.logout()

            return content
        except imaplib.IMAP4.error as e:
            print(f"IMAP error: {e}")
            return content
