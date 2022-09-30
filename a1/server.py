#  coding: utf-8 
from email import contentmanager
import socketserver
import re
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #print("Listening...")
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        #split the header to get the requested page
        headers = self.data.decode().split('\n')
        headers = re.split(" ", self.data.decode())
        file_type = headers[1].split(".")

        url = headers[1]
        method_name = headers[0]

        if method_name == "GET":

            # change directory to www/
            www_dir = os.curdir + "/www"

            try:
                # default response variables
                status_code = 200
                status_desc = "OK"

                # get the index page if the url ends with a slash '/'
                # get the right content type
                if url.endswith('/'):
                    url += "index.html"
                    content_type = "text/html"
                else:
                    if len(file_type) <= 1:
                        url += "/index.html"
                        status_code = 301
                        status_desc = "Moved Permanently"
                        content_type = "text/html"
                    else:
                        if file_type[1] == "css":
                            content_type = "text/css"
                        elif file_type[1] == "html":
                            content_type = "text/html"
                        else:
                            response = 'HTTP/1.1 404 NOT FOUND\r\n\r\nFile Not Found'
                            self.request.sendall(response.encode())
                            exit()

                # open the path requested and read the contents
                path_to_open = www_dir + url
                get_file = open(path_to_open)
                content = get_file.read()
                get_file.close()

                # send response back to client
                response = f"HTTP/1.1 {status_code} {status_desc}\r\nContent-type: {content_type}\r\n{content}\n"
            except:
                response = 'HTTP/1.1 404 NOT FOUND\r\n\r\nFile Not Found'
        else:
            response = 'HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed'

        # send data to client
        self.request.sendall(response.encode())
        #print(response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    #server.server_bind()

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
