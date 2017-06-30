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


def evalAP(ret, ans):
    tp = [float(docID in ans) for docID, val in ret]

    precisions = []
    ans_count = 0
    for idx, (docID, val) in enumerate(ret):
        ans_count += tp[idx]
        precisions.append(ans_count / (idx + 1) * tp[idx])

    return (sum(precisions) / len(ans) if len(ans) else 0.)
