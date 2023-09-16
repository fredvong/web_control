# Write a http program to have a button in the middle

from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# This is html page content. It has a button in the middle
# The button has two events: press and release
# When the button is pressed, it will call the function press()
# When the button is released, it will call the function release()\
# press() function will call the /pressed path and release() function
# will call the /released path
html_page = """
<html>
<head>
<title>Control</title>
</head>
<body>
<script>
function press() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/pressed", true);
    xhttp.send();
}
function release() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/released", true);
    xhttp.send();
}
</script>
<button onmousedown="press()" onmouseup="release()">Click me</button>
</body>
</html>
"""


def press_command():
    # this function execute the echo command in bash to print the string "Key pressed"
    # to the terminal
    os.system("echo 'Key pressed'")


def release_command():
    # this function execute the echo command in bash to print the string "Key released"
    # to the terminal
    os.system("echo 'Key released'")


def render_button_page(handler:   BaseHTTPRequestHandler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html; charset=utf-8')
    handler.end_headers()
    # write the html_page to the client
    handler.wfile.write(html_page.encode())


def handle_key_pressed(handler: BaseHTTPRequestHandler):
    handler.send_response(201)
    handler.send_header('Content-type', 'text/html; charset=utf-8')
    handler.end_headers()
    press_command()
    # write the html_page to the client
    handler.wfile.write(b'ok')


def handle_key_released(handler: BaseHTTPRequestHandler):
    handler.send_response(201)
    handler.send_header('Content-type', 'text/html; charset=utf-8')
    handler.end_headers()
    release_command()
    # write the html_page to the client
    handler.wfile.write(b'ok')


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # check if the path requested is the root path, i.e. '/'
        # /released or /pressed, then call the appropriate function
        if self.path == '/':
            render_button_page(self)
        elif self.path == '/pressed':
            handle_key_pressed(self)
        elif self.path == '/released':
            handle_key_released(self)


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HelloHandler)
    print("Starting server at port http://localhost:8000")
    httpd.serve_forever()

