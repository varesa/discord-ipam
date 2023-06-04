import json
from typing import Optional

import flask.app
import flask_discord
from flask import redirect, url_for
from flask_discord import DiscordOAuth2Session, Unauthorized
from flask_discord.models import User

import config


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


class UsernameStore:
    def __init__(self):
        try:
            with open(config.data_path('users.json')) as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}

    def write(self):
        with open(config.data_path('users.json'), 'w') as f:
            json.dump(self.users, f)

    def update(self, user: User):
        uid = user.id
        if self.users.get(uid, {"username": None})['username'] != user.username:
            self.users[uid] = {"username": user.username}
            self.write()

    def get_username(self, uid: int) -> Optional[str]:
        return self.users.get(uid, {"username": None})['username']


class MockDiscord:
    def __init__(self, userid: int):
        self.userid = userid
        self.authorized = True

    def fetch_user(self):
        return MockUser(self.userid)


class MockUser:
    def __init__(self, userid: int):
        self.id = userid
        self.username = "username"
        self.discriminator = "1234"

    def __str__(self):
        return f"{self.username}#{self.discriminator}"
