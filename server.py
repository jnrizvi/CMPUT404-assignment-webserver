#  coding: utf-8 
import socketserver
import re
# from PIL import Image

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


# FROM:  https://stackoverflow.com/questions/47726865/html-page-not-displaying-using-python-socket-programming 2021-01-27 by lappet 2017
# filename = 'static/index.html'
# f = open(filename, 'r')

# csock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
# csock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
# csock.send(str.encode('\r\n'))
# # send data per line
# for l in f.readlines():
#     print('Sent ', repr(l))
#     csock.sendall(str.encode(""+l+"", 'iso-8859-1'))
#     l = f.read(1024)
# f.close()
# END FROM

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # Need to parse the self.data. Look at the path to see which file/folder should be returned. Look at HTTP method and see if its GET. POST/PUT/DELETE not supported
        # print ("Got a request of: %s\n" % self.data)
        print(self.data)

        request_snippet = self.data.decode("utf-8").split("?")[0]

        # Just grab the HTTP method and the file path using a regular expression
        method_and_path = re.match(r"GET\s\/([A-Za-z]+\.[A-Za-z]+)?", request_snippet).group().split(" ")
        print(method_and_path)

        # from self.data, extract the path to know which files should be sent
        filename = 'www/index.html'
        if method_and_path[1] != "/":
            filename = "www" + method_and_path[1]

        # f = ""
        # if "ico" in method_and_path[1]:
        #     f = Image.open(filename)
        # else:
        f = open(filename, "r")

        l = f.read()
    
        self.request.sendall(bytearray("HTTP/1.1 200 OK\n",'utf-8'))

        mimetype = "text/html"
        if "css" in method_and_path[1]:
            mimetype = "text/css"

        self.request.sendall(bytearray(f'Content-Type: {mimetype}\n', 'utf-8'))
        self.request.send(bytearray('\n', 'utf-8'))
        self.request.sendall(bytearray(""+l+"", 'utf-8'))
        f.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

# # Reading the file and sending it
# python3 -m http.server
# # Check against it? What do you mean?
# GET http://127

