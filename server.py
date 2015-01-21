#!/usr/bin/env python

"""
Bottle-based HTTP Reflector
"""

import sys
from bottle import route, run
import urllib.request
import urllib.parse

@route('/check/<address:path>')
def urls(address):
    """ Checks HTTP connection to address """
    address = urllib.parse.unquote(address)
    if not (address.startswith('http://') or address.startswith('https://')):
        address = 'http://' + address
    try:
        http_response = urllib.request.urlopen(address)
    except urllib.error.URLError as e:
        return dict(status='error', kind='urllib.error.URLError', details=str(e))
    code = http_response.getcode()
    length = len(http_response.read())
    if code == 200:
        return dict(status='success', code=code, length=length)
    return dict(status='error', kind='HTTP.Code', code=code)

def main():
    import argparse
    import socket
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server-adapter', default='cherrypy', help='Which server to run this web app on. (If you only want IPv4, you may use "wsgiref").')
    parser.add_argument('--base-url', default='http://{}/'.format(socket.gethostname()), help='The base URL of this service.')
    parser.add_argument('--host', default='::', help='The host/IP to bind the server to. Use "0.0.0.0" if you want IPv4 only.')
    parser.add_argument('--port', default=8080, type=int, help='The port the server should listen at. Default: 8080.')
    parser.add_argument('--debug', action='store_true', help='Enable debugging mode.')

    args = parser.parse_args()

    BASE_URL = args.base_url

    run(server=args.server_adapter, host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()

