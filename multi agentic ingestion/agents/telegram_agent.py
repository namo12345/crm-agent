import os
from dotenv import load_dotenv
from supabase import create_client, Client
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# === Load environment variables ===
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN not found in .env file!")

# === Initialize Supabase client ===
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Handler for incoming messages ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return  # Ignore non-text messages

    try:
        message = update.message.text
        user = update.message.from_user
        username = user.username if user.username else ""
        user_id = user.id

        # Insert message into Supabase
        supabase.table("telegram_messages").insert({
            "user_id": user_id,
            "username": username,
            "message": message
        }).execute()

        print(f"✅ Saved message from {username} ({user_id}): {message}")

    except Exception as e:
        print(f"❌ Error saving message: {e}")

# === Build Telegram Bot Application ===
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Add handler for incoming text messages
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# === Run Bot ===
print("🚀 Telegram Agent running...")
app.run_polling(poll_interval=3)  # poll every 3 seconds
