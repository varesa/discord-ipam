import pynetbox

from config import read as config

URL = 'https://netbox.srvlab.acl.fi'
TOKEN = config()['netbox_key']

nb = pynetbox.api(URL, token=TOKEN)


class ASN:
    netbox_object: pynetbox.core.response.Record = None

    def __init__(self, netbox_object: pynetbox.core.response.Record):
        self.netbox_object = netbox_object

    def asn(self) -> int:
        return self.netbox_object.ASN

    def display(self) -> str:
        return self.netbox_object.display

    def discord_id(self):
        return self.netbox_object.custom_fields['discord_id']

    @staticmethod
    def get_all():
        ASNs = []

        api = nb.ipam.asns
        for ASN in api.all():
            ASNs.append(ASN(ASN))

        return ASNs


class Address:
    netbox_object: pynetbox.core.response.Record = None

    def __init__(self, netbox_object: pynetbox.core.response.Record):
        self.netbox_object = netbox_object

    @property
    def with_mask(self) -> str:
        return self.netbox_object.address

    @property
    def without_mask(self) -> str:
        return self.with_mask.split('/')[0]


class Prefix:
    netbox_object: pynetbox.core.response.Record = None

    def __init__(self, netbox_object: pynetbox.core.response.Record):
        self.netbox_object = netbox_object

    @property
    def cidr(self) -> str:
        return self.netbox_object.prefix

    def create_inner(self, prefix_length: int=30, description: str="") -> 'Prefix':
        return Prefix(self.netbox_object.available_prefixes.create({
            "prefix_length": prefix_length,
            "description": description,
        }))

    def create_address(self, description: str) -> Address:
        return Address(self.netbox_object.available_ips.create({
            "description": description,
        }))

    def get_or_create_address(self, device_name: str) -> Address:
        api = getattr(nb.ipam, 'ip-addresses')

        existing_ips = api.filter(parent=self.cidr)
        for ip in existing_ips:
            if ip.description == device_name:
                return Address(ip)

        return self.create_address(device_name)

