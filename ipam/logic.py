from ipam import netbox
import flask_discord.models


def get_user_ASNs(user: flask_discord.models.User) -> (list[netbox.ASN], list[netbox.ASN]):
    my_ASNs = []
    other_ASNs = []

    for asn in netbox.ASN.get_all():
        if str(asn.discord_id()) == str(user.id):
            my_ASNs.append(asn)
        else:
            other_ASNs.append(asn)

    return my_ASNs, other_ASNs