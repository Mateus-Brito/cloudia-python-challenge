# -*- coding: utf-8 -*-
"""Check if the program is correctly storing the messages sent by the user"""
import json
from datetime import datetime

from telegram import User
from telegram.chat import Chat
from telegram.message import Message

from cloudia_challenge.telegram.enums import ChatTypesEnum
from cloudia_challenge.telegram.models import (
    TelegramChat,
    TelegramMessage,
    TelegramUser,
)
from cloudia_challenge.telegram.services import (
    create_telegram_chat_record,
    create_telegram_message_record,
    create_telegram_user_record,
)


def test_store_user_record(db):
    """Create a new telegram user record on the database."""
    sender = {
        "id": 1,
        "is_bot": False,
        "first_name": "Teste",
        "last_name": None,
        "username": "teste",
    }
    create_telegram_user_record(User(**sender))

    assert db.session.query(TelegramUser).count() == 1
    new_user = db.session.query(TelegramUser).filter_by(id=1).first()
    assert new_user.id == sender["id"]
    assert new_user.is_bot == sender["is_bot"]
    assert new_user.first_name == sender["first_name"]
    assert new_user.last_name == sender["last_name"]
    assert new_user.username == sender["username"]


def test_store_chat_record(db):
    """Create a new telegram chat record on the database."""
    chat = {
        "id": 1,
        "type": ChatTypesEnum.private,
        "title": "my_chat",
        "username": "teste",
    }
    create_telegram_chat_record(Chat(**chat))

    assert db.session.query(TelegramChat).count() == 1
    new_chat = db.session.query(TelegramChat).filter_by(id=1).first()
    assert new_chat.id == chat["id"]
    assert new_chat.type == chat["type"]
    assert new_chat.title == chat["title"]
    assert new_chat.username == chat["username"]


def test_store_message_record(db):
    """Create a new telegram message record on the database."""
    user_data = {"id": 1, "username": "teste", "first_name": "teste", "is_bot": False}
    chat_data = {"id": 1, "type": ChatTypesEnum.private}
    TelegramUser.create(**user_data)
    TelegramChat.create(**chat_data)

    message = {
        "message_id": 1,
        "from_user": User(**user_data),
        "date": datetime.now(),
        "chat": Chat(**chat_data),
        "edit_date": None,
        "text": "hi",
    }
    create_telegram_message_record(Message(**message))

    assert db.session.query(TelegramMessage).count() == 1
    new_message = db.session.query(TelegramMessage).filter_by(id=1).first()
    assert new_message.id == message["message_id"]
    assert new_message.from_user_id == message["from_user"]["id"]
    assert new_message.date == message["date"]
    assert new_message.chat_id == message["chat"]["id"]
    assert new_message.edit_date == message["edit_date"]
    assert new_message.text == message["text"]


def test_question_and_answer_messages_flow(client, db):
    """Test flow of question and answer messages."""
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    user_data = {"id": 1, "username": "teste", "first_name": "teste", "is_bot": False}
    chat_data = {"id": 1, "type": ChatTypesEnum.private.value}
    data = {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "from": user_data,
            "date": int(datetime.now().timestamp()),
            "chat": chat_data,
            "edit_date": None,
            "text": "15",
        }
    }
    client.post("/api/telegram/update", data=json.dumps(data), headers=headers)
    messages = db.session.query(TelegramMessage).all()

    assert len(messages) == 2
    assert messages[0].text == "15"
    assert messages[1].text == "FizzBuzz"
