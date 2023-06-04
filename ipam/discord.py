import flask.app
import flask_discord
from flask import redirect, url_for
from flask_discord import DiscordOAuth2Session, Unauthorized


def configure_discord_auth_routes(app: flask.app.Flask) -> flask_discord.DiscordOAuth2Session:
    discord = DiscordOAuth2Session(app)

    @app.route("/login")
    def login():
        return discord.create_session(scope=['identify'])

    @app.route("/callback")
    def callback():
        discord.callback()
        return redirect(url_for(".root"))

    @app.errorhandler(Unauthorized)
    def redirect_unauthorized(e):
        return redirect(url_for("login"))

    return discord
