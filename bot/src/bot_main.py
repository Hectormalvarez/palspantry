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

# Simple in-memory user state tracking
# will be replaced with django api
user_states = {}


def get_user_state(chat_id):
    """Retrieves the authentication state of a user."""
    if chat_id in user_states:
        return user_states[chat_id]
    else:
        return "UNAUTHENTICATED"  # Default for new users


def set_user_state(chat_id, state):
    """Updates the authentication state of a user."""
    user_states[chat_id] = state


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message to the user and provides options based on their authentication state."""
    chat_id = update.effective_chat.id
    user_state = get_user_state(chat_id)  # Use the function

    if user_state == "AUTHENTICATED":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Welcome back! Here's what you can do:\n"
            "* /browse: View available products\n"
            "* /order: Place an order\n"
            "* /help: Get more information",
        )
    else:
        if chat_id not in user_states:
            set_user_state(chat_id, "UNAUTHENTICATED")

        await context.bot.send_message(
            chat_id=chat_id,
            text="Welcome to Pals Pantry! To use the store, please log in. Type /login to begin.",
        )


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authenticates a user and sets state to 'AUTHENTICATED'"""

    chat_id = update.effective_chat.id
    user_states[chat_id] = "AUTHENTICATED"

    await context.bot.send_message(
        chat_id=chat_id,
        text="Login successful! You can now browse products and place orders.",
    )


async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Logs out a user and sets state to 'UNAUTHENTICATED'"""
    chat_id = update.effective_chat.id
    user_states[chat_id] = "UNAUTHENTICATED"

    await context.bot.send_message(chat_id=chat_id, text="You have been logged out.")


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    login_handler = CommandHandler("login", login)
    logout_handler = CommandHandler("logout", logout)

    application.add_handler(start_handler)
    application.add_handler(login_handler)
    application.add_handler(logout_handler)

    application.run_polling()
