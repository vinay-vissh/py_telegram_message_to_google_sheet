# Telegram Message Tools

This project contains Python scripts to interact with the Telegram API using the [Telethon](https://docs.telethon.dev/) library.

## Prerequisites

- Python 3.x
- A Telegram account
- Telegram API Credentials _(`APP_ID` and `APP_HASH`)_ obtained from [my.telegram.org](https://my.telegram.org)

## Installation

1. Clone the repository or download the source code.

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, you would need to use either `source .venv\Scripts\activate` or `source .venv/Scripts/activate`
   ```

3. Install the required dependencies: `pip install -r requirements.txt`

## Configuration

1. Open `config.py` and update the following variables with your Telegram API credentials:
   - `APP_ID`
   - `APP_HASH`

2. **Generate a Session String:**
   - To avoid logging in every time, you need to generate a session string.
   - Run the session generator script: `python generate_session.py`
     - Follow the on-screen instructions to log in.
     - Once successful, the script will print a session string.

3. Copy the generated session string and paste it into `config.py` as the value for `APP_SESSION_STR`.

## Usage

### Read Subscribed Channels
To list your subscribed channels and view the last message from each:

```bash
python test_read_channels.py
```

### Listen for New Messages
To listen for new messages in real-time (currently configured to listen to all events, or specific channels can be targeted in the code):

```bash
python listen_to_channel.py
```

## Project Structure

- `config.py`: Configuration file for API credentials and session string.
- `generate_session.py`: Script to authenticate and generate a persistent session string.
- `test_read_channels.py`: Script to fetch and display subscribed channels and their latest messages.
- `listen_to_channel.py`: Script to listen for incoming messages in real-time.
