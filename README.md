
### HTTP Reflector

HTTP Reflector is a web server allowing you to check the availability of other web servers.
The name is not perfect. It is not actually "reflecting" your request but rather checking
a given URL for availability .

#### Usage

Start the server:

    $ ./server.py --port 8080

Run the client:

    $ ./client.py --debug http://localhost:8080 http://google.com
    HTTP request to http://localhost:8080/check/http%3A//google.com
    {'length': 17532, 'code': 200, 'status': 'success'}
    The server is reachable!
    $ echo $?
    0
    $ ./client.py --debug http://localhost:8080 http://gogogo.com
    HTTP request to http://localhost:8080/check/http%3A//gogogo.com
    {'details': 'HTTP Error 403: Forbidden', 'kind': 'urllib.error.URLError', 'status': 'error'}
    The server is not reachable!
    $ echo $?
    128


#### ToDO

* Limit requests to 20 per minute?
* Limit IP range?

#### Alternative Implementations

Instead of returning JSON containing the information,
you could just as well replicate the HTTP status of
the contacted server. This would allow simple use
from any client without the Python tool but with standard
`curl` commands and exit codes.  
An extra URL could possibly provide this service.

#### Resources

* A simple IP address reflector: <https://gist.github.com/donavanm/812782>


