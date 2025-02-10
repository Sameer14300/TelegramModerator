import logging
import sys
from pyrogram import Client, filters
from config import TOKEN, API_ID, API_HASH
from handlers import (
    start_command,
    help_command,
    warn_command,
    unwarn_command,
    broadcast_command,
    check_user_bio
)
from database import Database

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Initialize bot
app = Client(
    "bio_link_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)

def main():
    """Start the bot."""
    try:
        # Test database connection
        db = Database()
        logger.info("Database connection successful")

        # Register command handlers
        app.on_message(filters.command("start") & filters.private)(start_command)
        app.on_message(filters.command("help"))(help_command)
        app.on_message(filters.command("warn") & filters.group)(warn_command)
        app.on_message(filters.command("unwarn") & filters.group)(unwarn_command)
        app.on_message(filters.command("broadcast") & filters.private)(broadcast_command)
        app.on_chat_member_updated()(check_user_bio)

        logger.info("All handlers registered successfully")

        # Start the bot
        logger.info("Starting bot...")
        app.run()
        logger.info("Bot started successfully")

    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()