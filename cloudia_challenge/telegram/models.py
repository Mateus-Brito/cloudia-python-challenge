# -*- coding: utf-8 -*-
"""Telegram models."""
from cloudia_challenge.database import (
    Column,
    Enum,
    PkModel,
    db,
    reference_col,
    relationship,
)

from .enums import ChatTypesEnum


class TelegramUser(PkModel):
    """
    Represented a `user` type in Bot API:
        https://core.telegram.org/bots/api#user
    """

    __tablename__ = "telegram_users"
    is_bot = Column(db.Boolean(), default=False)
    first_name = Column(db.String(128), nullable=False)
    last_name = Column(db.String(128), nullable=True)
    username = Column(db.String(128), nullable=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TelegramUser({self.first_name!r})>"


class TelegramChat(PkModel):
    """
    Represented a `user` type in Bot API:
        https://core.telegram.org/bots/api#chat
    """

    __tablename__ = "telegram_chats"
    type = Column(Enum(ChatTypesEnum), nullable=False)
    title = Column(db.String(512), nullable=True)
    username = Column(db.String(128), nullable=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TelegramChat({self.type!r})>"


class TelegramMessage(PkModel):
    """
    Represented a `user` type in Bot API:
        https://core.telegram.org/bots/api#message
    """

    __tablename__ = "telegram_messages"
    from_user_id = reference_col("telegram_users", nullable=False)
    date = Column(db.DateTime)
    chat_id = reference_col("telegram_chats", nullable=False)
    edit_date = Column(db.DateTime, nullable=True)
    text = Column(db.String(4096), nullable=True)

    chat = relationship("TelegramChat", lazy="joined")
    from_user = relationship("TelegramUser", lazy="joined")
