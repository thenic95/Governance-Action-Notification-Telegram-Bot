import requests
import json
import logging
from logging.handlers import RotatingFileHandler

# Replace with your bot token
TELEGRAM_BOT_TOKEN = 'INSERT HERE' # Insert your Telegram bot token here. Follow instructions at https://core.telegram.org/bots/tutorial
TELEGRAM_CHAT_ID = 'INSERT HERE' # Replace with your Telegram chat ID with your bot. Instructions can be found here: https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id

# URL of the Koios API endpoint for proposals
API_URL = "https://api.koios.rest/api/v1/proposal_list" # This is the public Koios API for Cardano Mainnet

# File to store the IDs of proposals that have been notified
NOTIFIED_PROPOSALS_FILE = 'notified_proposals.json'

# Configure logging with log rotation
log_handler = RotatingFileHandler('telegram_bot_log.txt', maxBytes=1024*1024, backupCount=5)
logging.basicConfig(
    handlers=[log_handler],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def load_notified_proposals():
    """Load the list of notified proposals from a JSON file."""
    try:
        with open(NOTIFIED_PROPOSALS_FILE, 'r') as file:
            notified_proposals = json.load(file)
        logging.info("Loaded notified proposals from JSON file.")
    except FileNotFoundError:
        notified_proposals = set()
        logging.info("No previous notified proposals file found. Starting fresh.")
    except json.JSONDecodeError:
        notified_proposals = set()
        logging.error("Error reading JSON file. Starting fresh with an empty set.")
    return set(notified_proposals)  # Convert to set to avoid duplicates

def save_notified_proposals(notified_proposals):
    """Save the notified proposals to a JSON file."""
    with open(NOTIFIED_PROPOSALS_FILE, 'w') as file:
        json.dump(list(notified_proposals), file)
    logging.info("Saved notified proposals to JSON file.")

def fetch_proposals():
    """Fetch the latest governance proposals from the Koios API."""
    try:
        response = requests.get(API_URL, headers={"accept": "application/json"})
        response.raise_for_status()  # Raise an exception for HTTP errors
        logging.info("Successfully fetched proposals.")
        
        # Check if the response content is valid JSON
        try:
            proposals = response.json()
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON response from the API.")
            return None

        # Check if the response contains expected data
        if not proposals or not isinstance(proposals, list):
            logging.warning("API response does not contain valid proposals data.")
            logging.warning(f"Response content: {response.text}")
            return None

        return proposals
    except requests.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

def send_telegram_message(message):
    """Send a formatted message to the Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"  # Use Markdown for better formatting
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logging.info("Message sent successfully.")
    except requests.RequestException as e:
        logging.error(f"Error sending message: {e}")

def format_message(proposal):
    """Format the message in a more readable way."""
    description = proposal.get('proposal_description', {}).get('summary', 'No description available')
    meta_url = proposal.get('meta_url', 'No URL available')

    # Format the message including the meta_url
    message = (
        f"*New Governance Proposal Detected!*\n"
        f"*Proposal ID:* `{proposal['proposal_id']}`\n"
        f"*Type:* {proposal['proposal_type']}\n"
        f"*Description:* {description}\n"
        f"*Proposed Epoch:* {proposal.get('proposed_epoch', 'N/A')}\n"
        f"*Expiration:* {proposal.get('expiration', 'N/A')}\n"
        f"*Meta URL:* [{meta_url}]({meta_url})\n"  # Include the meta_url with Markdown link format
    )
    return message


def compare_and_notify(latest_proposals, notified_proposals):
    """Compare the latest proposals with already notified proposals and notify of new ones."""
    if latest_proposals is None:
        logging.warning("No proposals to compare; fetch may have failed or returned invalid data.")
        return

    new_proposals = [p for p in latest_proposals if p['proposal_id'] not in notified_proposals]

    if new_proposals:
        for proposal in new_proposals:
            message = format_message(proposal)
            send_telegram_message(message)
            # Mark the proposal as notified
            notified_proposals.add(proposal['proposal_id'])
            logging.info(f"New proposal detected and notified: {proposal['proposal_id']}")
        # Save updated list of notified proposals to the JSON file
        save_notified_proposals(notified_proposals)
    else:
        logging.info("No new proposals found. No message will be sent.")

def main():
    """Main function to fetch and check proposals."""
    notified_proposals = load_notified_proposals()

    latest_proposals = fetch_proposals()
    if latest_proposals is not None:
        compare_and_notify(latest_proposals, notified_proposals)
    else:
        logging.warning("Failed to fetch proposals. Retrying in the next run...")

if __name__ == "__main__":
    main()