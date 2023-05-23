from http.server import HTTPServer, CGIHTTPRequestHandler


if __name__ == '__main__':
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
    httpd.serve_forever()
