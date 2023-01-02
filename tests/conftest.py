# -*- coding: utf-8 -*-
"""Providing fixtures for the directory."""
import logging

import pytest

from cloudia_challenge.app import create_app
from cloudia_challenge.database import db as _db

@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app(config_object="tests.settings")
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture()
def client(app):
    """Create client for the tests."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()
