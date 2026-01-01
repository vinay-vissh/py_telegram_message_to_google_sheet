from telethon import TelegramClient, events
from telethon.sessions import StringSession
import config
import asyncio
from datetime import datetime
import pytz
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
            f"Successfully connected to Google Sheet: '{sh.title}' (ID: {config.GOOGLE_SHEET_ID}) / Worksheet: '{config.GOOGLE_SHEET_NAME}'"
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
    target = config.TARGET_CHANNEL
    # Convert string ID to int if it looks like one (e.g. "-100...")
    if isinstance(target, str):
        if target.lstrip("-").isdigit():
            target = int(target)
    event_params["chats"] = target


@client.on(events.NewMessage(**event_params))
async def new_message_handler(event):
    chat = await event.get_chat()
    sender = await event.get_sender()

    chat_name = chat.title if hasattr(chat, "title") else "Unknown"
    sender_name = sender.first_name if sender else "Unknown"
    message_id = event.id
    message = event.text
    status = "Pending"

    ist = pytz.timezone("Asia/Kolkata")
    status_updated_at = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

    print(f"--- New Message in {chat_name} ---")
    print(f"Message ID: {message_id}")  # Print ID
    print(f"Sender: {sender_name}")
    print(f"Message: {message}")
    print("-" * 30)

    if sheet:
        try:
            # timestamp, chat_name, sender_name, message
            timestamp = event.date.astimezone(ist).strftime("%Y-%m-%d %H:%M:%S")
            # Insert row at index 2 (below the header) so the latest message is on top
            sheet.insert_row(
                [
                    timestamp,
                    chat_name,
                    sender_name,
                    message_id,
                    message,
                    status,
                    status_updated_at,
                ],
                index=2,
                value_input_option="USER_ENTERED",
            )
            print("Logged to Google Sheet.")
        except Exception as e:
            print(f"Failed to log to Google Sheet: {e}")


async def main():
    print("Connecting...")
    await client.start()

    # If we are filtering by a specific chat, ensure the client has it in cache
    if "chats" in event_params:
        target = event_params["chats"]
        try:
            await client.get_entity(target)
        except ValueError:
            print(f"Entity {target} not found in session. Refreshing dialogs...")
            await client.get_dialogs()
            # Try again to verify
            try:
                await client.get_entity(target)
                print(f"Successfully found entity {target}.")
            except ValueError:
                print(
                    f"ERROR: Could not find entity {target} even after refreshing dialogs. Check the ID/Username."
                )
                print(
                    "Exiting script because the target channel is invalid or not accessible."
                )
                await client.disconnect()
                return

    target_desc = "ALL CHATS"
    if config.TARGET_CHANNEL:
        try:
            entity = await client.get_entity(event_params["chats"])
            target_desc = (
                getattr(entity, "title", None)
                or getattr(entity, "first_name", None)
                or config.TARGET_CHANNEL
            )

            if target_desc != config.TARGET_CHANNEL:
                target_desc += f" ({config.TARGET_CHANNEL})"
        except Exception:
            target_desc = config.TARGET_CHANNEL

    print(f"Listening for new messages in: {target_desc}...")
    print("Press Ctrl+C to stop.")

    # This will keep the script running and listening for events
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped listening.")
