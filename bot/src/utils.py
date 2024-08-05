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


def call_api(endpoint, data=None, headers=None):
    """Makes a POST request to the specified API endpoint."""
    url = f"{get_api_url()}{endpoint}"
    return requests.post(url, data=data, headers=headers, timeout=5)


async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    """Job to delete a message after a delay."""
    message = context.job.data
    chat_id = context.job.chat_id

    await context.bot.delete_message(chat_id=chat_id, message_id=message)


def check_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Checks the validity of a user's access token and handles potential refresh.

    Args:
        context: The Telegram CallbackContext object.

    Returns:
        bool: True if the token is valid or was successfully refreshed, False otherwise.
    """
    user_data = context.user_data
    access_token = user_data.get("access_token")
    refresh_token = user_data.get("refresh_token")

    logging.info(
        "check_token: Started: User %s (ID %d)",
        update.effective_user.username,
        update.effective_user.id,
    )

    if access_token:
        try:
            logging.info(
                "check_token: in progress: User %s (ID %d) calling verify api endpoint",
                update.effective_user.username,
                update.effective_user.id,
            )
            response = call_api("/api/token/verify/", data={"token": access_token})
            if response.status_code == 200:
                logging.info(
                    "check_token: Success: User %s (ID %d) access token valid",
                    update.effective_user.username,
                    update.effective_user.id,
                )
                return True  # Token is valid
        except InvalidToken:
            pass  # Access Token is invalid

        # Try refreshing the token if it's invalid
        if refresh_token:
            data = {"refresh": refresh_token}
            try:
                logging.info(
                    "check_token: in progress: User %s (ID %d) calling refresh api endpoint",
                    update.effective_user.username,
                    update.effective_user.id,
                )
                refresh_response = call_api("/api/token/refresh/", data=data)
                if refresh_response.status_code == 200:
                    logging.info(
                        "check_token: sucess: User %s (ID %d) refresh token valid",
                        update.effective_user.username,
                        update.effective_user.id,
                    )
                    new_tokens = refresh_response.json()
                    user_data["access_token"] = new_tokens["access"]
                    return True  # Refresh successful
            except TokenError:
                return False  # Refresh Failed

        logging.info(
            "check_token: failed: User %s (ID %d) unable to verify tokens",
            update.effective_user.username,
            update.effective_user.id,
        )

    # If the access token is invalid and refreshing failed, return False
    return False
