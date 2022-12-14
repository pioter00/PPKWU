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

        if len(qs) == 1 and 'str' in qs.keys():
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            to_count_str = qs['str'][0]
            count_dict = {
                "lowercase" : sum(map(str.islower, to_count_str)), 
                "uppercase" : sum(map(str.isupper, to_count_str)), 
                "digits" : sum(map(str.isdigit, to_count_str)), 
                "special" : len(to_count_str) - sum(map(str.islower, to_count_str)) - sum(map(str.isupper, to_count_str)) - sum(map(str.isdigit, to_count_str))
            }
            self.wfile.write(json.dumps(count_dict).encode())
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
