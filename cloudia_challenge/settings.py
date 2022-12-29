# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

FLASK_DEBUG = env.str("FLASK_DEBUG", default=False)
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL", default="sqlite:////tmp/test.db")
SECRET_KEY = env.str("SECRET_KEY")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SENTRY_DSN_URL = env.str("SENTRY_DSN_URL", default=None)
BOT_TOKEN = env.str("BOT_TOKEN")
SAVE_LOG_FILE = False
