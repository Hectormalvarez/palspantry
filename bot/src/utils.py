"""Utility functions for the bot."""

import logging
import os

import requests
from telegram import Update
from telegram.ext import ContextTypes
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING) 

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("PALSPANTRY_API_URL")


def get_api_url():
    """Retrieves the API URL from the environment variable."""
    if not API_URL:
        raise ValueError("PALSPANTRY_API_URL environment variable not set.")
    return API_URL


async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    """Job to delete a message after a delay."""
    message = context.job.data
    chat_id = context.job.chat_id

    await context.bot.delete_message(chat_id=chat_id, message_id=message)


def check_token(update: Update, context: ContextTypes.DEFAULT_TYPE, requests_lib=requests):
    """
    Checks the validity of a user's access token and handles potential refresh.

    Args:
        context: The Telegram CallbackContext object.
        requests_lib: The requests library to use for making API requests.

    Returns:
        bool: True if the token is valid or was successfully refreshed, False otherwise.
    """
    user_data = context.user_data
    access_token = user_data.get("access_token")
    refresh_token = user_data.get("refresh_token")

    if access_token:
        try:
            response = requests_lib.post(
                f"{get_api_url()}/api/token/verify/", data={"token": access_token}
            ) 
            if response.status_code == 200:
                # Token is valid
                return True
        except InvalidToken:
            # Access Token is invalid
            pass
        # Try refreshing the token if it's invalid
        if refresh_token:
            try:
                refresh_response = requests_lib.post(
                    f"{get_api_url()}/api/token/refresh/", data={"refresh": refresh_token}
                )

                if refresh_response.status_code == 200:
                    new_tokens = refresh_response.json()
                    user_data["access_token"] = new_tokens["access"]
                    return True  # Refresh successful
            except TokenError:
                return False  # Refresh Failed
    # If the access token is invalid and refreshing failed, return False
    return False
