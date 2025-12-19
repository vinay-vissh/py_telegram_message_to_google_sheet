from telethon import TelegramClient, events
from telethon.sessions import StringSession
import config
import asyncio

# You can specify the channel username or ID here.
# Example: 'my_channel' or 123456789
# If you want to listen to ALL chats, remove the `chats` parameter in the decorator.
TARGET_CHANNEL = "me"  # Listening to "Saved Messages" for testing. Change this to your desired channel.

print("Initializing Telegram Client for listening...")
client = TelegramClient(
    StringSession(config.APP_SESSION_STR), config.APP_ID, config.APP_HASH
)


@client.on(events.NewMessage())
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

    print(f"Listening for new messages in: {TARGET_CHANNEL}...")
    print("Press Ctrl+C to stop.")

    # This will keep the script running and listening for events
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped listening.")
