"""handles the start command, which provides options based on the user's authentication state."""

from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message to the user based on their authentication state."""

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome back! Here's what you can do:\n"
        "* /browse: View available products\n"
        "* /order: Place an order\n"
        "* /help: Get more information",
    )
