#!/usr/bin/env python3
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
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = data.split(" ")
        return int(code[1])

    def get_headers(self, response):
        return None 

    def get_body(self, data):
        # get everything after the final \r\n\r\n (header end)
        body = data.split("\r\n\r\n")[1]
        return body

    def parse_url(self, url):
        host = ""
        path = ""

        # remove http://
        if "http://" in url:
            split_url = url[7:].split("/")
        else:
            split_url = url

        # parse url, separate host and path
        host = split_url[0]

        if len(split_url) >= 2:
            for i in range(1, len(split_url)):
                path += "/" + split_url[i]
        else:
            path = "/"

        # get port if there is one (local host)
        try:
            port = host.split(":")[1]
            host = host.split(":")[0]
        except:
            port = 80

        return [host, port, path]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

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
        return buffer.decode('utf-8')

    def GET(self, url, args=None):

        # parse url
        parsed_url = self.parse_url(url)
        host = parsed_url[0]
        port = int(parsed_url[1])
        path = parsed_url[2]

        # connect to socket
        # source: https://stackoverflow.com/questions/47658584/implementing-http-client-with-sockets-without-http-libraries-with-python
        self.connect(host, port)

        # send request
        message = f'GET {path} HTTP/1.0\r\n'
        message += f'Host: {host}\r\n\r\n'
        self.sendall(message)

        # recieve data
        data = b""
        data = self.recvall(self.socket)
        self.close()

        # call helpers to get code and body
        code = self.get_code(data)
        body = self.get_body(data)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):

        # parse url
        parsed_url = self.parse_url(url)
        host = parsed_url[0]
        port = int(parsed_url[1])
        path = parsed_url[2]

        # connect to socket
        self.connect(host, port)
            
        # format args if any
        params = ''
        if args is not None:
            params = urllib.parse.urlencode(args)
            content_length = len(params)
            print(f'Content_length = {content_length}')
        else:
            content_length = 0

        # setup headers and send POST request
        # source: https://stackoverflow.com/questions/14551194/how-are-parameters-sent-in-an-http-post-request
        message = f'POST {path} HTTP/1.0\r\n'
        message += f'Host: {host}\r\n'
        message += 'Content-Type: application/x-www-form-urlencoded\r\n'
        message += f'Content-Length: {content_length}\r\n'
        message += 'Accept: */*\r\n'
        message += "\r\n" # end of headers

        message += f'{params}\r\n'
    
        # send request
        self.sendall(message)

        # recieve data
        data = b""
        data = self.recvall(self.socket)
        self.close()

        # # call helpers to get code and body
        code = self.get_code(data)
        body = self.get_body(data)

        return HTTPResponse(code, body)

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
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
