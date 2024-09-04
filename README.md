# Telegram Bot for Governance Proposals

This is a Python-based Telegram bot that monitors governance proposals from the Cardano blockchain using the Koios API and sends notifications to a specified Telegram chat when new governance actions are detected.

## Features

- Fetches governance proposals from the Koios API.
- Notifies via Telegram when new proposals are detected.
- Keeps track of notified proposals to avoid duplicate notifications.
- Logs bot activity and errors to a log file.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/thenic95/Governance-Action-Notification-Telegram-Bot.git
    ```

2. **Install required dependencies**:

    Use `pip` to install the required Python libraries:

    ```sh
    pip install requests
    ```

3. **Set up your environment**:

    - Replace `'YOUR_BOT_TOKEN'` with your actual Telegram bot token.
    - Replace `'YOUR_CHAT_ID'` with your Telegram chat ID.

4. **Run the bot**:

    Execute the Python script to start the bot:

    ```sh
    python telegram_bot.py
    ```

## Usage

The bot will:
1. Fetch new governance proposals from the Koios API.
2. Send a message to the specified Telegram chat whenever a new proposal is detected.
3. Log its activities to `telegram_bot_log.txt`.

## Configuration

You can customize the following files:

- **`telegram_bot.py`**: Modify the script to change the bot's behavior or message format.
- **`notified_proposals.json`**: Stores the IDs of proposals that have already been notified. This file is automatically created and updated by the script.
- **`telegram_bot_log.txt`**: Stores log information, including errors and successful operations. This file is automatically created and updated by the script.

## Troubleshooting

- If the bot fails to fetch proposals, check your internet connection or the Koios API status.
- Review the log file (`telegram_bot_log.txt`) for detailed error messages and debugging information.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or suggestions.

## License

This project is licensed under the MIT License - see the [Apache License Version 2.0](LICENSE) file for details.
