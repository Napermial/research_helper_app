from itertools import tee


def pairwise(seq):
    """:returns the next iterator of the sequence"""
    a, b = tee(seq)
    next(b)
    return zip(a, b)
