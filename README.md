# Email Client Application

This is a Python-based email client application that allows users to log in to their Gmail account, send and receive emails, and receive desktop notifications for new emails. The application is built using the `tkinter` library for the GUI and the `smtplib` and `imaplib` libraries for sending and receiving emails, respectively. Additionally, the `plyer` library is used for desktop notifications.

## Features

- **Login Page**: Users can log in using their Gmail credentials (email and app password).
- **Main Page**:
  - **Inbox**: Displays the latest email in the inbox.
  - **Compose Email**: Allows users to compose and send emails.
  - **Refresh Inbox**: Refreshes the inbox to fetch the latest email.
  - **Logout**: Logs out the user and returns to the login page.
- **Desktop Notifications**: Notifies the user when a new email arrives.
- **Error Handling**: Provides error messages for invalid login credentials or other issues.

## Dependencies

The application requires the following Python libraries:

- `tkinter`
- `smtplib`
- `imaplib`
- `plyer`
- `email`

All dependencies except `plyer` are included with Python. To install `plyer`, run the following command in your terminal:

```bash
pip install plyer
```

## Running the Application

### Download the Code

1. Save the three Python files (`main.py`, `receiving_emails.py`, and `sending_emails.py`) in the same directory.

### Run the Application

1. Open a terminal or command prompt, navigate to the directory containing the files.
2. Run the command: `python main.py`

### Using the Application

1. **Login**: Enter your Gmail email address (without `@gmail.com`) and app password.
2. **Main Page**:
   - View the latest email in the inbox.
   - Click "Compose" to send a new email.
   - Click "Refresh" to update the inbox.
   - Click "Log Out" to return to the login page.
3. **Notifications**: If a new email arrives and it is not shown in the inbox (by pressing refresh), a desktop notification will appear.

## Enabling App Password

To use the application, you must enable an app password for your Gmail account:

1. Go to your Google Account settings.
2. Navigate to **Security > 2-Step Verification** and enable it.
3. Generate an app password under **Security > App Passwords**.
4. Use this app password to log in to the application.

## Troubleshooting

- **IMAP/SMTP Errors**: Ensure IMAP and SMTP are enabled in your Gmail settings.
- **Notification Issues**: Verify that `plyer` is installed correctly and your system supports notifications. Make sure "Do Not Disturb" is turned off.

**Note**: If you press refresh before the notification shows up, it will never show up as you are already seeing the latest email in your inbox.

## Code Documentation

### File Structure

- **main.py**: Contains the main application logic and GUI implementation.
- **receiving_emails.py**: Handles receiving and parsing emails from the inbox.
- **sending_emails.py**: Handles sending emails.

### main.py

- **GUI Class**:
  - Manages the GUI and user interactions.
  - Methods:
    - `login_page()`: Displays the login page.
    - `check_login()`: Validates user credentials.
    - `main_page()`: Displays the main page with inbox, compose, and log out options.
    - `compose()`: Opens a window to compose and send emails.
    - `send_email()`: Sends the composed email.
    - `populate_inbox()`: Displays the latest email in the inbox.
    - `refresh_inbox()`: Refreshes the inbox.
    - `check_new_emails()`: Checks for new emails and triggers notifications.
    - `logout()`: Logs out the user and returns to the login page.

### receiving_emails.py

- **email_receiver Class**:
  - Handles receiving and parsing emails from the inbox.
  - Methods:
    - `get_mail()`: Fetches the latest email from the inbox and parses its content.

### sending_emails.py

- **send_email() Function**:
  - Sends an email using the provided sender credentials, recipient, subject, and body.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
