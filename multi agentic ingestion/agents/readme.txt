Perfect 👍 A **README.md** will help document your hackathon project so far.
Here’s a first draft tailored to what you’ve built:

---

# 🧠 Multi-Agent CRM Pipeline (Hackathon Project)

This project implements a **multi-agent pipeline** for handling customer interactions across multiple channels (Email, Telegram, and more in the future).
It integrates with **Supabase** as a backend for message storage and includes a **classification engine** to assign priority and intent to incoming messages.

---

## 🚀 Features Implemented

✅ **Base Agent** – common utilities (Supabase client, env handling).
✅ **Email Agent** – fetches unread emails (via Gmail IMAP) and stores them in Supabase.
✅ **Telegram Agent** – listens to Telegram bot messages and inserts them into Supabase.
✅ **Classification Agent** – processes messages (email + telegram), applies **sentiment + keyword analysis**, and stores classified results in a dedicated table.
✅ **Supabase Tables** – structured schema for storing messages and classified results.

---

## 🗂 Supabase Schema

* **email\_messages**

  * `id` (PK)
  * `from_email`
  * `subject`
  * `body`
  * `created_at`

* **telegram\_messages**

  * `id` (PK)
  * `from_user`
  * `body`
  * `created_at`

* **classified\_messages**

  * `id` (PK)
  * `source` (`email` / `telegram`)
  * `message_id` (FK → email\_messages.id or telegram\_messages.id)
  * `classification` (priority/intent label)
  * `created_at`

---

## ⚙️ Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd crm-agent
```

### 2. Create Virtual Environment

```bash
python -m venv hackathon_env
source hackathon_env/Scripts/activate   # Windows (Git Bash / PowerShell)
# OR
source hackathon_env/bin/activate      # Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:

* `python-telegram-bot`
* `supabase`
* `python-dotenv`
* `openai`
* `pandas`
* `textblob` or `vaderSentiment` (for polarity)

### 4. Setup `.env`

Create a `.env` file in the root:

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_key   # (optional for advanced classification)
```

---

## ▶️ Running Agents

### Run Email Agent

```bash
python agents/email_agent.py
```

Fetches unread emails and inserts them into Supabase.

### Run Telegram Agent

```bash
python agents/telegram_agent.py
```

Listens to Telegram messages and inserts them into Supabase.

### Run Classification Agent

```bash
python agents/classification_agent.py
```

Reads new messages from both sources, applies preprocessing and sentiment analysis,
and inserts results into `classified_messages`.

---

## 📊 Classification Logic

* **Polarity (Sentiment Score)**

  ```
  polarity = (positive_words - negative_words) / total_words
  ```
* **Priority Mapping**

  * `High` → Negative polarity (< -0.5) + urgency keywords (`refund`, `immediately`, `not working`)
  * `Medium` → Slightly negative or complaint
  * `Low` → Neutral or positive messages

---

## 🛠 Next Steps

* Add **Preprocessing Layer** (text cleaning, tokenization, stopword removal).
* Extend to **other channels** (WhatsApp, Voice transcripts).
* Build **Resolution Engine** (AI replies + RAG with knowledge base).
* Add **Supervisor Dashboard** (FastAPI + React + Charts).

---

📌 This README documents everything done **so far** in the hackathon project.

---

Do you want me to also generate a **requirements.txt** so your teammates can install dependencies quickly?
