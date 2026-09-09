import os
from threading import Thread
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# --- 1. RENDER KEEP-ALIVE SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. TELEGRAM BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🥊 UFC Stream", callback_data='ufc')],
        [InlineKeyboardButton("⚽ Football Stream", callback_data='football')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('აირჩიე სტრიმი:', reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ufc_link = os.environ.get("UFC_LINK", "ლინკი არ არის დამატებული")
    football_link = os.environ.get("FOOTBALL_LINK", "ლინკი არ არის დამატებული")

    if query.data == 'ufc':
        await query.message.reply_text(f"🥊 UFC Live Link:\n{ufc_link}")
    elif query.data == 'football':
        await query.message.reply_text(f"⚽ Football Live Link:\n{football_link}")

# --- 3. MAIN EXECUTION ---
if __name__ == '__main__':
    # რთავს ვებ-სერვერს Render-ისთვის
    keep_alive()

    # რთავს Telegram ბოტს
    token = os.environ.get("BOT_TOKEN")
    if token:
        application = ApplicationBuilder().token(token).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CallbackQueryHandler(button_click))
        application.run_polling()
    else:
        print("Error: BOT_TOKEN is missing in Environment Variables!")
