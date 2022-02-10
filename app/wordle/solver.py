import random

from . import dictionary


def choose_random_word():
    word = random.choice(dictionary.fives)
    return word
