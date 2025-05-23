from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update

import os

BOT_TOKEN = '8074657707:AAHEKs6vUtijx3GGVod_-VlzuQmH47nvIdg'
CHANNEL_ID = '@BethelShelter'  # Example: "@yourchannel" or "-1001234567890"

ALLOWED_WORDS = ["police", "check", "safe", "danger", "cid", "emergency", "operaci", "operation", "block"]
def is_valid_text(text: str) -> bool:
    """Check if the text contains any allowed alert word."""
    return any(word in text.lower() for word in ALLOWED_WORDS)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    text = message.text or ""
    caption = message.caption or ""
    full_text = (text + " " + caption).strip()

    has_location = message.location is not None
    has_text = is_valid_text(full_text)

    if has_location and has_text:
        lat = message.location.latitude
        lon = message.location.longitude
        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        alert = (
            f"**Location Alert**\n"
            f"Lat: {lat}, Lon: {lon}\n"
            f"[View on Map]({maps_link})\n\n"
            f"**Message:** {full_text}"
        )
        await context.bot.send_message(chat_id=CHANNEL_ID, text=alert, parse_mode="Markdown")
        await message.reply_text("Your location and message alert have been sent.")
        return

    if has_location:
        lat = message.location.latitude
        lon = message.location.longitude
        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        alert = (
            f"**Location Alert**\n"
            f"Lat: {lat}, Lon: {lon}\n"
            f"[View on Map]({maps_link})"
        )
        await context.bot.send_message(chat_id=CHANNEL_ID, text=alert, parse_mode="Markdown")
        await message.reply_text("Location alert sent.")
        return

    if has_text:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=f"**Alert:** {full_text}", parse_mode="Markdown")
        await message.reply_text("Your alert has been sent.")
        return

    await message.reply_text("Please send a valid alert message or share your location.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("Bot is running...")
    app.run_polling()
# def is_valid_text(text):
#     return any(word in text.lower() for word in ALLOWED_WORDS)

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message = update.message

#     # Handle location pin
#     if message.location:
#         lat = message.location.latitude
#         lon = message.location.longitude
#         maps_link = f"https://www.google.com/maps?q={lat},{lon}"
#         alert = f"**Location Alert**\nLat: {lat}, Lon: {lon}\n[View on Map]({maps_link})"
#         await context.bot.send_message(chat_id=CHANNEL_ID, text=alert, parse_mode="Markdown")
#         await message.reply_text("Location alert sent.")
#         return

#     # Handle text messages
#     text = message.text or ""
#     if is_valid_text(text):
#         await context.bot.send_message(chat_id=CHANNEL_ID, text=f"**Alert:** {text}", parse_mode="Markdown")
#         await message.reply_text("Your alert has been sent.")
#     else:
#         await message.reply_text("Please send a valid alert message or share your location.")

# # Run the bot
# app = ApplicationBuilder().token(BOT_TOKEN).build()
# app.add_handler(MessageHandler(filters.ALL, handle_message))
# app.run_polling()
