import http.server
import string
import random
import csv
import cgi


def save_url(long_url, short_code):
    with open('urls.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([long_url, short_code])


def read_url():
    with open('urls.csv', 'r') as file:
        all_links = {line[0]:line[1:] for line in csv.reader(file)}
    return all_links


def generate_code():
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(6))


class HttpGetHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/short_url':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><head>'
            output += '<meta charset="UTF-8"/>'
            output += '</head><body>'
            output += '<h1>Short URL</h1>'
            output += '<h3><a href="/short_url/new">Сократить ссылку</a></h3>'
            output += '<p>Полный адрес : Сокращенная ссылка</p>'
            output += '<h4>Ваши ссылки</h4>'
            for long_url, short_url in read_url().items():
                output += f'{long_url} : {short_url[0]}'
                output += '<br>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><head>'
            output += '<meta charset="UTF-8"/>'
            output += '</head><body>'
            output += '<h1>Сократить ссылку</h1>'

            output += '<form method="POST" enctype="multipart/form-data" action="/short_url/new">'
            output += '<input name="long_url" type="text" placeholder="Длинная ссылка">'
            output += '<input type="submit" value="Отправить">'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())

        if self.path:
            for long_url, code in read_url().items():
                if self.path[1:] == code[0]:
                    self.send_response(301)
                    self.send_header('Location', long_url)
                    self.end_headers()

    def do_POST(self):
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == "multipart/form-data":
                fields = cgi.parse_multipart(self.rfile, pdict)
                long_url = fields.get('long_url')
                if long_url[0] in read_url().keys():
                    print('Уже есть короткая ссылка')
                    print(read_url()[long_url[0]])
                else:
                    save_url(long_url[0], generate_code())

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/short_url')
            self.end_headers()


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, HttpGetHandler)
    httpd.serve_forever()
