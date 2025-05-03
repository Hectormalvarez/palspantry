import pytest
from unittest.mock import AsyncMock
from telegram import Update
from telegram.ext import CallbackContext

from src.commands.help import help_command
from ..conftest import setup_mock_update_context

@pytest.mark.asyncio
async def test_help_command(mock_update_context):
    """Test the /help command."""
    update, context = mock_update_context
    setup_mock_update_context(update, context)

    await help_command(update, context)

    context.bot.send_message.assert_called_once_with(
        chat_id=456,
        text="This is a simple bot. Available commands:\n/help - Show this help message."
    )