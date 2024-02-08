import requests
import os
import logging
import schedule
import time
from fetchers import check_itau
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# List to store subscribed user chat IDs
subscribed_users = []

def start(update, context):
    update.message.reply_text("Welcome to the Subscription Bot! Send /subscribe to subscribe to updates.")

def subscribe(update, context):
    user_id = update.message.chat_id
    if user_id not in subscribed_users:
        subscribed_users.append(user_id)
    update.message.reply_text("You have subscribed to updates.")

def unsubscribe(update, context):
    user_id = update.message.chat_id
    if user_id in subscribed_users:
        subscribed_users.remove(user_id)
    update.message.reply_text("You have unsubscribed from updates.")

def echo(update, context):
    update.message.reply_text("Unknown command. Send /start to begin.")

def send_message_to_subscribers(bot, message):
    for user_id in subscribed_users:
        bot.send_message(chat_id=user_id, text=message)
    
def main():
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # Register a default message handler for unknown commands
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Run the check_itau function every hour (adjust interval as needed)
    # You can use a scheduler library like `schedule` for more advanced scheduling
    def scan_job():
        if check_itau():
            diffed_url = "https://escola.itaucultural.org.br/mediados"
            send_message_to_subscribers(updater.bot, f"Updates on {diffed_url}")
            # Send a message to all subscribed users about the update
            pass  # Implement sending message to subscribers

    # Start the Bot
    updater.start_polling()
    schedule.every().hour.do(scan_job) 
    updater.idle()
    while True:
        schedule.run_pending()
        time.sleep(1)
        
    # Run the bot until you press Ctrl-C

if __name__ == '__main__':
    main()



