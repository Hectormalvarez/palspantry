import pytest
from tests.conftest import assert_state_and_message, user_states, chat_id
from src.commands.start import start


@pytest.mark.asyncio
async def test_start_new_user(mocked_objects):
    """Tests the behavior for a new, unauthenticated user"""
    mocked_update, mocked_context = mocked_objects

    await start(mocked_update, mocked_context)

    expected_message = (
        "Welcome to Pals Pantry! To use the store, please log in. Type /login to begin."
    )
    assert_state_and_message(
        mocked_context,
        expected_state="UNAUTHENTICATED",
        expected_message=expected_message,
    )


@pytest.mark.asyncio
async def test_start_returning_user(mocked_objects):
    """Tests the behavior for a returning, authenticated user."""
    user_states[chat_id] = "AUTHENTICATED"
    mocked_update, mocked_context = mocked_objects

    await start(mocked_update, mocked_context)

    expected_message = (
        "Welcome back! Here's what you can do:\n"
        "* /browse: View available products\n"
        "* /order: Place an order\n"
        "* /help: Get more information"
    )
    assert_state_and_message(
        mocked_context,
        expected_state="AUTHENTICATED",
        expected_message=expected_message,
    )
