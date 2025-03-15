import tkinter as tk
import smtplib
from tkinter import messagebox

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.show_pass_check_state = tk.IntVar()
        self.login_successful = False

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
        email = self.email_entry.get()
        password = self.pass_entry.get()

        smtp_server = 'smtp.gmail.com'
        port = 587

        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(email, password)
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

    def main_page(self):
        self.root.title("Main Page")
        self.root.geometry("800x500")
        
        welcome_label = tk.Label(self.root, text="Welcome to Main Page", font=("Arial", 24))
        welcome_label.pack()
        
        # Add more widgets and functionality here for sending/receiving emails

        send_but = tk.Button(self.root, text="Send an Email", font=("Arial", 16))
        send_but.place(x=620, y=20)
        
        self.root.mainloop()

def main():
    gui = GUI()
    gui.login()
    gui.main_page()

if __name__ == "__main__":
    main()