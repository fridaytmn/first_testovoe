import http.server
import string
import json
import random
import csv


class HttpGetHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('''
                <html>
                    <head>
                        <meta charset="UTF-8"/>
                    </head>
                    <body>
                        <form method="POST">
                            <label for="long_url">Длинный URL:</label><br>
                            <input type="text" id="long_url" name="long_url"><br>
                            <button type="submit">Отправить</button>
                        </form>
                    </body>
                </html>
            '''.encode())

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            long_url = post_data
            short_code = self.generate_code()
            self.save_url(long_url, short_code)
            response = {
                'short_url': f'http://{self.server.server_name}:{self.server.server_port}/{short_code}'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write('Короткая ссылка '.encode())
            self.wfile.write(json.dumps(response['short_url']).encode())
            self.wfile.write(json.dumps(self.read_url()).encode())

    def generate_code(self):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for i in range(6))

    # def save_url(self, long_url, short_code):
    #     with open('urls.csv', mode='ab') as file:
    #         link = {'code': short_code,
    #                 'long_url': long_url}
    #         csv.dump(link, file)

    # def read_url(self):
    #     all_urls = []
    #     with open('urls.csv', 'rb') as file:
    #         all_urls = csv.load(file)
    #     for key, value in all_urls.items():
    #         print(key, value)


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, HttpGetHandler)
    httpd.serve_forever()
