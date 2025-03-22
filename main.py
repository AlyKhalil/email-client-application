import tkinter as tk
import smtplib
from tkinter import messagebox
import sending_emails
import receiving_emails
from plyer import notification
import threading
import time

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.show_pass_check_state = tk.IntVar()
        self.email = ""
        self.password = ""
        self.email_receiver = None

#=======================================================================================================================================================================
# Login Page    
    def login_page(self):
        self.root.title("Login Page")
        self.root.geometry("300x350")
        
        self.Label = tk.Label(self.root, text="Login Page", font=("Arial", 24))
        self.Label.pack(pady=20)

        login_frame = tk.Frame(self.root, padx=10, pady=10)
        login_frame.pack(fill=tk.BOTH, expand=True)

        self.email_label = tk.Label(login_frame, text="Email:", font=("Arial", 16))
        self.email_label.grid(row=0, column=0, columnspan=2, sticky=tk.N, pady=(0, 10))

        self.email_entry = tk.Entry(login_frame, font=("Arial", 16), width=12)
        self.email_entry.grid(row=1, column=0, pady=(0, 10))
        self.email_entry.focus_set() # Focus the cursor on the email entry when the window opens
        self.email_entry.bind("<Return>", lambda event: self.pass_entry.focus_set()) #<Return> is the event of the Enter key

        # The lambda function is used to pass the event to the next widget, so that the user can press Enter to move to the next widget

        gmail_label = tk.Label(login_frame, text="@gmail.com", font=("Arial", 12))
        gmail_label.grid(row=1, column=1, sticky=tk.N, pady=(0, 10))

        self.pass_label = tk.Label(login_frame, text="App Password:", font=("Arial", 16), width=14)
        self.pass_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        self.pass_entry = tk.Entry(login_frame, font=("Arial", 16), show="*")
        self.pass_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        self.pass_entry.bind("<Return>", lambda event: self.check_login())

        self.show_pass_check = tk.Checkbutton(login_frame, text="Show password", font=("Arial", 8), variable=self.show_pass_check_state, command=self.toggle_show_pass)
        self.show_pass_check.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        login_but = tk.Button(login_frame, text="Login", font=("Arial", 16), command=self.check_login)
        login_but.grid(row=5, column=0, columnspan=2, pady=20)

        self.root.mainloop()

    def toggle_show_pass(self):
        if self.show_pass_check_state.get() == 1:
            self.pass_entry.config(show="") # Shows the actual password
        else:
            self.pass_entry.config(show="*") # Hides the password with "*"

    def check_login(self):
            self.email = self.email_entry.get() + "@gmail.com"
            self.password = self.pass_entry.get()

            smtp_server = 'smtp.gmail.com' # smtp server for gmail
            port = 587 # port for gmail

            try:
                server = smtplib.SMTP(smtp_server, port)
                server.starttls()
                server.login(self.email, self.password)
                server.quit() # Close the connection as we only needed to check credentials
                messagebox.showinfo("Login Successful", "You have successfully logged in!")
                self.root.destroy()  # Close the login window
                self.main_page()  # Open the main page
            except smtplib.SMTPAuthenticationError:
                messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")
                self.email_entry.delete(0, tk.END) # Clears the entries
                self.pass_entry.delete(0, tk.END)
                self.email_entry.focus_set() # Focus the cursor on the email entry, and waits for the user to enter the email again
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

# tkinter is event driven, so it waits for user inputs on gui elements to do something

#=======================================================================================================================================================================
# Main Page
    def main_page(self): 
        self.root = tk.Tk()
        self.root.title("Main Page")
        self.root.geometry("800x500")

        print(self.email, self.password)
        
        welcome_label = tk.Label(self.root, text="Main Page", font=("Arial", 24))
        welcome_label.grid(row=0, column=0, columnspan=4, pady=20)  # Centered at the top

        # Frame for Inbox Label and Refresh Button
        inbox_frame = tk.Frame(self.root)
        inbox_frame.grid(row=1, column=0, sticky=tk.W, padx=20, pady=(0, 10))

        inbox_label = tk.Label(inbox_frame, text="Inbox", font=("Arial", 24))
        inbox_label.pack(side=tk.LEFT, padx=(0, 10))  # Align to the left with some padding

        refresh_button = tk.Button(inbox_frame, text="Refresh", font=("Arial", 12), command=self.refresh_inbox)
        refresh_button.pack(side=tk.LEFT)  # Place next to the Inbox label

        send_but = tk.Button(self.root, text="Compose", font=("Arial", 16), command=self.compose)
        send_but.grid(row=0, column=3, sticky=tk.E, padx=10, pady=10)  # Top-right corner

        logout_but = tk.Button(self.root, text="Log Out", font=("Arial", 16), command=self.logout)
        logout_but.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)  # Top-left corner

        # Frame for displaying emails
        email_frame = tk.Frame(self.root, padx=10, pady=10)
        email_frame.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW)  # Expand to fill space

        # Text widget to display emails
        self.email_text = tk.Text(email_frame, font=("Arial", 12), wrap=tk.WORD)
        self.email_text.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for the Text widget
        scrollbar = tk.Scrollbar(email_frame, orient=tk.VERTICAL, command=self.email_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.email_text.config(yscrollcommand=scrollbar.set)

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        # Create an object of the email receiver class
        self.email_receiver = receiving_emails.email_receiver(self.email, self.password)

        content = self.email_receiver.get_mail()
        
        if content == []:
            self.email_text.insert(tk.END, "Inbox is Empty")
        else:
            self.populate_inbox(content)
        
        # call the email check fn for notifications
        self.check_new_emails()

        self.root.mainloop()

#=======================================================================================================================================================================
# Compose Email
    def compose(self):
        compose_window = tk.Toplevel(self.root)
        compose_window.title("Compose Email")
        compose_window.geometry("500x400")

        main_frame = tk.Frame(compose_window, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        to_label = tk.Label(main_frame, text="To:", font=("Arial", 12))
        to_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.to_entry = tk.Entry(main_frame, font=("Arial", 12), width=40)
        self.to_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 10))
        self.to_entry.focus_set()
        self.to_entry.bind("<Return>", lambda event: self.subject_entry.focus_set())

        subject_label = tk.Label(main_frame, text="Subject:", font=("Arial", 12))
        subject_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.subject_entry = tk.Entry(main_frame, font=("Arial", 12), width=40)
        self.subject_entry.grid(row=1, column=1, sticky=tk.EW, pady=(0, 10))
        self.subject_entry.bind("<Return>", lambda event: self.body_text.focus_set())

        body_label = tk.Label(main_frame, text="Body:", font=("Arial", 12))
        body_label.grid(row=2, column=0, sticky=tk.NW, pady=(0, 10))
        self.body_text = tk.Text(main_frame, font=("Arial", 12), width=40, height=10)
        self.body_text.grid(row=2, column=1, sticky=tk.EW, pady=(0, 10))
        
        # Send Button
        send_button = tk.Button(main_frame, text="Send", font=("Arial", 12), command=lambda:self.send_email(compose_window))
        send_button.grid(row=3, column=1, sticky=tk.E, pady=(10, 0))

        # Configure grid column to expand
        main_frame.columnconfigure(1, weight=1)
            
    def send_email(self, compose_window):
        to = self.to_entry.get()
        subject = self.subject_entry.get()
        body = self.body_text.get("1.0", tk.END)

        if not to or not subject or not body.strip():
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        sending_emails.send_email(self.email, self.password, [to], subject, body)

        messagebox.showinfo("Email Sent", "Your email has been sent successfully!")
        self.to_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.body_text.delete("1.0", tk.END)
        compose_window.destroy() #closes the compose window after checking

#=======================================================================================================================================================================
# Inbox
    def populate_inbox(self, content):
            self.email_text.delete("1.0", tk.END)
            self.email_text.insert(tk.END, f"From:  {content[0]}\n")
            self.email_text.insert(tk.END, f"Subject:   {content[1]}\n")
            self.email_text.insert(tk.END, f"Body:\n{content[2]}\n")
        
    def refresh_inbox(self):
        # Clear the current emails in the Text widget
        self.email_text.delete(1.0, tk.END)

        content = self.email_receiver.get_mail()
        if content == []:
            self.email_text.insert(tk.END, "Inbox is Empty")
        else:
            self.populate_inbox(content)

#=======================================================================================================================================================================
# Notification
    def check_new_emails(self):
        def check():
            while True:
                content = self.email_receiver.get_mail()
                if self.email_receiver.is_new:
                    notification.notify(
                            title="New Email",
                            message=f"From: {content[0]}\nSubject: {content[1]}",
                            timeout=10
                    )
                time.sleep(10)  # Check every 10 seconds

        threading.Thread(target=check, daemon=True).start() # Daemon threads donnot stop the main thread from exiting

#=======================================================================================================================================================================
# Logout
    def logout(self):
        self.root.destroy()
        self.email_receiver = None
        self.email = ""
        self.password = ""
        self.root = tk.Tk()
        self.show_pass_check_state = tk.IntVar()
        self.login_page()

#=======================================================================================================================================================================

if __name__ == "__main__":
    gui = GUI()
    gui.login_page()