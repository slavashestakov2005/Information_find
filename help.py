import sys
import re


def start():
    sys.stdout = open('output.txt', 'w')
    with open('log.txt', 'w') as file:
        file.write('Fail')


def finish():
    with open('log.txt', 'w') as file:
        file.write('Ok')


def split_string(string):
    pattern = re.compile(r'[\W_]+')
    return pattern.sub(' ', string.lower()).split()
