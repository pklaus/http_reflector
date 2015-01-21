#!/usr/bin/env python

"""
Bottle-based HTTP Reflector Client
"""

import sys
import json
import urllib.request
import urllib.parse

def main():
    import argparse
    import socket
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reflector_address', help='The address of your reflector server.')
    parser.add_argument('check_address', help='The address of the server you want to check.')
    args = parser.parse_args()

    check_address = urllib.parse.quote(args.check_address)
    checkurl = urllib.parse.urljoin(args.reflector_address, '/check/' + check_address)
    print("HTTP request to {}".format(checkurl))
    try:
        response = json.loads(urllib.request.urlopen(checkurl).read().decode('utf-8'))
        print(response)
    except urllib.error.URLError as e:
        print("Could not reach the reflector server '{}'. Error: '{}'.".format(args.reflector_address, str(e)))
        sys.exit(1)

if __name__ == '__main__':
    main()

