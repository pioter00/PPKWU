#!/usr/bin/env python3
import http.server
import socketserver
import os
import datetime as dt
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json

class web_server(http.server.SimpleHTTPRequestHandler):
    def count_letters(self, expression):
        to_count_str = expression['str']
        return {
            "lowercase" : sum(map(str.islower, to_count_str)), 
            "uppercase" : sum(map(str.isupper, to_count_str)), 
            "digits" : sum(map(str.isdigit, to_count_str)), 
            "special" : len(to_count_str) - sum(map(str.islower, to_count_str)) - sum(map(str.isupper, to_count_str)) - sum(map(str.isdigit, to_count_str))
        }
    def count_expression(self, expression):
        num1 = expression['num1']
        num2 = expression['num2']
        return {    
            "sum" : num1 + num2, 
            "sub" : num1 - num2, 
            "mul" : num1 * num2, 
            "div" : int(num1 / num2),
            "mod" : num1 % num2
        }
    def do_POST(self):
        final_dict = {}
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.end_headers()
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        expression = json.loads(data_string)
        if 'num1' in expression.keys() and 'num2' in expression.keys():
            if expression['num2'] == 0 or type(expression['num1']) != int or type(expression['num2']) != int:
                self.wfile.write("Not valid numbers".encode())
                return
            final_dict.update(self.count_expression(expression))
        if 'str' in expression.keys():
            final_dict.update(self.count_letters(expression))
        
        self.wfile.write(json.dumps(final_dict).encode())

# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
