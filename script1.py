from dotenv import load_dotenv
import imaplib 
import email
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve email credentials and server details from environment variables
EMAIL_ADDRESS = os.getenv("email_address")
EMAIL_PASSWORD = os.getenv("password")
IMAP_SERVER = os.getenv("imap_server")

# Establish a secure connection to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)

# Log in to your email account using the credentials
mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

# Select the "Inbox" folder to search for emails
mail.select("Inbox")
TARGET_FOLDER = "uhCollege"  # Define the target folder to move emails to

# Search for emails containing the test "uh.edu"
status, messageIDs = mail.search(None, '(BODY "uh.edu")')

# Loop through each email ID retrieved from the search
for messageID in messageIDs[0].split():

    # Fetch the email by its ID
    status, emailAddress = mail.fetch(messageID, "(RFC822)")

    if status != "OK":
        print(f"Failed to fetch email with ID {messageID.decode()}.")
        continue

    # Parse the email content to get the message object
    msg = email.message_from_bytes(emailAddress[0][1])

    # Extract and print the subject and sender of the email
    subject = msg.get("subject")
    from_ = msg.get("from")
    to = msg.get("to")

    print(f"Subject: {subject}")
    print(f"From: {from_}")
    print(f'To: {to}')

    # Copy the email to the "uhCollege" folder
    status, response = mail.copy(messageID, TARGET_FOLDER)

    if status != "OK":
        print(f"Failed to copy email with ID {messageID.decode()} to {TARGET_FOLDER}.")
        continue
    
    # Uncomment the line below if you want to delete the email from the Inbox after copying
    # mail.store(messageID, '+FLAGS', '\\Deleted')

# Uncomment the line below if you want to permanently delete the emails from the Inbox
# mail.expunge()

# Log out and close the connection to the email server
mail.logout()




