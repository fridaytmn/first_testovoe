#!/usr/bin/env python3

import cgi
import html
import csv
import string
import random
import os

form = cgi.FieldStorage()
long_url = form.getfirst("long_url", "не задано")
long_url = html.escape(long_url)



def check_in_db(long_url):
    if long_url in read_url().keys():
        short_link = f'http://localhost:8000/{read_url()[long_url][0]}'
    else:
        save_url(long_url, generate_code())
    short_link = f'http://localhost:8000/{read_url()[long_url][0]}'
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


print("Content-type: text/html\n")
print('''<!DOCTYPE HTML>
        <html>
        <head>
            <script>
            function copyText() {
            navigator.clipboard.writeText
            ('%s');}
            </script>
            <meta charset="UTF-8"/>
            <title>Your short link</title>
        </head>
        <body>''' % check_in_db(long_url))
print(os.environ)
print("<h1>Your short link!</h1>")
print(f'<p>Short_link: {check_in_db(long_url)}</p>')
print('<input type="submit" value="Copy" onclick="copyText()">')
print("""</body>
        </html>""")