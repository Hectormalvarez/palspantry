"""handles user login"""

from telegram import Update
from telegram.ext import ContextTypes

from states import user_states


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authenticates a user and sets state to 'AUTHENTICATED'"""

    chat_id = update.effective_chat.id
    user_states[chat_id] = "AUTHENTICATED"

    await context.bot.send_message(
        chat_id=chat_id,
        text="Login successful! You can now browse products and place orders.",
    )
