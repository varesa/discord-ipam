from flask import Flask, redirect, url_for
from flask_discord import requires_authorization

from config import config_app
from ipam.discord import configure_discord_auth_routes
from ipam.logic import get_user_asns

app = Flask(__name__)
config_app(app)
discord = configure_discord_auth_routes(app)


@app.route("/")
@requires_authorization
def root():
    user = discord.fetch_user()
    my_asns, other_asns = get_user_asns(user)

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
