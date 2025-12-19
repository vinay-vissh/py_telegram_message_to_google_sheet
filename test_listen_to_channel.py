from telethon import TelegramClient, events
from telethon.sessions import StringSession
import config
import asyncio
import logging

# Configure logging to see connection/disconnection events
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

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
