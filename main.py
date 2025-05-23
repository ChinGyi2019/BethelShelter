from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update

import os

BOT_TOKEN = os.getenv("8074657707:AAHEKs6vUtijx3GGVod_-VlzuQmH47nvIdg")
CHANNEL_ID = os.getenv("@BethelShelter")  # Example: "@yourchannel" or "-1001234567890"

ALLOWED_WORDS = ["police", "check", "safe", "danger", "help", "emergency"]

def is_valid_text(text):
    return any(word in text.lower() for word in ALLOWED_WORDS)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Handle location pin
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude
        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        alert = f"**Location Alert**\nLat: {lat}, Lon: {lon}\n[View on Map]({maps_link})"
        await context.bot.send_message(chat_id=CHANNEL_ID, text=alert, parse_mode="Markdown")
        await message.reply_text("Location alert sent.")
        return

    # Handle text messages
    text = message.text or ""
    if is_valid_text(text):
        await context.bot.send_message(chat_id=CHANNEL_ID, text=f"**Alert:** {text}", parse_mode="Markdown")
        await message.reply_text("Your alert has been sent.")
    else:
        await message.reply_text("Please send a valid alert message or share your location.")

# Run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))
app.run_polling()
