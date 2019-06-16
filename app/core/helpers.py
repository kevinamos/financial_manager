import random


def random_color():
    return f'#{"".join([random.choice("0123456789ABCDEF") for _ in range(6)])}'