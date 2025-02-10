import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TOKEN = os.getenv('BOT_TOKEN')
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/telegram_bot')
OWNER_ID = int(os.getenv('OWNER_ID', '12345'))  # Replace with actual owner ID

# Message Templates
WARN_MESSAGE = """
⚠️ Warning! User {user_mention}
Your bio contains links which are not allowed in this group.
Warnings: {warn_count}/3
"""

RESTRICTED_MESSAGE = """
🚫 User {user_mention} has been restricted due to having links in bio.
Total warnings: {warn_count}
"""

BROADCAST_SUCCESS = "✅ Broadcast message sent to {success_count} chats"

# Regular Expressions
LINK_PATTERN = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|([a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+)'

# Pyrogram API Configuration
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

# Command descriptions
COMMANDS = {
    'start': 'Start the bot',
    'help': 'Show help message',
    'warn': 'Warn a user',
    'unwarn': 'Remove warnings from a user',
    'warns': 'Check warnings for a user',
    'broadcast': 'Broadcast message (Owner only)',
    'settings': 'Configure group settings'
}