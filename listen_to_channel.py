from telethon import TelegramClient, events
from telethon.sessions import StringSession
import config
import asyncio
import logging
import gspread
import traceback
from google.oauth2.service_account import Credentials

# Configure logging to see connection/disconnection events
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Google Sheet Setup
sheet = None
if config.GOOGLE_SHEET_ID and config.GOOGLE_SHEET_CREDENTIALS_FILE:
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(
            config.GOOGLE_SHEET_CREDENTIALS_FILE, scopes=scopes
        )
        gc = gspread.authorize(creds)
        # Open the spreadsheet by ID, then select the worksheet by name
        sh = gc.open_by_key(config.GOOGLE_SHEET_ID)
        sheet = sh.worksheet(config.GOOGLE_SHEET_NAME)
        print(
            f"Successfully connected to Google Sheet: {config.GOOGLE_SHEET_ID} ({config.GOOGLE_SHEET_NAME})"
        )
    except Exception as e:
        print(f"Error connecting to Google Sheet: {e}")
        traceback.print_exc()

print("Initializing Telegram Client for listening...")
client = TelegramClient(
    StringSession(config.APP_SESSION_STR), config.APP_ID, config.APP_HASH
)


# Configure event listener arguments
# If config.TARGET_CHANNEL is set, we filter by that chat. Otherwise, we listen to all.
event_params = {}
if config.TARGET_CHANNEL:
    event_params["chats"] = config.TARGET_CHANNEL


@client.on(events.NewMessage(**event_params))
async def new_message_handler(event):
    chat = await event.get_chat()
    sender = await event.get_sender()

    chat_name = chat.title if hasattr(chat, "title") else "Unknown"
    sender_name = sender.first_name if sender else "Unknown"

    print(f"--- New Message in {chat_name} ---")
    print(f"Sender: {sender_name}")
    print(f"Message: {event.text}")
    print("-" * 30)

    if sheet:
        try:
            # timestamp, chat_name, sender_name, message
            timestamp = event.date.strftime("%Y-%m-%d %H:%M:%S")
            # Insert row at index 2 (below the header) so the latest message is on top
            sheet.insert_row([timestamp, chat_name, sender_name, event.text], index=2)
            print("Logged to Google Sheet.")
        except Exception as e:
            print(f"Failed to log to Google Sheet: {e}")


async def main():
    print("Connecting...")
    await client.start()

    target_desc = config.TARGET_CHANNEL if config.TARGET_CHANNEL else "ALL CHATS"
    print(f"Listening for new messages in: {target_desc}...")
    print("Press Ctrl+C to stop.")

    # This will keep the script running and listening for events
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped listening.")
