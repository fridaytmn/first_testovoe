from http.server import HTTPServer, BaseHTTPRequestHandler
import re


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
        self.send_response(301)
        self.send_header('Location','/support')
        self.end_headers()
        path = self.path
        if path == '/long_link':
            content_len = int(self.headers.get('Content-Length'))
            post = self.rfile.read(content_len)
            link = re.split(r'link=', str(post))[1]
            link = re.sub(r'\'', '', link)
        print(link)
        return


def main():
    server = HTTPServer(('', 8000), HttpGetHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
