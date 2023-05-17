import csv
import string
import random


def generate_code():
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(6))


def add_url(long_url):
    code = generate_code()
    with open('urls.csv', 'a', encoding='utf-8', newline='') as file:
        fieldnames = ['long_url', 'short_url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'long_url': long_url,
                            'short_url': code})

    #     with open('urls.csv', 'w', encoding='utf-8', newline='') as file:
    #         fieldnames = ['long_url', 'short_url']
    #         writer = csv.DictWriter(file, fieldnames=fieldnames)
    #         writer.writeheader()
    #         add_url(long_url)


def get_url(long_url):
    with open('urls.csv', newline='') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            print(row['long_url'])


if __name__ == '__main__':
    add_url('https://ya.ru')
    # get_url('https://ya.ru')
