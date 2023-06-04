from flask import Flask, render_template, redirect, url_for
from flask_discord import requires_authorization
import os

from config import config_app
from ipam.discord import configure_discord_auth_routes, MockDiscord, UsernameStore
from ipam.logic import get_user_ASNs, alloc_new_ASN

app = Flask(__name__)
config_app(app)
if not os.environ.get("MOCK_AUTH"):
    discord = configure_discord_auth_routes(app)
else:
    discord = MockDiscord(139452618190618624)
    app.discord = discord

user_store = UsernameStore()


@app.route("/")
@requires_authorization
def root():
    user = discord.fetch_user()
    user_store.update(user)
    my_ASNs, other_ASNs = get_user_ASNs(user)

    context = {
        "user": user,
        "user_store": user_store,
        "my_ASNs": my_ASNs,
        "other_ASNs": other_ASNs,
    }

    return render_template("home.html", **context)


@app.route("/new_asn")
@requires_authorization
def route_new_asn():
    user = discord.fetch_user()
    alloc_new_ASN(user)
    return redirect(url_for(".root"))


if __name__ == "__main__":
    app.run()
