import pytest
from telegram.ext import ContextTypes

from src.commands.register import (
    register,
    register_name,
    register_pin,
    cancel,
    REGISTER_NAME,
    REGISTER_PIN,
)


@pytest.mark.asyncio
async def test_register(mocked_objects):
    """Tests the behavior of the register function."""
    mocked_update, mocked_context = mocked_objects

    await register(mocked_update, mocked_context)

    expected_message = "Welcome to the registration process!\nFirst we will need your name\nthis is what the shop owner will see!"
    mocked_context.bot.send_message.assert_called_once_with(
        mocked_update.effective_chat.id,
        text=expected_message,
    )
    mocked_update.message.reply_text.assert_called_once_with("Please enter your name:")



# @pytest.mark.asyncio
# async def test_register_name(mocked_objects):
#     """Tests the behavior of the register_name function."""
#     mocked_update, mocked_context = mocked_objects
#     mocked_update.message.text = "John Doe"

#     await register_name(mocked_update, mocked_context)

#     assert mocked_context.user_data == {"name": "John Doe"}
#     mocked_update.message.reply_text.assert_called_once_with(
#         "Please enter a 4-digit PIN:"
#     )
#     assert mocked_context.bot.state == REGISTER_PIN


# @pytest.mark.asyncio
# async def test_register_pin_valid(mocked_objects):
#     """Tests the behavior of the register_pin function with a valid PIN."""
#     mocked_update, mocked_context = mocked_objects
#     mocked_update.message.text = "1234"
#     mocked_context.user_data = {"name": "John Doe"}

#     await register_pin(mocked_update, mocked_context)

#     assert mocked_context.user_data == {"name": "John Doe", "pin": "1234"}
#     mocked_context.bot.send_message.assert_any_call(
#         mocked_update.effective_chat.id,
#         text=mocked_context.user_data,
#     )
#     mocked_context.bot.send_message.assert_any_call(
#         "Registration successful!",
#         chat_id=mocked_update.effective_chat.id,
#     )
#     assert mocked_context.bot.state == ContextTypes.END


# @pytest.mark.asyncio
# async def test_register_pin_invalid(mocked_objects):
#     """Tests the behavior of the register_pin function with an invalid PIN."""
#     mocked_update, mocked_context = mocked_objects
#     mocked_update.message.text = "123"

#     await register_pin(mocked_update, mocked_context)

#     mocked_update.message.reply_text.assert_called_once_with(
#         "Invalid PIN. Please enter a 4-digit number."
#     )
#     assert mocked_context.bot.state == REGISTER_PIN


# @pytest.mark.asyncio
# async def test_cancel(mocked_objects):
#     """Tests the behavior of the cancel function."""
#     mocked_update, mocked_context = mocked_objects
#     mocked_context.user_data = {"name": "John Doe", "pin": "1234"}

#     await cancel(mocked_update, mocked_context)

#     mocked_update.message.reply_text.assert_called_once_with("Registration canceled.")
#     assert mocked_context.user_data == {}
#     assert mocked_context.bot.state == ContextTypes.END
