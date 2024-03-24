"""handles user logout"""

from telegram import Update
from telegram.ext import ContextTypes

from states import user_states


async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Logs out a user and sets state to 'UNAUTHENTICATED'"""
    chat_id = update.effective_chat.id
    user_states[chat_id] = "UNAUTHENTICATED"

    await context.bot.send_message(chat_id=chat_id, text="You have been logged out.")
