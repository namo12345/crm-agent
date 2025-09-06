import os
import re
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# === Load Supabase keys ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Preprocessing function ===
def preprocess_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # remove special chars
    text = re.sub(r"\s+", " ", text).strip()
    return text

# === Simple keyword-based classifier (can replace with ML later) ===
def classify_message(text):
    if "sale" in text or "discount" in text:
        return "Marketing"
    elif "help" in text or "support" in text:
        return "Support"
    elif "order" in text or "payment" in text:
        return "Orders"
    else:
        return "General"

# === Fetch unclassified messages from Email & Telegram ===
def fetch_messages():
    email_res = supabase.table("email_messages").select("*").execute()
    telegram_res = supabase.table("telegram_messages").select("*").execute()
    email_msgs = email_res.data
    telegram_msgs = telegram_res.data
    return email_msgs, telegram_msgs

# === Process & classify messages ===
def classify_messages():
    email_msgs, telegram_msgs = fetch_messages()
    all_msgs = []

    for msg in email_msgs:
        all_msgs.append({
            "source": "email",
            "user": msg.get("from_email", ""),
            "message": msg.get("body", "")
        })

    for msg in telegram_msgs:
        all_msgs.append({
            "source": "telegram",
            "user": msg.get("username", ""),
            "message": msg.get("message", "")
        })

    for msg in all_msgs:
        preprocessed = preprocess_text(msg["message"])
        category = classify_message(preprocessed)

        # Insert into classified_messages table
        supabase.table("classified_messages").insert({
            "source": msg["source"],
            "user": msg["user"],
            "message": msg["message"],
            "preprocessed": preprocessed,
            "category": category
        }).execute()

        print(f"✅ Classified message from {msg['user']} as {category}")

# === Run classification ===
if __name__ == "__main__":
    print("🚀 Running Classification Agent...")
    classify_messages()
    print("✅ Classification completed.")
