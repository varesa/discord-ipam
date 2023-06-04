from flask import Flask, render_template
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

    context = {
        "my_ASNs_str": "<br>".join([ASN.display() for ASN in my_ASNs]),
        "other_ASNs_str": "<br>".join([ASN.display() for ASN in other_ASNs]),
    }

    return render_template("home.html", **context)


if __name__ == "__main__":
    app.run()
