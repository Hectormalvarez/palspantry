from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays a help message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="This is a simple bot. Available commands:\n/help - Show this help message."
    )