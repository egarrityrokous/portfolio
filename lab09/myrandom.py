import random

def randint(start, end):
    default = random.randint(0, 100000000)
    random.seed(default)
    val = random.randint(start, end)
    return val
