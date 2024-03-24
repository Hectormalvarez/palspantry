"""handles the start command, which provides options based on the user's authentication state."""

from telegram import Update
from telegram.ext import ContextTypes

from states import user_states, get_user_state, set_user_state


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message to the user based on their authentication state."""
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
