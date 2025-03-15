import pytest
from unittest.mock import AsyncMock
from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

from src.commands.help import help_command

@pytest.mark.asyncio
async def test_help_command():
    # Create mock objects for update and context
    update = AsyncMock(spec=Update)
    context = AsyncMock(spec=CallbackContext)
    context.bot.send_message = AsyncMock()
    update.effective_chat.id = 12345

    # Call the help_command function
    await help_command(update, context)

    # Assert that the bot sends the expected help message
    context.bot.send_message.assert_called_once_with(
        chat_id=12345,
        text="This is a simple bot. Available commands:\n/help - Show this help message."
    )