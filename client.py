#!/usr/bin/env python

"""
Bottle-based HTTP Reflector Client

Exit codes:

0   - Server reachable, returned HTTP status code 200

2   - Error parsing your CLI arguments

16  - Reflector server not reachable
17  - Received strange response / not a Reflector server?

128 - The reflector server was checking the address but HTTP status code != 200
129 - The reflector server was checking the address but the expected length didn't match.

"""

import sys
import json
import urllib.request
import urllib.parse
import argparse

def parse_range(string):
    parts = string.split('-')
    if len(parts) == 1:
        parts.append(parts[0])
    if len(parts) != 2:
        raise ArgumentTypeError("{} is not a range. Expected something like '0-5' or '2100'.".format(string))
    return range(int(parts[0],10), int(parts[1],10)+1)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reflector_address', help='The address of your reflector server.')
    parser.add_argument('check_address', help='The address of the server you want to check.')
    parser.add_argument('--expected-length', '-l', type=parse_range, help='Specify a Enable verbose debug mode.')
    parser.add_argument('--debug', action="store_true", help='Enable verbose debug mode.')
    args = parser.parse_args()

    if not (args.reflector_address.startswith('http://') or args.reflector_address.startswith('https://')):
        args.reflector_address = 'http://' + args.reflector_address
    check_address = urllib.parse.quote(args.check_address)
    checkurl = urllib.parse.urljoin(args.reflector_address, '/check/' + check_address)
    if args.debug: print("HTTP request to {}".format(checkurl))
    try:
        response = json.loads(urllib.request.urlopen(checkurl).read().decode('utf-8'))
        if args.debug: print(response)
        if 'status' not in response:
            if args.debug: print("A problem at the server side occured / not a http_reflector server?")
            sys.exit(17)
        if response['status'] == 'error':
            if args.debug: print("The server is not reachable!")
            sys.exit(128)
        if response['status'] == 'success':
            if args.expected_length == None:
                if args.debug: print("The server is reachable!")
                sys.exit(0)
            else:
                if response['length'] in args.expected_length:
                    if args.debug: print("The server is reachable and the length fits.")
                    sys.exit(0)
                else:
                    if args.debug: print("The server was reachable but the length didn't fit!")
                    sys.exit(129)
    except urllib.error.URLError as e:
        if args.debug: print("Could not reach the reflector server '{}'! Error: '{}'.".format(args.reflector_address, str(e)))
        sys.exit(16)

if __name__ == '__main__':
    main()

