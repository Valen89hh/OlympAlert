from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID
print(TELEGRAM_TOKEN)
bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(message: str):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"[ERROR Telegram] {e}")
