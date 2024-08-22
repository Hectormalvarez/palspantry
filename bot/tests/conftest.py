from unittest.mock import AsyncMock, MagicMock

import pytest
from telegram import Update
from telegram.ext import ContextTypes


@pytest.fixture
def mock_context():
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot = AsyncMock()
    context.bot.send_message = AsyncMock()
    context.bot.edit_message_text = AsyncMock()
    context.bot.delete_message = AsyncMock()
    context.job_queue.run_once = MagicMock()

    return context


@pytest.fixture
def mock_update():
    update = AsyncMock(spec=Update)
    update.effective_chat.id = 12345
    update.effective_user.id = 98765
    update.effective_user.username = "testuser"
    update.effective_message.delete = AsyncMock()
    update.message.message_id = 67890
    update.message.reply_text = AsyncMock()

    return update
