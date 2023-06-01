import json


def read():
    with open('/etc/discord-ipam.json', 'r') as f:
        config = json.load(f)
    return config


def config_app(app):
    config = read()
    app.secret_key = config['flask_secret']

    app.config["DISCORD_CLIENT_ID"] = config['discord_client_id']
    app.config["DISCORD_CLIENT_SECRET"] = config['discord_client_secret']
    app.config["DISCORD_REDIRECT_URI"] = "https://ipam.srvlab.acl.fi/callback"
    app.config["DISCORD_BOT_TOKEN"] = ""

