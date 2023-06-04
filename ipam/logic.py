from netbox import Asn
import flask_discord.models


def get_user_asns(user: flask_discord.models.User) -> (list[Asn], list[Asn]):
    my_asns = []
    other_asns = []

    for asn in Asn.get_all():
        if str(asn.discord_id()) == str(user.id):
            my_asns.append(asn)
        else:
            other_asns.append(asn)

    return my_asns, other_asns