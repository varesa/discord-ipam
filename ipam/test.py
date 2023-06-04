from flask import Flask, redirect, url_for
from flask_discord import requires_authorization

from config import config_app
from ipam.discord import configure_discord_auth_routes
from ipam.logic import get_user_ASNs

app = Flask(__name__)
config_app(app)
discord = configure_discord_auth_routes(app)


@app.route("/")
@requires_authorization
def root():
    user = discord.fetch_user()
    my_ASNs, other_ASNs = get_user_ASNs(user)

    my_ASNs_str = "<br>".join([ASN.display() for ASN in my_ASNs])
    other_ASNs_str = "<br>".join([ASN.display() for ASN in other_ASNs])

    return f"""
    <html>
        <head>
            <title>Srvlab IPAM test</title>
        </head>
        <body>
            <p>User info: Authenticated as {user.id} ({user})</p>
            <p>My ASNs:<br>{my_ASNs_str}</p>
            <p>Other ASNs:<br>{other_ASNs_str}</p>
        </body>
    </html>"""


if __name__ == "__main__":
    app.run()
