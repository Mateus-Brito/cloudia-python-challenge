# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import sentry_sdk
import sys
import telegram
from flask import Flask, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration

from cloudia_challenge import commands
from cloudia_challenge import telegram as telegram_module
from cloudia_challenge.extensions import db, migrate
from cloudia_challenge.telegram.mock import create_send_message_mock


def create_app(config_object="cloudia_challenge.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    configure_app(app, config_object)
    configure_bot(app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def get_is_running_server():
    command_line = " ".join(sys.argv)
    is_running_server = (
        ("flask run" in command_line)
        or ("gunicorn" in command_line)
        or ("autoapp" in command_line)
    )
    return is_running_server


def configure_bot(app):
    """Register Telegram Bot instance."""
    is_running_server = get_is_running_server()
    if app.config["TESTING"] or not is_running_server:
        from unittest.mock import Mock

        bot = Mock()
        bot.send_message = create_send_message_mock()
    else:
        bot = telegram.Bot(token=app.config["BOT_TOKEN"])
    app.bot = bot
    return app


def configure_app(app, config_object):
    """Register default app configuration"""
    app.config.from_object(config_object)
    app.url_map.strict_slashes = False
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(telegram_module.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    if app.config["SENTRY_DSN_URL"]:
        sentry_sdk.init(
            dsn=app.config["SENTRY_DSN_URL"],
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
        )

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return jsonify({"message": str(error)}), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": telegram.models.TelegramUser}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
