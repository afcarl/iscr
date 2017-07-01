import argparse
import os
import sys
sys.path.append('.')

from iscr.searchengine.indexer import text_to_wordcount
from iscr.utils import load_from_pickle, save_to_pickle

def build_query_answer(lex_dict, query_file, answer_file, out_pickle):
    # Perform query wordcount
    query = {}
    with open(query_file, 'r') as fin:
        for query_idx, line in enumerate(fin.readlines(), 1):
            query[query_idx] = {'wordcount': text_to_wordcount(
                lex_dict, line), 'answer': {} }

    # Load answer
    with open(answer_file) as fin:
        for line in fin.readlines():
            tokens = line.split()
            query_idx = int(tokens[0])
            answer_idx = int(tokens[2][1:])
            query[query_idx]['answer'][ answer_idx ] = 1

    # Save to pickle
    save_to_pickle(out_pickle, query)

    return query


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lex_pickle",type=str,
			default='./iscr/searchengine/data/PTV_onebest_fromMATBN_charSeg/lex.pickle')
    parser.add_argument('--query_file', type=str,
                        default='./data/query/PTV.utf8.jieba.query')
    parser.add_argument('--answer_file', type=str,
                        default='./data/query/PTV.ans')
    parser.add_argument('--out_pickle', type=str,
                        default='./queries/dnn.query.pickle')
    args = parser.parse_args()

    lex_dict = load_from_pickle(args.lex_pickle)

    query_answer = build_query_answer(lex_dict, args.query_file, args.answer_file, args.out_pickle)
