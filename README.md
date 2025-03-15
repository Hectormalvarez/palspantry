# PalsPantry Bot

A simple Telegram bot for managing a shared pantry/grocery list (work in progress).

## Description

This bot will allow sellers to list items and users to view them. Currently under heavy development.

## Setup

1. **Obtain a Bot Token:** Get a token from [BotFather](https://core.telegram.org/bots#6-botfather) on Telegram.
2. **Clone the Repository:**

    ```bash
    git clone <your_repository_url>
    cd <your_repository_directory>/bot
    ```

3. **Create a Virtual Environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    pip install -r requirements.dev.txt
    ```

5. **Create a `.env` File:**

    - Create `.env` in `bot/`.
    - Add: `BOT_TOKEN=YOUR_BOT_TOKEN` (replace with your token).

6. **Run the Bot:**

    ```bash
    python -m src.bot_main
    ```

## Usage (Current)

- `/help`: Displays a help message.
- `/additem`: Under development.

## Next Step

Implement the initial `/additem` functionality (shop name prompt).
