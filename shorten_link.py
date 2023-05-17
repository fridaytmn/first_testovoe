import csv
import string
import random


def generate_code(length: int) -> str:
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def add_url(url: str) -> str:
    with open('urls.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        code = generate_code(6)
        writer.writerow([url, code])
    return code


def get_url(code: str) -> str:
    with open('urls.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == code:
                return row[0]
    return None


def main():
    pass


if __name__ == '__main__':
    main()