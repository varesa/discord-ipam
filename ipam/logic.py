from netbox import ASN
import flask_discord.models


def get_user_ASNs(user: flask_discord.models.User) -> (list[ASN], list[ASN]):
    my_ASNs = []
    other_ASNs = []

    for ASN in ASN.get_all():
        if str(ASN.discord_id()) == str(user.id):
            my_ASNs.append(ASN)
        else:
            other_ASNs.append(ASN)

    return my_ASNs, other_ASNs