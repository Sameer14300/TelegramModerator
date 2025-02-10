import re
from pyrogram import Client
from pyrogram.types import User
from config import LINK_PATTERN, OWNER_ID

async def is_admin(client: Client, chat_id: int, user_id: int) -> bool:
    """Check if user is an admin in the chat"""
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

def is_owner(user_id: int) -> bool:
    """Check if user is the bot owner"""
    return user_id == OWNER_ID

def contains_link(text: str) -> bool:
    """Check if text contains links using regex pattern"""
    return bool(re.search(LINK_PATTERN, text or ""))

def get_user_mention(user: User) -> str:
    """Get user mention format"""
    if user.username:
        return f"@{user.username}"
    return f"[{user.first_name}](tg://user?id={user.id})"

async def restrict_user(client: Client, chat_id: int, user_id: int) -> bool:
    """Restrict user in the chat"""
    try:
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions={}  # Empty permissions means fully restricted
        )
        return True
    except Exception as e:
        print(f"Error restricting user: {e}")
        return False