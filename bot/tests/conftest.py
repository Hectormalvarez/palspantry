# bot/tests/conftest.py
import pytest
from unittest.mock import AsyncMock
from telegram import Update
from telegram.ext import CallbackContext

@pytest.fixture
def mock_update_context():
    """Provides a mock Update and Context for testing."""
    update = AsyncMock(spec=Update)
    context = AsyncMock(spec=CallbackContext)
    context.bot.send_message = AsyncMock()
    update.effective_user.id = 123  # Default user ID
    update.effective_chat.id = 456  # Default chat ID
    return update, context

# --- Helper function---
def setup_mock_update_context(update, context, user_data=None, text=None):
    """Sets up the mock update and context objects."""
    if user_data:
        context.user_data = user_data
    else:
        context.user_data = {}

    update.message.text = text