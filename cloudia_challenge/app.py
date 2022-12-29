# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging

import sentry_sdk
from flask import Flask, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration

from cloudia_challenge import commands, telegram
from cloudia_challenge.extensions import db, ma, migrate


def create_app(config_object="cloudia_challenge.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    configure_app(app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def configure_app(app):
    app.url_map.strict_slashes = False
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(telegram.views.blueprint)
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
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    if not app.config["FLASK_DEBUG"]:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)

        if app.config["SAVE_LOG_FILE"]:
            file_handler = logging.FileHandler("access.log")
            file_handler.setLevel(logging.DEBUG)
            app.logger.addHandler(file_handler)
