from http.server import HTTPServer, BaseHTTPRequestHandler


class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        path = self.path
        if path == '/':
            path = '/index'

        try:
            file = open(f'cgi-bin{path}.html', 'r', encoding='utf-8')
        except FileNotFoundError:
            pass

        message = file.read()
        file.close()
        self.wfile.write(bytes(message, encoding='UTF-8'))
        return

    def do_POST(self):
        self.send_response(501)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Proverka'.encode())


def main():
    server = HTTPServer(('', 8000), HttpGetHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
