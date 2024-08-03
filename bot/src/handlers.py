"""This module returns the telegram application builder with handlers already added."""

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
)

from commands.logout import logout
from commands.start import start
from commands.login import login_handler
from commands.register import register_handler
from utils import BOT_TOKEN


def create_application():
    """Creates and returns a Telegram application with all the necessary handlers added."""

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    logout_handler = CommandHandler("logout", logout)

    application.add_handler(start_handler)
    application.add_handler(login_handler)
    application.add_handler(logout_handler)
    application.add_handler(register_handler)

    return application
