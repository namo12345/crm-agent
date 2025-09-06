import imaplib
import email
from email.header import decode_header
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# === Initialize Supabase client ===
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Connect to Gmail IMAP server ===
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(EMAIL_USER, EMAIL_PASS)
imap.select("inbox")

# === Search for unread emails ===
status, messages = imap.search(None, '(UNSEEN)')
email_ids = messages[0].split()

# Limit to first 5 emails for testing
email_ids = email_ids[:5]

print(f"Found {len(email_ids)} unread emails. Processing...")

for e_id in email_ids:
    try:
        _, msg_data = imap.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Decode subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                
                from_ = msg.get("From")
                
                # Get email body (plain text only)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                
                # Insert into Supabase
                try:
                    supabase.table("emails").insert({
                        "sender": from_,
                        "subject": subject,
                        "body": body
                    }).execute()
                    print(f"Inserted email from {from_} - {subject}")
                except Exception as e:
                    print(f"Supabase insert failed for email from {from_}: {e}")
    except Exception as e:
        print(f"Error processing email {e_id}: {e}")

# Logout
imap.logout()
print("Email Agent finished processing emails.")
