from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Define the states
REGISTER_NAME, REGISTER_PIN = range(2)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starts the registration process by asking for the user's name.
    """
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id,
        text="Welcome to the registration process!\n"
        "First we will need your name\n"
        "this is what the shop owner will see!",
    )

    await update.message.reply_text("Please enter your name:")
    return REGISTER_NAME


async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's name input and asks for their PIN.
    """
    name = update.message.text
    context.user_data["name"] = name
    await update.message.reply_text("Please enter a 4-digit PIN:")
    return REGISTER_PIN


async def register_pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's PIN input and saves the user's information.
    """
    pin = update.message.text
    if len(pin) != 4 or not pin.isdigit():
        await update.message.reply_text("Invalid PIN. Please enter a 4-digit number.")
        return REGISTER_PIN

    context.user_data["pin"] = pin
    chat_id = update.effective_chat.id

    # format user_data to be displayed
    user_data = context.user_data

    await context.bot.send_message(chat_id, text="Registration successful!")
    await context.bot.send_message(chat_id, text=user_data)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels the registration process and clears the user's data.
    """
    user_data = context.user_data
    if user_data:
        user_data.clear()

    await update.message.reply_text("Registration canceled.")
    return ConversationHandler.END


# Define the conversation handler
register_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register)],
    states={
        REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)],
        REGISTER_PIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_pin)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
