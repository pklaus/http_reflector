#!/usr/bin/env python

"""
Bottle-based HTTP Reflector Client

Exit codes:

0   - Server reachable, returned HTTP status code 200

1   - Reflector server not reachable
2   - Received strange response / not a Reflector server?

128 - The reflector server was checking the address but HTTP status code != 200
129 - The reflector server was checking the address but the expected length didn't match.

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
    parser.add_argument('--expected-length', '-l', type=int, help='Specify a Enable verbose debug mode.')
    parser.add_argument('--debug', action="store_true", help='Enable verbose debug mode.')
    args = parser.parse_args()

    check_address = urllib.parse.quote(args.check_address)
    checkurl = urllib.parse.urljoin(args.reflector_address, '/check/' + check_address)
    if args.debug: print("HTTP request to {}".format(checkurl))
    try:
        response = json.loads(urllib.request.urlopen(checkurl).read().decode('utf-8'))
        if args.debug: print(response)
        if 'status' not in response:
            if args.debug: print("A problem at the server side occured / not a http_reflector server?")
            sys.exit(2)
        if response['status'] == 'error':
            if args.debug: print("The server is not reachable!")
            sys.exit(128)
        if response['status'] == 'success':
            if args.expected_length == None:
                if args.debug: print("The server is reachable!")
                sys.exit(0)
            else:
                if args.expected_length == response['length']:
                    if args.debug: print("The server is reachable and the length fits.")
                    sys.exit(0)
                else:
                    if args.debug: print("The server was reachable but the length didn't fit!")
                    sys.exit(129)
    except urllib.error.URLError as e:
        if args.debug: print("Could not reach the reflector server '{}'! Error: '{}'.".format(args.reflector_address, str(e)))
        sys.exit(1)

if __name__ == '__main__':
    main()

