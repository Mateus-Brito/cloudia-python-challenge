# -*- coding: utf-8 -*-
"""Create an application instance."""
from cloudia_challenge.app import create_app

app = create_app()

if app.debug:
    from flask_cloudflared import run_with_cloudflared

    run_with_cloudflared(app)

if __name__ == "__main__":
    app.run()
