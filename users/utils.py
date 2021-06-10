from itertools import tee


def pairwise(seq):
    a, b = tee(seq)
    next(b)
    return zip(a, b)
