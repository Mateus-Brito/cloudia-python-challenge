import enum


class ChatTypesEnum(enum.Enum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"
