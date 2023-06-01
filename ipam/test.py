import json
from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

from config import config_app
from netbox import get_asns

app = Flask(__name__)
config_app(app)
print("Hello world")


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

    my_asns = []
    other_asns = []

    for asn in get_asns():
        if str(asn.discord_id()) == str(user.id):
            my_asns.append(asn)
        else:
            other_asns.append(asn)

    my_asns_str = "<br>".join([asn.display() for asn in my_asns])
    other_asns_str = "<br>".join([asn.display() for asn in other_asns])


    return f"""
    <html>
        <head>
            <title>Srvlab IPAM test</title>
        </head>
        <body>
            <p>User info: Authenticated as {user.id} ({user})</p>
            <p>My ASNs:<br>{my_asns_str}</p>
            <p>Other ASNs:<br>{other_asns_str}</p>
        </body>
    </html>"""


if __name__ == "__main__":
    app.run()
