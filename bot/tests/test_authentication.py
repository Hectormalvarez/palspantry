import pytest
from .conftest import assert_state_and_message, chat_id
from src.bot_main import start, user_states, logout, login


@pytest.fixture(autouse=True)
def clear_states():
    user_states.clear()


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


@pytest.mark.asyncio
async def test_login(mocked_objects):
    """Tests the behavior of the login function."""
    mocked_update, mocked_context = mocked_objects

    await login(mocked_update, mocked_context)
    
    expected_message = "Login successful! You can now browse products and place orders."

    assert_state_and_message(
        mocked_context,
        expected_state="AUTHENTICATED",
        expected_message=expected_message,
    )


@pytest.mark.asyncio
async def test_logout(mocked_objects):
    """Tests the behavior of the logout function."""
    user_states[chat_id] = "AUTHENTICATED"
    mocked_update, mocked_context = mocked_objects

    await logout(mocked_update, mocked_context)

    expected_message = "You have been logged out."
    assert_state_and_message(
        mocked_context,
        expected_state="UNAUTHENTICATED",
        expected_message=expected_message
    )
