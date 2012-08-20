#!/usr/bin/python
"""This server logs data about commit received with POST request. 
You can close it using command 'stop' in POST request."""

import BaseHTTPServer
import cgi
import json
import logging
import socket
import sys
import time
from SocketServer import ThreadingMixIn

DEBUG = True       # Turn on debug mode, turn off logging. test.py needs DEBUG = True
running = True      # Flag for stopping the server with command "stop"


class ThreadingServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """Multithreading server class."""
    
    daemon_threads = True
    allow_reuse_address = True

    # Overriden function for closing server using "stop"
    def close_request(self, request):
        request.close()
        if not running:
            self.shutdown()
        

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """HTTP request handler class."""
    
    debug_info = ''
   
    def do_POST(self):
        """Process POST request."""
        global running
        content_len = int(self.headers.getheader('content-length'))
        req = dict(cgi.parse_qsl(self.rfile.read(content_len)))
        self.info = json.loads(req.get('info', '0'))
        if req.get('command', 0) == 'stop':
            running = False
        elif self.info:
            self.log()
        else:
            print "INCORRECT DATA"
        self.send_response(200)

    def log(self):
        """Logging commit info."""
        if not DEBUG:
            logging.basicConfig(filename=r'commit.log', level=logging.INFO)
            logging.info(' START: Server Time: ' + time.asctime() + '\nRepo url: %(repo_url)s\
            \nRepo: %(repo)s\nBranch: %(branch)s\nHash: %(commit_hash)s\nCommit time: %(time)s\nEND\n' % self.info)
        else:
            print "\nIN DEBUG MODE\n"
            MyHandler.debug_info = ' START: Server Time: ' + time.asctime() + '\nRepo url: %(repo_url)s\
            \nRepo: %(repo)s\nBranch: %(branch)s\nHash: %(commit_hash)s\nCommit time: %(time)s\nEND\n' % self.info


def run(server_class = ThreadingServer, handler_class = MyHandler):
    """Run server"""
    server_address = ('localhost', 13000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    return 0

if __name__ == '__main__':
    status = run()
    sys.exit(status)
    
