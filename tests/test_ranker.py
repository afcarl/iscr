import os

from iscr.ranker.metrics import normalize
from iscr.ranker import KLRanker
from iscr.utils import load_from_pickle, save_to_pickle


def test_klranker():
    cwd = os.path.dirname(__file__)

    test_collection_dir = os.path.join(cwd, 'PTV.test')
    test_query_pickle = os.path.join(
        test_collection_dir, 'PTV.test.query.pickle')
    test_scores_pickle = os.path.join(
        test_collection_dir, 'PTV.test.scores.pickle')

    test_query = load_from_pickle(test_query_pickle)
    test_scores = load_from_pickle(test_scores_pickle)
    ranker = KLRanker(test_collection_dir)

    for query_idx, test_ret in zip(test_query, test_scores):
        query_lm = normalize(test_query[query_idx]['wordcount'], inplace=False)
        ret = ranker.rank(query_lm)

        assert ret == test_ret
