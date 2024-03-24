import pytest
from tests.conftest import assert_state_and_message
from src.commands.login import login


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
