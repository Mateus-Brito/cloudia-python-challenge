from flask import Blueprint, current_app, request
from telegram import Update

from .services import save_telegram_records

blueprint = Blueprint("telegram", __name__, url_prefix="/api/telegram")

MAX_LENGTH = 280


def process_input(text_input: str):
    if len(text_input) > MAX_LENGTH:
        return "A entrada é muito longa. Por favor, insira até 280 caracteres."

    if not text_input.isdigit():
        return "Por favor, insira um número inteiro."

    integer_input = int(text_input)
    if integer_input % 3 == 0 and integer_input % 5 == 0:
        return "FizzBuzz"
    elif integer_input % 3 == 0:
        return "Fizz"
    elif integer_input % 5 == 0:
        return "Buzz"

    return integer_input


@blueprint.route("/update", methods=["POST"])
def webhook_handler():
    update = Update.de_json(request.get_json(force=True), current_app.bot)

    input_message = update.message
    save_telegram_records(input_message)

    text_output = process_input(update.message.text)
    output_message = current_app.bot.send_message(
        chat_id=update.message.chat_id, text=text_output
    )

    save_telegram_records(output_message)
    return "ok"
