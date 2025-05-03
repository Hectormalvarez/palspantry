import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv

from commands.help import help_command

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def main():
    """Runs the bot."""

    # Get the bot token from the environment variable
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        logging.error("BOT_TOKEN environment variable not set!")
        raise ValueError("BOT_TOKEN environment variable not set!")

    try:
        # Create the application
        application = ApplicationBuilder().token(TOKEN).build()

        # Register command handlers
        application.add_handler(CommandHandler("help", help_command))

        # Start the bot
        application.run_polling()
    except Exception as e:
        logging.critical(f"Bot failed to start: {e}")
        raise

if __name__ == "__main__":
    main()