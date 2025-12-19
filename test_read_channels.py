from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Channel
import config
import asyncio


async def main():
    try:
        # Initialize the client using the session string from config
        client = TelegramClient(
            StringSession(config.APP_SESSION_STR), config.APP_ID, config.APP_HASH
        )
    except Exception as e:
        print(f"Error initializing TelegramClient: {e}")
        print(
            "Please check if your APP_SESSION_STR in config.py is correct and valid for Telethon."
        )
        return

    print("Connecting...")
    await client.connect()

    if not await client.is_user_authorized():
        print("Session is invalid or not authorized. Please check your session string.")
        return

    print("Fetching subscribed channels...")

    # Iterate through all dialogs (chats/channels/groups)
    async for dialog in client.iter_dialogs():
        # Check if the entity is a Channel (and not a MegaGroup/SuperGroup if you only want broadcast channels,
        # but usually 'channels' implies both broadcast channels and supergroups in user terms.
        # Strictly speaking, Channel type covers both.
        # If we want strictly broadcast channels, we check dialog.is_channel and not dialog.is_group)

        if dialog.is_channel:
            # dialog.entity can be used to get more details
            print(f"Name: {dialog.name}, ID: {dialog.id}")

            # Get the last message
            messages = await client.get_messages(dialog.entity, limit=1)
            if messages:
                last_msg = messages[0]
                # Check if message has text, otherwise indicate it might be media
                content = last_msg.text if last_msg.text else "[Media or Empty]"
                print(f"Last Message: {content}")
            print("-" * 30)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
