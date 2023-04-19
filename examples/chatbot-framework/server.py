import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler


class MyHandler(Handler):
    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"
        return Handler.do_GET(self)


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
