import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

FOOTBALL_LINK = "https://t.me/+aTRN3nmrJ7tmNTlk"
UFC_LINK = "https://t.me/+Dw281fuKJWljM2E0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "UFULO MILIONERI-ს ოფიციალური ბოტი 🚀\n"
        "მიიღე ექსკლუზიური წვდომა ფეხბურთისა და UFC-ს დახურულ არხებზე.\n\n"
        "სპონსორი: Fastoo ⚡\n\n"
        "აირჩიე სასურველი კატეგორია:"
    )
    keyboard = [
        [
            InlineKeyboardButton("⚽ ფეხბურთი", callback_data="football"),
            InlineKeyboardButton("🥊 UFC", callback_data="ufc"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "football":
        await query.message.reply_text(f"შემოგვიერთდი ფეხბურთის ჯგუფში:\n{FOOTBALL_LINK}")
    elif query.data == "ufc":
        await query.message.reply_text(f"შემოგვიერთდი UFC-ს ჯგუფში:\n{UFC_LINK}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.run_polling()

if __name__ == "__main__":
    main()
