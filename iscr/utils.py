import json
import math
import pickle


def load_from_pickle(filename):
    with open(filename, 'rb') as fin:
        return pickle.load(fin)


def save_to_pickle(filename, obj):
    with open(filename, 'wb') as fout:
        pickle.dump(obj, fout)


def load_from_json(filename):
    with open(filename, 'r') as fin:
        return json.load(fin)


def save_to_json(filename, obj):
    with open(filename, 'w') as fout:
        json.dump(obj, fout, ensure_ascii=False, sort_keys=True, indent=4)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])