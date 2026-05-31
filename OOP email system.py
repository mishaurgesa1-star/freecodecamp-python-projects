import datetime


# ==========================================
# Email Class
# Represents a single email message
# ==========================================
class Email:
    def __init__(self, sender, receiver, subject, body):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.timestamp = datetime.datetime.now()
        self.read = False

    # Mark an email as read
    def mark_as_read(self):
        self.read = True

    # Display the full contents of an email
    def display_full_email(self):
        self.mark_as_read()

        print("\n--- Email ---")
        print(f"From: {self.sender.name}")
        print(f"To: {self.receiver.name}")
        print(f"Subject: {self.subject}")
        print(f"Received: {self.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print(f"Body: {self.body}")
        print("-------------\n")

    # String representation of an email
    def __str__(self):
        status = "Read" if self.read else "Unread"

        return (
            f"[{status}] "
            f"From: {self.sender.name} | "
            f"Subject: {self.subject} | "
            f"Time: {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
        )


# ==========================================
# Inbox Class
# Stores and manages a user's emails
# ==========================================
class Inbox:
    def __init__(self):
        self.emails = []

    # Add a received email to the inbox
    def receive_email(self, email):
        self.emails.append(email)

    # Display all emails in the inbox
    def list_emails(self):
        if not self.emails:
            print("Your inbox is empty.\n")
            return

        print("\nYour Emails:")

        for index, email in enumerate(self.emails, start=1):
            print(f"{index}. {email}")

    # Read an email by its number
    def read_email(self, index):
        if not self.emails:
            print("Inbox is empty.\n")
            return

        actual_index = index - 1

        if actual_index < 0 or actual_index >= len(self.emails):
            print("Invalid email number.\n")
            return

        self.emails[actual_index].display_full_email()

    # Delete an email by its number
    def delete_email(self, index):
        if not self.emails:
            print("Inbox is empty.\n")
            return

        actual_index = index - 1

        if actual_index < 0 or actual_index >= len(self.emails):
            print("Invalid email number.\n")
            return

        deleted_email = self.emails.pop(actual_index)

        print(
            f"Deleted email: '{deleted_email.subject}'\n"
        )


# ==========================================
# User Class
# Represents a user who can send and
# receive emails
# ==========================================
class User:
    def __init__(self, name):
        self.name = name
        self.inbox = Inbox()

    # Send an email to another user
    def send_email(self, receiver, subject, body):
        email = Email(
            sender=self,
            receiver=receiver,
            subject=subject,
            body=body
        )

        receiver.inbox.receive_email(email)

        print(
            f"Email sent from {self.name} "
            f"to {receiver.name}!\n"
        )

    # Display the user's inbox
    def check_inbox(self):
        print(f"\n{self.name}'s Inbox:")
        self.inbox.list_emails()

    # Read an email
    def read_email(self, index):
        self.inbox.read_email(index)

    # Delete an email
    def delete_email(self, index):
        self.inbox.delete_email(index)


# ==========================================
# Main Program
# Demonstrates the email system
# ==========================================
def main():

    # Create users
    tory = User("Tory")
    ramy = User("Ramy")

    # Send emails
    tory.send_email(
        ramy,
        "Hello",
        "Hi Ramy, just saying hello!"
    )

    ramy.send_email(
        tory,
        "Re: Hello",
        "Hi Tory, hope you are fine."
    )

    # View inbox
    ramy.check_inbox()

    # Read first email
    ramy.read_email(1)

    # Delete first email
    ramy.delete_email(1)

    # View inbox again
    ramy.check_inbox()


# Run the program
if __name__ == "__main__":
    main()