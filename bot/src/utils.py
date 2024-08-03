"""Utility functions for the bot."""

import logging
import os

import requests
from telegram.ext import ContextTypes


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

BOT_TOKEN = os.getenv("BOT_TOKEN")


def get_api_url():
    """Retrieves the API URL from the environment variable."""
    api_url = os.getenv("PALSPANTRY_API_URL")
    if not api_url:
        raise ValueError("PALSPANTRY_API_URL environment variable not set.")
    return api_url


def call_api(endpoint, data=None):
    """Makes a POST request to the specified API endpoint.

    Args:
        endpoint (str): The API endpoint path (e.g., '/api/token/').
        data (dict, optional): The data to send with the request.

    Returns:
        requests.Response: The response object from the API request.
    """
    url = f"{get_api_url()}{endpoint}"
    return requests.post(url, data=data, timeout=5)


async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    """Job to delete a message after a delay."""
    message = context.job.data
    chat_id = context.job.chat_id

    await context.bot.delete_message(chat_id=chat_id, message_id=message)
