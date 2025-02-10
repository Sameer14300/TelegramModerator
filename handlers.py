from pyrogram import Client, filters
from pyrogram.types import Message, ChatMember
from config import WARN_MESSAGE, RESTRICTED_MESSAGE, BROADCAST_SUCCESS, OWNER_ID
from database import Database
from utils import is_admin, is_owner, contains_link, get_user_mention, restrict_user

db = Database()

async def start_command(client: Client, message: Message):
    """Handle /start command"""
    await message.reply_text(
        "Hello! I'm a group moderation bot that helps detect and restrict users with links in their bios."
    )

async def help_command(client: Client, message: Message):
    """Handle /help command"""
    help_text = """
🤖 *Available Commands*

Regular Users:
/start - Start the bot
/help - Show this help message
/warns - Check your warnings

Admins Only:
/warn - Warn a user
/unwarn - Remove warning from user
/settings - Configure group settings

Owner Only:
/broadcast - Send message to all groups
    """
    await message.reply_text(help_text, parse_mode='markdown')

async def warn_command(client: Client, message: Message):
    """Handle /warn command"""
    if not message.reply_to_message:
        await message.reply_text("Reply to a user's message to warn them.")
        return

    chat_id = message.chat.id
    if not await is_admin(client, message.chat.id, message.from_user.id):
        await message.reply_text("This command is only for admins!")
        return

    target_user = message.reply_to_message.from_user
    warn_count = db.add_warning(target_user.id, chat_id, target_user.username)

    warn_msg = WARN_MESSAGE.format(
        user_mention=get_user_mention(target_user),
        warn_count=warn_count
    )

    if warn_count >= 3:
        if await restrict_user(client, chat_id, target_user.id):
            warn_msg += "\n🚫 User has been restricted due to excessive warnings."

    await message.reply_text(warn_msg, parse_mode='markdown')

async def unwarn_command(client: Client, message: Message):
    """Handle /unwarn command"""
    if not message.reply_to_message:
        await message.reply_text("Reply to a user's message to remove their warning.")
        return

    if not await is_admin(client, message.chat.id, message.from_user.id):
        await message.reply_text("This command is only for admins!")
        return

    target_user = message.reply_to_message.from_user
    warn_count = db.remove_warning(target_user.id, message.chat.id)

    await message.reply_text(
        f"Warning removed for {get_user_mention(target_user)}. Current warnings: {warn_count}",
        parse_mode='markdown'
    )

async def broadcast_command(client: Client, message: Message):
    """Handle /broadcast command"""
    if not is_owner(message.from_user.id):
        await message.reply_text("This command is only for the bot owner!")
        return

    if len(message.command) < 2:
        await message.reply_text("Please provide a message to broadcast.")
        return

    broadcast_message = " ".join(message.command[1:])
    success_count = 0
    groups = db.get_all_groups()

    for group in groups:
        try:
            await client.send_message(
                chat_id=group["chat_id"],
                text=broadcast_message,
                parse_mode='markdown'
            )
            success_count += 1
        except Exception as e:
            print(f"Broadcast failed for group {group['chat_id']}: {e}")

    await message.reply_text(
        BROADCAST_SUCCESS.format(success_count=success_count)
    )

async def check_user_bio(client: Client, message: Message):
    """Check user's bio for links when they join the group"""
    if not message.new_chat_members:
        return

    for member in message.new_chat_members:
        try:
            user = await client.get_users(member.id)
            if user.bio and contains_link(user.bio):
                warn_count = db.add_warning(member.id, message.chat.id, member.username)
                warn_msg = WARN_MESSAGE.format(
                    user_mention=get_user_mention(member),
                    warn_count=warn_count
                )

                if warn_count >= 3:
                    if await restrict_user(client, message.chat.id, member.id):
                        warn_msg = RESTRICTED_MESSAGE.format(
                            user_mention=get_user_mention(member),
                            warn_count=warn_count
                        )

                await message.reply_text(warn_msg, parse_mode='markdown')
        except Exception as e:
            print(f"Error checking bio for user {member.id}: {e}")