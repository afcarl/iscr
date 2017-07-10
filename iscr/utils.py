import math
import pickle

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

def load_from_pickle(filename):
    with open(filename, 'rb') as fin:
        return pickle.load(fin)


def save_to_pickle(filename, obj):
    with open(filename, 'wb') as fout:
        pickle.dump(obj, fout)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
