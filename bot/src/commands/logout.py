"""PalsPantry /logout command"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.utils import delete_message

logger = logging.getLogger(__name__)


async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Logs out a user"""
    user_data = context.user_data
    access_token = user_data.get("access_token")
    refresh_token = user_data.get("refresh_token")
    logger.info(
        "Log Out: Started: User %s (ID %d)",
        update.effective_user.username,
        update.effective_user.id,
    )

    # delete the /logout message sent by user
    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=update.message.message_id
    )

    if access_token or refresh_token:
        user_data.pop("access_token", None)
        user_data.pop("refresh_token", None)
        logger.info(
            "Log Out: Success: User %s (ID %d)",
            update.effective_user.username,
            update.effective_user.id,
        )
        logout_message = await update.message.reply_text(
            "You have been logged out successfully!"
        )
    else:
        logger.info(
            "Log Out: Failed: User %s (ID %d)",
            update.effective_user.username,
            update.effective_user.id,
        )
        logout_message = await update.message.reply_text(
            "You are not currently logged in."
        )
    context.job_queue.run_once(
        delete_message,
        5,
        data=logout_message.id,
        chat_id=update.effective_chat.id,
    )
