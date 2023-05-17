#! /usr/bin/env python3

import cgi

our_form = cgi.FieldStorage()

long_url = our_form.getfirst('long_url', 'Пусто')

print('Content-type: text/html')
print()
print(long_url)