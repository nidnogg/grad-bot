import os
import logging
from fetchers import check_itau, check_unirio, check_ufsc, check_ufsc_antro
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

available_commands = ["/start", "/subscribe", "/unsubscribe", "/help", "/scan"]


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
    await update.message.reply_text(
        "Scanning for updates...",
    )
    update_messages = ['&#10071; <b>Updates found on:</b>']

    if check_itau():
        diffed_url = "https://escola.itaucultural.org.br/mediados"
        update_messages.append(f"{diffed_url}")

    if check_ufsc():
        diffed_url = "https://pgcin.ufsc.br/processos-seletivos/"
        update_messages.append(f"{diffed_url}")
    
    if check_ufsc_antro():
        diffed_url = "https://ppgas.posgrad.ufsc.br/"
        update_messages.append(f"{diffed_url}")

    if check_unirio():
        diffed_url = "https://www.unirio.br/ppg-pmus/processos-seletivos-mestrado"
        update_messages.append(f"{diffed_url}")

    if len(update_messages) > 1:
        combined_message = "&#10;&#13;".join(update_messages)
        await update.message.reply_text(combined_message, parse_mode="HTML")
    else:
        await update.message.reply_text("&#9203; <b>No updates found.</b>", parse_mode="HTML")


async def send_message_to_subscribers(bot, message):
    for user_id in subscribed_users:
        await bot.send_message(chat_id=user_id, text=message, parse_mode="HTML")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)

    if not current_jobs:
        return False

    for job in current_jobs:
        job.schedule_removal()

    return True


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

    async def scan_job(context: ContextTypes.DEFAULT_TYPE):
        logger.info("Triggering scan job")
        # Checks go here
        ################################################################
        if check_itau():
            diffed_url = "https://escola.itaucultural.org.br/mediados"
            await send_message_to_subscribers(
                app.bot, f"&#10071;<b>Updates found on: </b>{diffed_url}"
            )
        # End of checks
        ################################################################
        pass
    # Schedule scan jobs
    app.job_queue.run_once(scan_job, 20)
    app.job_queue.run_repeating(scan_job, 3600)
    
    # Starts and runs the bot until Ctrl-C is pressed
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
