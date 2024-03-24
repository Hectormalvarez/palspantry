import pytest
from unittest.mock import AsyncMock

from src.bot_main import user_states

chat_id = 12345


# Fixture for creating mocked update and context objects
@pytest.fixture
def mocked_objects():
    # Create a mocked update & context object
    # Set the effective chat ID on the mocked update object
    mocked_update = AsyncMock()
    mocked_update.effective_chat.id = chat_id
    mocked_context = AsyncMock()

    # Return the mocked update and context objects as a tuple
    return mocked_update, mocked_context


# Fixture to clear the user_states dictionary before each test case
@pytest.fixture(autouse=True)
def clear_states():
    from src.bot_main import user_states

    # Clear the user_states dictionary
    user_states.clear()


# Helper function to assert the user state and the message sent by the bot
def assert_state_and_message(
    mocked_context, expected_state, expected_message
):    
    # Assert that the user state matches the expected state
    assert user_states[chat_id] == expected_state
    
    # Assert that the send_message method was called with the expected chat ID and message
    mocked_context.bot.send_message.assert_awaited_once_with(
        chat_id=chat_id, text=expected_message
    )
