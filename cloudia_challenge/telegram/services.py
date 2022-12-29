from telegram import User
from telegram.chat import Chat
from telegram.message import Message

from .models import TelegramChat, TelegramMessage, TelegramUser


def create_telegram_user_record(sender: User):
    TelegramUser.create_or_update_by_id(
        id=sender.id,
        is_bot=sender.is_bot,
        first_name=sender.first_name,
        last_name=sender.last_name,
        username=sender.username,
    )


def create_telegram_chat_record(chat: Chat):
    TelegramChat.create_or_update_by_id(
        id=chat.id,
        type=chat.type,
        title=chat.title,
        username=chat.username,
    )


def create_telegram_message_record(message: Message):
    telegram_message = TelegramMessage.create_or_update_by_id(
        id=message.message_id,
        from_user_id=message.from_user.id,
        date=message.date,
        chat_id=message.chat.id,
        edit_date=message.edit_date,
        text=message.text,
    )
    return telegram_message


def save_telegram_records(message: Message):
    create_telegram_user_record(message.from_user)
    create_telegram_chat_record(message.chat)
    create_telegram_message_record(message)
