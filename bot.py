import os
import re
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ["BOT_TOKEN"]

server = Flask(__name__)

@server.route("/")
def home():
    return "Instagram bot ishlayapti!", 200

def start_server():
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

async def convert_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    match = re.search(
        r"https?://(?:www\.)?instagram\.com/([^\s]+)",
        text,
        re.IGNORECASE
    )

    if match:
        path = match.group(1).rstrip("/")
        await update.message.reply_text(
            "https://kkclip.com/" + path
        )
    else:
        await update.message.reply_text("Instagram havolasi topilmadi.")

def main():
    threading.Thread(target=start_server, daemon=True).start()

    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link)
    )

    print("Bot ishga tushdi!")
    bot.run_polling()

if __name__ == "__main__":
    main()
