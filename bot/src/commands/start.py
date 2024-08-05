"""handles the start command, which provides options based on the user's authentication state."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.utils import delete_message, check_token

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a welcome message to the user based on their authentication state.
    """
    # delete the /start message sent by user
    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=update.message.message_id
    )

    token_valid = check_token(context=context, update=update)
    if token_valid:
        start_message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Welcome back! Here's what you can do:\n"
            "* /browse: View available products\n"
            "* /order: Place an order\n"
            "* /help: Get more information",
        )
        logger.info(
            "Start: Logged In: User %s (ID %s)",
            update.effective_user.username,
            update.effective_user.id,
        )
    else:
        start_message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter the /login command to gain access to the menu",
        )
        logger.info(
            "Start: Logged Out: User %s (ID %s)",
            update.effective_user.username,
            update.effective_user.id,
        )
    context.job_queue.run_once(
        delete_message, 30, data=start_message.id, chat_id=update.effective_chat.id
    )
