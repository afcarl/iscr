import argparse
import os
import sys
import time
sys.path.append('.')

from tqdm import tqdm

from iscr import KLRanker
from iscr.ranker.metrics import normalize
from iscr.evalute import average_precision
from iscr.utils import load_from_pickle


def run_ap_baseline(query_pickle, data_dir):

    ranker = KLRanker(data_dir)

    query = load_from_pickle(query_pickle)

    _start_time = time.time()

    aps = []

    for query_idx in tqdm(query):
        if 'languagemodel' in query[query_idx]:
            query_lm = query[query_idx]['languagemodel']
        else:
            query_lm = normalize(query[query_idx]['wordcount'], inplace=False)

        answer_set = query[query_idx]['answer']

        name_answer_set = {}
        for key, val in answer_set.items():
            docname = 'T' + str(key).zfill(4)
            name_answer_set[docname] = val

        ret = ranker.rank(query_lm, negquery=None)

        # Calculate Mean Average Precision
        ap = average_precision(ret, name_answer_set)
        aps.append(ap)

    # Time end
    _end_time = time.time()
    print("Mean Average Precision: {}".format(sum(aps) / len(aps)))
    print("Time taken: {} seconds".format(_end_time - _start_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query_pickle', type=str,
                        default='./queries/PTV.dnn.onebest.jieba.query.pickle')
    parser.add_argument('-d', '--data_dir', type=str,
                        default='./iscr/ranker/collections/PTV.dnn.onebest.jieba')
    args = parser.parse_args()

    run_ap_baseline(args.query_pickle, args.data_dir)
