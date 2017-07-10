import math

def cross_entropy(p, q):
	if q == 0:
		return 0
	else:
		return -1 * p * math.log(p / q)
