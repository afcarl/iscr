import math
import numpy as np


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
		return -1 * p * math.log(p/q)

def kl_divergence(p, q):
    # Normalizing is the bottle neck!
    kl_sum = 0.
    for word_idx in p:
        if word_idx in q:
            p_prob = p[word_idx]
            q_prob = q[word_idx]
            kl_sum -= p_prob * math.log(p_prob / q_prob)

    return kl_sum


def evalAP(ret, ans):
    tp = [float(docID in ans) for docID, val in ret]
    atp = np.cumsum(tp)

    precision = [atp[idx] / (idx + 1)
                 for idx, (docID, val) in enumerate(ret) if tp[idx]]

    return (sum(precision) / len(ans) if len(ans) else 0.)
