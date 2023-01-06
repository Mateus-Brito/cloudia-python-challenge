from datetime import datetime

from telegram.chat import Chat
from telegram.message import Message
from telegram.user import User


def create_send_message_mock():
    message_id = 0

    def send_message_mock(*args, **kwargs):
        nonlocal message_id
        message_id += 2
        chat_id = kwargs.get("chat_id")
        text = kwargs.get("text")
        bot_user = {
            "id": 10000,
            "username": "thebot",
            "first_name": "bot",
            "is_bot": True,
        }
        message = Message(
            message_id=message_id,
            from_user=User(**bot_user),
            date=datetime.now(),
            chat=Chat(id=chat_id, type="private"),
            edit_date=None,
            text=text,
        )
        return message

    return send_message_mock
