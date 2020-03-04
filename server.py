import http.server
import os
import socketserver

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT"))
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
