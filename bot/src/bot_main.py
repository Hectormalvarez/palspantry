"""Main module for the Pals Pantry bot."""

from handlers import create_application


if __name__ == "__main__":
    create_application().run_polling()
