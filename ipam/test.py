import os
import json

from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__)

with open('/etc/discord-ipam.json', 'r') as f:
    config = json.load(f)

app.secret_key = config['flask_secret']

app.config["DISCORD_CLIENT_ID"] = config['discord_client_id']
app.config["DISCORD_CLIENT_SECRET"] = config['discord_client_secret']
app.config["DISCORD_REDIRECT_URI"] = "https://ipam.srvlab.acl.fi/callback"
app.config["DISCORD_BOT_TOKEN"] = ""

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
