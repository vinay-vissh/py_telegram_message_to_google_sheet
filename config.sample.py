# Telegram App Credentials
APP_ID = "34632541"
APP_HASH = "ea4a9d7bc12152ef335f385b2c5cd766"
APP_SESSION_STR = "1BVtsOMcBuzqfOJBeN3ImEOJ5ws8oDe63eoFjPx_wUAE4EwPKcBCckaJXJXGQHGTukoPK980_Azq9ALI5Ek8DiJpivAojIlcpNV44YMrp9VGDgXZ9OssNIWXceOoEKb5uLJoolYrwLtYpk-dgyporHlcZHJJRlonYf2IuF2AY8kdNjqaDaVrJhyjFukzEAqdhX6tmsSFJmqLBkZc7ZQ2cT-ryGwxl20aCSO6OMevEWK4EM22SXqdaIk45q-YmrOXcpk2A4iHiiS2A82ZoeQBqjkpJkZkNCL5yiPeUEEcymAPJmzWkE9J2VouQwdtz9"

# You can specify the channel username or ID here.
# Example: 'my_channel' or 123456789
# Set to None to listen to ALL chats.
# TARGET_CHANNEL = "me"  # Listen to "Saved Messages" for testing
TARGET_CHANNEL = None  # Listen to ALL chats

# Google Sheet Configuration
GOOGLE_SHEET_ID = "1YKN_xfKP142GZs9dUWuQbBF_kSyBemV98ZtJ4CF6028"  # The ID of the Google Sheet to write to
GOOGLE_SHEET_NAME = "Chats"  # The name of the specific worksheet
GOOGLE_SHEET_CREDENTIALS_FILE = (
    "gcp-service-account.json"  # Path to the service account JSON file
)
