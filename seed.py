import os
import pynetbox
from pprint import pprint

nb = pynetbox.api(
    'http://localhost:8000',
    token='0123456789abcdef0123456789abcdef01234567'
)

####
####
# Custom fields must be added manually via the admin portal.
# http://localhost:8000/admin/extras/customfield/add/
# Add the "appid" and "environment" custom fields under ipam/prefix for this
# to work properly. According to the netbox contributor, this functionality
# was intentionally not exposed via the API for security purposes.
#
####
####


SITES = [
    {
        "name": "Avalon-Datacenter",
        "slug": "avalon-datacenter",
        "physical_address": "N/A",
        "tags": []
    },
    {
        "name": "Splinx-Datacenter",
        "slug": "splinx-datacenter",
        "physical_address": "in the cloud",
        "tags": []
    }
]

PREFIXES = [
    {
        "prefix": "192.168.1.0/24",
        "tags": [],
        "description": "",
        "custom_fields": {
            "appid": "blue",
            "environment": "dev"
        }
    },
    {
        "prefix": "192.168.2.0/24",
        "tags": [],
        "description": "",
        "custom_fields": {
            "appid": "red",
            "environment": "prod"
        }
    },
    {
        "prefix": "192.168.3.0/24",
        "tags": [],
        "description": "",
        "custom_fields": {
            "appid": "green",
            "environment": "staging"
        }
    },
    {
        "prefix": "192.168.4.0/24",
        "tags": [],
        "description": "",
        "custom_fields": {
            "appid": "yellow",
            "environment": "prod"
        }
    },
    {
        "prefix": "192.168.5.0/24",
        "tags": [],
        "description": "",
        "custom_fields": {
            "appid": "white",
            "environment": "dev"
        }
    },
]


def create_sites():
  results = nb.dcim.sites.all()
  for result in results:
    result = str(result)
    if result == SITES[0].get("name"):
      print("seeding sites previously completed")
      return

  print("seeding sites into database")
  for site in SITES:
    try:
      result = nb.dcim.sites.create(
          name=site.get('name'),
          slug=site.get('slug'),
          physical_address=site.get('physical_address'),
          tags=site.get('tags'),
      )
      print(result)
    except pynetbox.RequestError as e:
      print(e.error)
  print("seeding sites completed")


def create_prefix():
  results = nb.ipam.prefixes.all()
  for result in results:
    result = str(result)
    if result == PREFIXES[0].get("prefix"):
      print("seeding prefixes previously completed")
      return

  print("seeding prefixes")
  for prefix in PREFIXES:
    try:
      prefix_attr = {
          "prefix": prefix.get('prefix'),
          "tags": prefix.get('tags'),
          "description": prefix.get('description'),
          "custom_fields": {
              "appid": prefix.get('appid'),
              "environment": prefix.get('environment')
          }
      }
      pfx = nb.ipam.prefixes.create(prefix_attr)
      # pprint(dict(pfx))  # for debugging purposes
    except pynetbox.RequestError as e:
      print(e.error)
  print("seeding prefixes completed")


def seed():
  create_sites()
  create_prefix()


def main():
  seed()


if __name__ == "__main__":
  main()
