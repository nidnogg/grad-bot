import os
import logging
import schedule
import time
from fetchers import check_itau
from helpers import get_users, store_user, remove_user
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# List to store subscribed user chat IDs
subscribed_users = get_users()

# Watched websites
watched_websites = [
    "https://escola.itaucultural.org.br/mediados",
    "https://escola.itaucultural.org.br/mediados_test",
]

available_commands = [
    "/start",
    "/subscribe",
    "/unsubscribe",
    "/help",
    "/scan"
]

async def start(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Assembles list of watched websites and send a message when the command /start is issued."""

    websites_message = "<b>These are the currently watched websites:</b>\n"
    for url in watched_websites:
        websites_message += f"{url}\n"

    websites_message += "\n<b>Available commands:</b>\n"
    for command in available_commands:
        websites_message += f"{command}\n"

    await update.message.reply_text(websites_message, parse_mode="HTML")


async def subscribe(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id not in subscribed_users:
        store_user(user_id)
        logger.info(f"Subscribed users: {subscribed_users}")
    await update.message.reply_text("You have subscribed to updates.")


async def unsubscribe(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id in subscribed_users:
        remove_user(user_id)
        logger.info(f"Subscribed users: {subscribed_users}")
    await update.message.reply_text("You have unsubscribed from updates.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_message = "<b>Available commands:</b>\n"
    for command in available_commands:
        help_message += f"{command}\n"

    await update.message.reply_text(help_message, parse_mode="HTML")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Scan website for user"""
    await update.message.reply_text("Scanning for updates...", )
    if check_itau():
        diffed_url = "https://escola.itaucultural.org.br/mediados"
        await update.message.reply_text(f"&#10071; <b>Updates found on {diffed_url}</b>", parse_mode="HTML")
    else:
        diffed_url = "https://escola.itaucultural.org.br/mediados"
        await update.message.reply_text(f"&#9203; <b>No updates found on {diffed_url}</b>", parse_mode="HTML")
    pass

async def send_message_to_subscribers(bot, message):
    for user_id in subscribed_users:
        await bot.send_message(chat_id=user_id, text=message)

def main():
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers setup
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("scan", scan))


    # Register a default message handler for unknown commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    async def scan_job():
        if check_itau():
            diffed_url = "https://escola.itaucultural.org.br/mediados"
            await send_message_to_subscribers(app.bot, f"Updates on {diffed_url}")
        pass

    # Starts bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    schedule.every().hour.do(scan_job)
    # Run the bot until Ctrl-C is pressed
    app.idle()
    while True:
        schedule.run_pending()
        logger.debug("Running")
        time.sleep(1)


if __name__ == "__main__":
    main()
