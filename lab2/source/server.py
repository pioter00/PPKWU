#!/usr/bin/env python3
import http.server
import socketserver
import os
import datetime as dt
import pytz
from urllib.parse import urlparse
from urllib.parse import parse_qs

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        now = dt.datetime.now(pytz.timezone('Europe/Warsaw'))
        time = now.strftime("%H:%M:%S") + "\n"
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        
        if self.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()            
            self.wfile.write(b"Hello World!\n")
            self.wfile.write(time.encode())
        else:
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()            
            self.wfile.write(str(qs).encode())
            # super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
