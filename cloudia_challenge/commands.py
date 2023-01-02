# -*- coding: utf-8 -*-
"""Click commands."""
import os

import click

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
@click.option(
    "-c",
    "--coverage",
    default=True,
    is_flag=True,
    help="Show coverage report",
)
def test(coverage):
    """Run the tests."""
    import pytest

    args = [TEST_PATH, "--verbose"]
    if coverage:
        args.append("--cov=cloudia_challenge")
        args.append("-s")
    rv = pytest.main(args)
    exit(rv)
