import pytest
from unittest.mock import MagicMock, AsyncMock

from src.commands.start import start, START_MESSAGE_LOGGED_IN, START_MESSAGE_LOGGED_OUT


@pytest.mark.asyncio
async def test_start_logged_in(mock_context, mock_update, mocker):
    # Mock the requests library's post method and set up mock responses
    mocker.patch(
        "src.utils.requests.post",
        side_effect=[
            MagicMock(status_code=200),  # Successful token verification
        ],
    )

    # Set up user_data to simulate a logged-in user
    mock_context.user_data["access_token"] = "some_access_token"
    mock_context.user_data["refresh_token"] = "some_refresh_token"

    await start(mock_update, mock_context)

    # Assert welcome message and log message
    mock_context.bot.send_message.assert_called_once_with(
        chat_id=12345,
        text=START_MESSAGE_LOGGED_IN,
    )
    mock_context.job_queue.run_once.assert_called_once()


@pytest.mark.asyncio
async def test_start_logged_out(mock_context, mock_update, mocker):
    # Mock the requests library's post method (so it does not call the api)
    mocker.patch("src.utils.requests.post")

    await start(mock_update, mock_context)

    # Assert login prompt and log message
    mock_context.bot.send_message.assert_called_once_with(
        chat_id=12345, text=START_MESSAGE_LOGGED_OUT
    )
    mock_context.job_queue.run_once.assert_called_once()
