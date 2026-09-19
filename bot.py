import os
import logging
from threading import Thread
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# -------------------------------------------------------------
# 1. Flask ვებ-სერვერი (Render / UptimeRobot-ისთვის)
# -------------------------------------------------------------
server = Flask("")


@server.route("/")
def home():
  return "Bot is live and running!", 200


def run_flask():
  port = int(os.environ.get("PORT", 8080))
  server.run(host="0.0.0.0", port=port)


# გააშვი Flask ცალკე ნაკადში (Thread)
Thread(target=run_flask, daemon=True).start()

# -------------------------------------------------------------
# 2. ტელეგრამ ბოტის კონფიგურაცია
# -------------------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")

# შენი განახლებული ლინკები
FOOTBALL_LINK = "https://t.me/+w2IUjhPKSOw4OTY0"
UFC_LINK = "https://t.me/+w2IUjhPKSOw4OTY0"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text = (
      "UFULO MILIONERI-ს ოფიციალური ბოტი 🚀\n"
      "მიიღე ექსკლუზიური წვდომა ფეხბურთისა და UFC-ს დახურულ"
      " არხებზე.\n\n"
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

  # 1. უსაფრთხო პასუხი ღილაკზე (Timeout ერორი რომ აირიდო)
  try:
    await query.answer()
  except BadRequest as e:
    if "Query is too old" in str(e):
      pass  # ვადაგასულ მოთხოვნას უბრალოდ გაატარებს კრაშის გარეშე
    else:
      raise e

  # 2. ბოტის ლოგიკა
  if query.data == "football":
    await query.message.reply_text(
        f"შემოგვიერთდი ფეხბურთის ჯგუფში:\n{FOOTBALL_LINK}"
    )
  elif query.data == "ufc":
    await query.message.reply_text(f"შემოგვიერთდი UFC-ს ჯგუფში:\n{UFC_LINK}")


def main():
  if not TOKEN:
    print("ERROR: BOT_TOKEN Environment Variable is missing!")
    return

  app = Application.builder().token(TOKEN).build()
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(button_click))

  # drop_pending_updates=True ასუფთავებს ძველ დაგროვილ ღილაკებს ჩართვისას
  app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
  main()
