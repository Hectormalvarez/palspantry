"""Palspantry /login command"""

import logging

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.utils import get_api_url, check_token, delete_message

LOGIN_USERNAME, LOGIN_PASSWORD = range(2)
logger = logging.getLogger(__name__)


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starts the login process by asking for the user's username.
    """
    logger.info(
        "Login: Started: User %s (ID %d)",
        update.effective_user.username,
        update.effective_user.id,
    )

    # delete the /login message sent by user
    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=update.message.message_id
    )

    token_valid = check_token(context=context, update=update)
    if token_valid:
        logger.info(
            "Login: Cancelled: Logged In: User %s (ID %d)",
            update.effective_user.username,
            update.effective_user.id,
        )
        welcome_message = await update.message.reply_text(
            """
        Welcome to the PalsPantry!
        You are already logged in!
        """
        )
        context.job_queue.run_once(
            delete_message,
            3,
            data=welcome_message.id,
            chat_id=update.effective_chat.id,
        )
        return ConversationHandler.END

    welcome_message = await update.message.reply_text(
        """
        Welcome to the login process!
        Please enter your username:
        """
    )
    # save welcome message id for text updates on same bubble
    context.user_data["login_message_id"] = welcome_message.message_id

    return LOGIN_USERNAME


async def login_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's username input and asks for their password.
    """
    username = update.message.text
    context.user_data["username"] = username

    # delete username
    await update.effective_message.delete()

    logger.info(
        "Login: In Progress: entered username: %s: User %s (ID %d)",
        username,
        update.effective_user.username,
        update.effective_user.id,
    )

    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=context.user_data["login_message_id"],
        text="Please enter your password:",
    )

    return LOGIN_PASSWORD


async def login_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the user's password input and attempts to log in."""
    password = update.message.text
    username = context.user_data["username"]

    # delete password message
    await update.effective_message.delete()
    logger.info(
        "Login: In Progress: User %s (ID %d): entered password",
        update.effective_user.username,
        update.effective_user.id,
    )

    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=context.user_data["login_message_id"],
        text="attempting login...",
    )
    logger.info(
        "Login: In Progress: User %s (ID %d): calling /token api",
        update.effective_user.username,
        update.effective_user.id,
    )
    response = requests.post(
        f"{get_api_url()}/api/token/", data={"username": username, "password": password}
    )

    if response.status_code == 200:
        data = response.json()
        context.user_data["access_token"] = data["access"]
        context.user_data["refresh_token"] = data["refresh"]

        logger.info(
            "Login: Success: User %s (ID %s)",
            username,
            update.effective_user.id,
        )
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["login_message_id"],
            text="Login successful!",
        )
    else:
        logger.warning(
            "Login: Failed: User %s (ID %s)",
            username,
            update.effective_user.id,
        )
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["login_message_id"],
            text="Invalid credentials. Please try again.",
        )

    # delete /login conversation message
    context.job_queue.run_once(
        delete_message,
        3,
        data=context.user_data["login_message_id"],
        chat_id=update.effective_chat.id,
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels the login process and clears the user's data.
    """
    user_data = context.user_data
    username = context.user_data["username"]

    if user_data:
        user_data.clear()

    logger.warning(
        "Login: Canceled: User %s (ID %s)",
        username,
        update.effective_user.id,
    )
    await update.message.reply_text("Login canceled.")

    return ConversationHandler.END


async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    """Job to delete a message after a delay."""
    message = context.job.data
    chat_id = context.job.chat_id

    await context.bot.delete_message(chat_id=chat_id, message_id=message)


login_handler = ConversationHandler(
    entry_points=[CommandHandler("login", login)],
    states={
        LOGIN_USERNAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, login_username)
        ],
        LOGIN_PASSWORD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, login_password)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
