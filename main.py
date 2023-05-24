import http.server
import string
import random
import csv
import cgi


def check_in_db(long_url):
    if long_url in read_url().keys():
        short_link = f'http://212.76.162.88:8888/{read_url()[long_url][0]}'
    else:
        save_url(long_url, generate_code())
    short_link = f'http://212.76.162.88:8888/{read_url()[long_url][0]}'
    return short_link


def save_url(long_url, short_code):
    with open('urls.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([long_url, short_code])


def read_url():
    with open('urls.csv', 'r') as file:
        all_links = {line[0]: line[1:] for line in csv.reader(file)}
    return all_links


def generate_code():
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(6))


class HttpGetHandler(http.server.CGIHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            output = ''
            output += '<html><head>'
            output += '<meta charset="UTF-8"/>'
            output += '</head><body>'
            output += '<h1>Short URL</h1>'
            output += '<h3><a href="/new">Сократить ссылку</a></h3>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><head>'
            output += '<meta charset="UTF-8"/>'
            output += '</head><body>'
            output += '<h1>Сократить ссылку</h1>'
            output += '<form action="/result" method="POST">'
            output += '<input name="long_url" type="text" placeholder="Длинная ссылка">'
            output += '<input type="submit" value="Отправить">'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())

        if self.path[1:] in [link[0] for link in read_url().values()]:
            for long_url, code in read_url().items():
                if self.path[1:] == code[0]:
                    self.send_response(301)
                    self.send_header('Location', long_url)
                    self.end_headers()

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                })

            url = form.getvalue('long_url')
            output = ''
            output += '<html><head>'
            output += '''<script>
            function copyText() {
            navigator.clipboard.writeText
            ('%s');}
            </script>''' % check_in_db(url)
            output += '<meta charset="UTF-8"/>'
            output += '</head><body>'
            output += '<h1>Результат сокращения</h1>'
            output += f'{check_in_db(url)}  '
            output += '<input type="submit" value="Копировать" onclick="copyText()">'
            output += '</form>'
            output += '</body></html>'

            # self.wfile.write(output.encode())
        except:
            self.send_error(404, 'Bad request submitted.')
        self.end_headers()
        self.wfile.write(bytes(output, 'utf-8'))


if __name__ == '__main__':
    server_address = ('', 8888)
    httpd = http.server.HTTPServer(server_address, HttpGetHandler)
    httpd.serve_forever()