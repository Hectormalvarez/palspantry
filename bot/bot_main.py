import logging
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provides a welcome message and initial guidance for the Pals Pantry bot."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to Pals Pantry! Your friendly neighborhood grocery bot. 😊\n\n"
        "Here's what I can help you with:\n"
        "* Type /help to see a list of commands\n"
        "* Type /browse to view available products\n"
        "* Want to place an order? Type /order",
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
