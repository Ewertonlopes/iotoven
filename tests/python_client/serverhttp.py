import http.server
import socketserver
import numpy as np

# Define the port number you want to use (e.g., 8000)
port = 8000
i = 1
# Create a custom request handler to specify the response

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global i
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        i = np.random.randint(1,50)
        response = f'{i}'
        self.wfile.write(response.encode('utf-8'))

# Create the HTTP server with your custom request handler
with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"Serving at port {port}")
    httpd.serve_forever()