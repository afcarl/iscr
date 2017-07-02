import math

def normalize(d, inplace=False):
    total = sum(d.values())
    if inplace is True:
        for k, v in d.items():
            d[k] = v / total
    else:
        norm_d = {}
        for k, v in d.items():
            norm_d[k] = v / total
        return norm_d


def cross_entropy(p, q):
    if q == 0:
        return 0
    else:
        return -1 * p * math.log(p / q)
