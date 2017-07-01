from collections import defaultdict
import os
import sys
import time

from .metrics import normalize, cross_entropy
from ..utils import load_from_pickle


class SearchEngine(object):
    def __init__(self, lex_pickle, index_pickle, build_wordcount=False):

        print("[SearchEngine] Loading lex from {}".format(lex_pickle))
        self.lex_dict = load_from_pickle(lex_pickle)

        print("[SearchEngine] Loading index from {}".format(index_pickle))
        self.indices = load_from_pickle(index_pickle)

        self.docnames = self.indices['doclengs'].keys()

    def refresh_results(self):
        self.result = defaultdict(float)
        for docname in self.docnames:
            self.result[docname] = 0.

    def retrieve(self, query, negquery=None):
        """
            Returns a list of tuples [(docname, score),...]
            For MAP, every docname has to exist
        """
        self.refresh_results()

        self._retrieve(query, 1)
        if negquery is not None:
            self._retrieve(negquery, -0.1)

        sorted_ret = sorted(self.result.items(),
                            key=lambda x: x[1], reverse=True)
        return sorted_ret

    def _retrieve(self, query, entropy_weight=1.):
        # Query
        for wordID, word_prob in query.items():
            # Check if query word intersects with documents
            if wordID not in self.indices['background']:
                continue

            # Recored scored documents for this word
            word_background_prob = self.indices['background'][wordID]
            word_inverted_index = self.indices['inverted_index'][wordID]

            for docID, doclength in self.indices['doclengs'].items():
                # Get doc prob if in inverted_index, else set to 0.
                docprob = word_inverted_index.get(docID, 0.)

                smoothed_docprob = smooth_docprob(
                    docprob, doclength, word_background_prob)

                weighted_entropy = entropy_weight * \
                    cross_entropy(word_prob, smoothed_docprob)
                # Add to result
                self.result[docID] += weighted_entropy


def smooth_docprob(docprob, doclength, word_background_prob, alpha=1000):
    alpha_d = doclength / (doclength + alpha)
    smoothed_docprob = (1 - alpha_d) * word_background_prob + alpha_d * docprob
    return smoothed_docprob


if __name__ == "__main__":
    pass
