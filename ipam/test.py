import json
from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

from .config import config_app

app = Flask(__name__)
config_app(app)


discord = DiscordOAuth2Session(app)

@app.route("/login")
def login():
    return discord.create_session(scope=['identify'])
	

@app.route("/callback")
def callback():
    discord.callback()
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

	
@app.route("/me")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>Srvlab IPAM test</title>
        </head>
        <body>
            <pre>User info: Authenticated as {json.dumps(user.__dict__, indent=4)}</pre>
        </body>
    </html>"""


if __name__ == "__main__":
    app.run()
