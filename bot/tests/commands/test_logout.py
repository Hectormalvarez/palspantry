import pytest
from tests.conftest import assert_state_and_message, chat_id, user_states
from src.commands.logout import logout


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
        expected_message=expected_message,
    )
