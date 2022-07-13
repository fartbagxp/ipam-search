import ipaddress
import pynetbox
from pprint import pprint

nb = pynetbox.api(
    'http://localhost:32768',
    token='0123456789abcdef0123456789abcdef01234567'
)


def search(term, field=None):

  # use the field as the field to search if it
  # is defined to provide an better search category
  guess_field = ''
  if field != None:
    guess_field = field

  # validate that the term is an IP address or a CIDR notation range
  # if it's not, the search category shouldn't be IP based
  # use one of the other fields for searching
  isValidParameter = False
  try:
    ipaddress.ip_address(term)
    isValidParameter = True
  except ValueError:
    pass

  try:
    ipaddress.ip_network(term)
    isValidParameter = True
  except ValueError:
    pass

  if isValidParameter:
    nyse_pfxs = nb.ipam.prefixes.filter(q=term)
    for pfx in nyse_pfxs:
      pprint(pfx.__dict__)

  else:
    available_field = [
        'cf_appid',
        'cf_environment'
    ]

    for field in available_field:
      search_field = {}
      search_field[field] = term.lower()
      print(field, term)
      nyse_pfxs = nb.ipam.prefixes.filter(**search_field)
      print(len(nyse_pfxs))
      # for pfx in nyse_pfxs:
      #   pprint(pfx.__dict__)


def main():
  term = "green"
  search(term)

  term = "192.168.1.0"
  search(term)


if __name__ == "__main__":
  main()
