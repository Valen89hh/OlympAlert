import os

TOKEN = os.environ.get("TOKEN")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

print(TELEGRAM_TOKEN, CHAT_ID, TOKEN)