#!/usr/bin/env python3
import http.server
import socketserver
import os
import datetime as dt
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)         

        if len(qs) == 1 and 'num1' in qs.keys() and 'num2' in qs.keys():
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            num1 = qs['num1'][0]
            num2 = qs['num2'][0]
            if not isinstance(num1, int) or not isinstance(num2, int) or num2 != 0:
                self.wfile.write("Not valid numbers".encode())
            else:
                count_dict = {    
                    "sum" : 0, 
                    "sub" : 0, 
                    "mul" : 0, 
                    "div" : 0,
                    "mod" : 0
                }
                self.wfile.write(json.dumps(count_dict).encode())
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
