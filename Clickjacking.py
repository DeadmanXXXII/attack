from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser

# HTML code for the redirection page
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clickjacked!</title>
</head>
<body>
    <h1>You have been clickjacked by DeadmanXXXII</h1>
    <p>My report for the bug bounty program will be submitted shortly.</p>
</body>
</html>
"""

# HTTP request handler class
class RequestHandler(BaseHTTPRequestHandler):
    # Handle GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_code.encode())

# Function to start the server
def start_server():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server started on http://0.0.0.0:8000')
    httpd.serve_forever()

# Function to open the browser with the target URLs
def open_browser_with_targets():
    target_urls = [
        "https://whatsapp.com/XsUVyEpy.asp",
        "http://whatsapp.com/XsUVyEpy.asp",
        "https://api.whatsapp.com/XsUVyEpy.asp",
        "http://api.whatsapp.com/XsUVyEpy.asp",
        "http://whatsapp.com/login",
        "https://whatsapp.com/login",
        "http://api.whatsapp.com",
        "https://api.whatsapp.com"
    ]
    for url in target_urls:
        webbrowser.open_new_tab(url)

if __name__ == "__main__":
    open_browser_with_targets()
    start_server()