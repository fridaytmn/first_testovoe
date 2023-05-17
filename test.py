import csv
import string
import random


def generate_code():
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(6))


def add_url(long_url):
    if long_url not in [i[0] for i in get_url()]:
        code = generate_code()
        with open('urls.csv', 'a', encoding='utf-8', newline='') as file:
            fieldnames = ['long_url', 'short_url']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'long_url': long_url,
                            'short_url': code})
        return [i[1] for i in get_url() if i[0] == long_url][0]
    else:
        long_url = [i[0] for i in get_url() if i[0] == long_url][0]
    return f'Ваша ссылка "{long_url}" уже есть в базе'

    #     with open('urls.csv', 'w', encoding='utf-8', newline='') as file:
    #         fieldnames = ['long_url', 'short_url']
    #         writer = csv.DictWriter(file, fieldnames=fieldnames)
    #         writer.writeheader()
    #         add_url(long_url)


def get_url():
    list_long_url = []
    with open('urls.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            list_long_url.append(row)
    return list_long_url


if __name__ == '__main__':
    print(add_url('https://ya.1ru'))
    #get_url()
