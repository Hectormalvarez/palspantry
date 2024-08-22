"""handles the start command, which provides options based on the user's authentication state."""

import logging

from telegram import Update, Message
from telegram.ext import ContextTypes

from src.utils import delete_message, check_token

logger = logging.getLogger(__name__)
START_MESSAGE_LOGGED_OUT = """
Please enter the /login command to gain access to the menu
"""
START_MESSAGE_LOGGED_IN = """
Welcome back! Here's what you can do:
* /browse: View available products
* /order: Place an order
* /help: Get more information
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a welcome message to the user based on their authentication state.
    """
    # delete the /start message sent by user
    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=update.message.message_id
    )

    has_tokens = context.user_data.get("access_token") or context.user_data.get(
        "refresh_token"
    ) 
    
    if has_tokens and check_token(context=context, update=update):
        start_message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=START_MESSAGE_LOGGED_IN,
        )
        context.job_queue.run_once(
            delete_message,
            10,
            data=start_message.id,
            chat_id=update.effective_chat.id,
        )
        logger.info(
            "Start: Logged In: User %s (ID %s)",
            update.effective_user.username,
            update.effective_user.id,
        )
    else:
        start_message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=START_MESSAGE_LOGGED_OUT,
        )
        context.job_queue.run_once(
            delete_message, 10, data=start_message.id, chat_id=update.effective_chat.id
        )
        logger.info(
            "Start: Logged Out: User %s (ID %s)",
            update.effective_user.username,
            update.effective_user.id,
        )
