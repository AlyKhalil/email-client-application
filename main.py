import tkinter as tk
import smtplib
from tkinter import messagebox
import sending_emails
import receiving_emails

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.show_pass_check_state = tk.IntVar()
        self.login_successful = False
        self.email = ""
        self.password = ""

    def login(self):
        self.root.title("Login Page")
        self.root.geometry("300x350")
        
        self.Label = tk.Label(self.root, text="Login Page", font=("Arial", 24))
        self.Label.pack(pady=20)
        
        self.email_label = tk.Label(self.root, text="Email:", font=("Arial", 16))
        self.email_label.pack(pady=10)

        self.email_entry = tk.Entry(self.root, font=("Arial", 16))
        self.email_entry.pack() 
        self.email_entry.focus_set()

        self.pass_label = tk.Label(self.root, text="Password:", font=("Arial", 16))
        self.pass_label.pack(pady=10)

        self.pass_entry = tk.Entry(self.root, font=("Arial", 16), show="*")
        self.pass_entry.pack()

        self.show_pass_check = tk.Checkbutton(self.root, text="Show password", font=("Arial", 8), variable=self.show_pass_check_state, command=self.toggle_show_pass)
        self.show_pass_check.pack()

        login_but = tk.Button(self.root, text="Login", font=("Arial", 16), command=self.check_login)
        login_but.pack(pady=20)
        
        self.root.mainloop()

    def toggle_show_pass(self):
        if self.show_pass_check_state.get() == 1:
            self.pass_entry.config(show="")
        else:
            self.pass_entry.config(show="*")

    def check_login(self):
        self.email = self.email_entry.get()
        self.password = self.pass_entry.get()

        smtp_server = 'smtp.gmail.com'
        port = 587

        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(self.email, self.password)
            server.quit()
            messagebox.showinfo("Login Successful", "You have successfully logged in!")
            self.login_successful = True
            self.root.destroy()  # Close the login window
            self.main_page()  # Open the main page
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")
            self.email_entry.delete(0, tk.END)
            self.pass_entry.delete(0, tk.END)
            self.email_entry.focus_set()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

#tkinter is an event-driven GUI framework. This means the program waits for user interaction (e.g., clicking a button, typing in a field)
# and responds to those events. When the login fails, the program does not terminate because 
# it is still waiting for further user input (e.g., the user retyping their credentials and clicking the "Login" button again).

    def compose(self):
        compose_window = tk.Toplevel(self.root)
        compose_window.title("Compose Email")
        compose_window.geometry("500x400")

        # Use a frame for better organization
        main_frame = tk.Frame(compose_window, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # To: Label and Entry
        to_label = tk.Label(main_frame, text="To:", font=("Arial", 12))
        to_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.to_entry = tk.Entry(main_frame, font=("Arial", 12), width=40)
        self.to_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 10))

        # Subject: Label and Entry
        subject_label = tk.Label(main_frame, text="Subject:", font=("Arial", 12))
        subject_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.subject_entry = tk.Entry(main_frame, font=("Arial", 12), width=40)
        self.subject_entry.grid(row=1, column=1, sticky=tk.EW, pady=(0, 10))

        # Body: Label and Text Widget
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


    def main_page(self):
        self.root = tk.Tk()
        self.root.title("Main Page")
        self.root.geometry("800x500")
        
        # Welcome Label
        welcome_label = tk.Label(self.root, text="Welcome to Main Page", font=("Arial", 24))
        welcome_label.grid(row=0, column=0, columnspan=4, pady=20)  # Centered at the top

        # Frame for Inbox Label and Refresh Button
        inbox_frame = tk.Frame(self.root)
        inbox_frame.grid(row=1, column=0, sticky=tk.W, padx=20, pady=(0, 10))

        # Inbox Label
        inbox_label = tk.Label(inbox_frame, text="Inbox", font=("Arial", 24))
        inbox_label.pack(side=tk.LEFT, padx=(0, 10))  # Align to the left with some padding

        # Refresh Button
        refresh_button = tk.Button(inbox_frame, text="Refresh", font=("Arial", 12), command=self.refresh_inbox)
        refresh_button.pack(side=tk.LEFT)  # Place next to the Inbox label

        # Compose Button
        send_but = tk.Button(self.root, text="Compose", font=("Arial", 16), command=self.compose)
        send_but.grid(row=0, column=3, sticky=tk.E, padx=10, pady=10)  # Top-right corner

        # Frame for displaying emails
        email_frame = tk.Frame(self.root, padx=10, pady=10)
        email_frame.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW)  # Expand to fill space

        # Listbox to display emails
        self.email_listbox = tk.Listbox(email_frame, font=("Arial", 12), selectmode=tk.SINGLE)
        self.email_listbox.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(email_frame, orient=tk.VERTICAL, command=self.email_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.email_listbox.config(yscrollcommand=scrollbar.set)

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        content = receiving_emails.get_mail(self.email, self.password)
        if content == []:
            self.email_listbox.insert(tk.END, f"    Inbox is Empty")
        else:
            self.populate_inbox(content)
        
        self.root.mainloop()

    def populate_inbox(self, content):
        self.email_listbox.insert(tk.END, f"From: {content[0]}")
        self.email_listbox.insert(tk.END, f"Subject: {content[1]}") 
        self.email_listbox.insert(tk.END, f"Body: ")
        self.email_listbox.insert(tk.END, content[2])

    def refresh_inbox(self):
        # Clear the current emails in the Listbox
        self.email_listbox.delete(0, tk.END)

        content = receiving_emails.get_mail(self.email, self.password)
        self.populate_inbox(content)
    

if __name__ == "__main__":
    gui = GUI()
    # gui.login()
    gui.main_page()