from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import config


def generate_string_session():
    print("Initializing Telegram Client to generate session string...")

    # We use a blank StringSession() to generate a new one
    with TelegramClient(StringSession(), config.APP_ID, config.APP_HASH) as client:
        # This will trigger the authentication flow (phone number -> code -> password)
        # It automatically asks for input in the console
        session_string = client.session.save()

        print("\n--- Session String Generated ---")
        print(
            "Please copy the string below and paste it into your config.py as APP_SESSION_STR:\n"
        )
        print(session_string)
        print("\n--------------------------------")

        print("\nRunning a quick test to verify the session...")
        try:
            me = client.get_me()
            print(f"Logged in as: {me.first_name} (ID: {me.id})")

            print("Fetching first 5 subscribed channels:")
            count = 0
            # iter_dialogs is synchronous here because we imported from telethon.sync
            for dialog in client.iter_dialogs():
                if dialog.is_channel:
                    print(f"- {dialog.name} (ID: {dialog.id})")
                    count += 1
                    if count >= 5:
                        break
            print("Test complete. Session is valid.")
        except Exception as e:
            print(f"Test failed: {e}")


if __name__ == "__main__":
    generate_string_session()
