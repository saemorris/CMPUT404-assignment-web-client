#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
import urlparse 

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

# create a request object
class HTTPRequest(object):

    def __init__(self, method, url, args=""):

        # parse the url
        parsed = urlparse.urlsplit(url) 

        self.method = method

        self.path = parsed.path
        if not self.path:
            self.path = "/"

        self.host = parsed.hostname

        self.port = parsed.port
        if not self.port:
            self.port = 80

        if args:
            self.body = urllib.urlencode(args)
        else:
            self.body = ""

    def getRequest(self):
        headers = self.requestHeaders()
        return headers + self.body

    def requestHeaders(self):
        protocol = "HTTP/1.1"

        first = self.method + " " +  self.path + " " + protocol + "\r\n"
        host = "Host: " + self.host + ":" + str(self.port) + "\r\n"
        type = "Content-type: application/x-www-form-urlencoded\r\n"
        length = "Content-length: " + str(len(self.body)) + "\r\n"
        accept = "Accept: */*\r\n"
        close = "Connection: close\r\n"

        return first + host + type + length + accept + close + "\r\n"

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):

        # Joshua Campbell, Cmput 404 Lab 2
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((str(host), int(port)))

        return sock

    def get_code(self, data):
        code = data.split("\r\n")[0].split(" ")[1]
        return code

    def get_headers(self,data):
        return None

    def get_body(self, data):
        body = "" if len(data.split("\r\n\r\n", 1)) == 1 else data.split("\r\n\r\n", 1)[-1]

        return body 

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
         # create the request
        request = HTTPRequest("GET", url, args)

        # open a connection and send the request
        socket = self.connect(request.host, request.port)
        socket.sendall(request.getRequest())

        response = self.recvall(socket)

        code = self.get_code(response) 
        body = self.get_body(response)
        return HTTPResponse(int(code), body)

    def POST(self, url, args=None):
        request = HTTPRequest("POST", url, args)

        socket = self.connect(request.host, request.port)
        socket.sendall(request.getRequest())

        response = self.recvall(socket)

        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(int(code), body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
