from environs import Env

env = Env()
env.read_env()

"""Settings module for test app."""
FLASK_DEBUG = True
TESTING = True
SQLALCHEMY_DATABASE_URI = env.str("TEST_DATABASE_URL", default="sqlite:////tmp/test.db")
SECRET_KEY = "not-so-secret-in-tests"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SENTRY_DSN_URL = None
SAVE_LOG_FILE = False
