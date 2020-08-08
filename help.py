import re
def split_string(string):
    pattern = re.compile(r'[\W_]+')
    return pattern.sub(' ', string.lower()).split()
