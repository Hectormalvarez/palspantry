from unittest.mock import MagicMock

from telegram.ext import ConversationHandler
import pytest

from src.commands.login import (
    LOGIN_USERNAME,
    LOGIN_PASSWORD,
    login,
    login_username,
    login_already_logged_in_response,
    login_initiated_response,
    login_username_response,
)


@pytest.mark.asyncio
async def test_login_already_logged_in(mock_context, mock_update, mocker):
    mocker.patch(
        "src.utils.requests.post",
        side_effect=[
            MagicMock(status_code=200),  # successful token verification
        ],
    )
    # set up user_data to simulate a logged-in user (tokens exist)
    mock_context.user_data["access_token"] = "some_access_token"
    mock_context.user_data["refresh_token"] = "some_refresh_token"

    result = await login(mock_update, mock_context)

    # check that message sent by user is deleted
    mock_context.bot.delete_message.assert_called_once_with(
        chat_id=mock_update.effective_chat.id, message_id=mock_update.message.message_id
    )
    # welcome_text_logged_in message was sent to user
    mock_update.message.reply_text.assert_called_once_with(login_already_logged_in_response)
    # message sent to user was added to the queue for deletion
    mock_context.job_queue.run_once.assert_called_once()  
    # handler ended the converstation since user is already logged in
    assert result == ConversationHandler.END


@pytest.mark.asyncio
async def test_login_not_logged_in_initiated(mock_context, mock_update, mocker):
    mocker.patch(
        "src.utils.requests.post",
        side_effect=[
            MagicMock(status_code=401),  # failed token verification
            MagicMock(
                status_code=400
            ),  # Second call (token refresh fails, if it happens)
        ],
    )

    result = await login(mock_update, mock_context)

    # message sent by user is deleted
    mock_context.bot.delete_message.assert_called_once_with(
        chat_id=mock_update.effective_chat.id, message_id=mock_update.message.message_id
    )
    # welcome_text_log_in_initiated message was sent to user
    mock_update.message.reply_text.assert_called_once_with(
        login_initiated_response
    )
    # login_message_id is set in user_data
    assert mock_context.user_data.get("login_message_id") is not None
    # test_login_username passes
    assert result == LOGIN_USERNAME

@pytest.mark.asyncio
async def test_login_username_accepts_input_and_prompts_for_password(
    mock_context, mock_update
):
    result = await login_username(mock_update, mock_context)
    
    # username message is deleted
    mock_update.effective_message.delete.assert_called_once()  
    # telegram bot edit message is called
    mock_context.bot.edit_message_text.assert_called_once_with(
        chat_id=mock_update.effective_chat.id,
        message_id=mock_context.user_data["login_message_id"],
        text=login_username_response,
    )
    # username is set in user_data
    assert mock_context.user_data["username"]
    # /login_username returns LOGIN_PASSWORD
    assert result == LOGIN_PASSWORD
