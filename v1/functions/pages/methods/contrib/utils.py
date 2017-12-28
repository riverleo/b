import random
from string import digits, ascii_letters


def create_random_key(length=10, digit_only=False):
    source = digits if digit_only else digits + ascii_letters

    return ''.join(random.choice(source) for _ in range(length))
