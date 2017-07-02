import os

from .metrics import cross_entropy
from ..utils import load_from_pickle

__all__ = ["KLRanker"]


class BaseRanker(object):
    def __init__(self, collection_dir):
        """
            Loads pickled lex and indices from collection directory
        """
        lex_pickle = os.path.join(collection_dir, 'lex.pickle')
        print("[Ranker] Loading lex from {}".format(lex_pickle))
        self._lex_dict = load_from_pickle(lex_pickle)

        index_pickle = os.path.join(collection_dir, 'indices.pickle')
        print("[Ranker] Loading index from {}".format(index_pickle))
        self._indices = load_from_pickle(index_pickle)

        print("[Ranker] Initializing document scores")
        self.init_docscores()

    def __call__(self, collection_dir):
        """
            Reloads lex and indices from collection_dir
        """
        self.__init__(collection_dir)

    def init_docscores(self):
        self._docscores = {}
        for docname in self._indices['doclengs']:
            self._docscores[docname] = 0.
        return self._docscores

    def refresh_docscores(self):
        for docname in self._docscores:
            self._docscores[docname] = 0.
        return self._docscores

    def rank(self, query, negquery=None):
        """
            Argument:
			    - query:
			        a language model dictionary,
			        with entropy_weight set at 1.0
			    - (Optional) negquery:
			        a language model dictionary,
			        with entropy_weight set at -0.1
		    Return:
		    	- a list of tuples[(docname, score), ...]

        """
        self.refresh_docscores()

        self.update_document_scores(query, entropy_weight=1.)
        if negquery is not None:
            self.update_document_scores(negquery, entropy_weight=-0.1)

        sorted_ret = sorted(self._docscores.items(),
                            key=lambda x: x[1], reverse=True)
        return sorted_ret

    def update_document_scores(self, query, entropy_weight=1.):
        """
                Inherit and override the base class!
        """
        raise NotImplementedError


class KLRanker(BaseRanker):
    def update_document_scores(self, query, entropy_weight=1.):
        """
                Calculate KL divergence with smoothing
        """
        # Loop through query first to lower access time
        query_indices = []
        for wordID, word_prob in query.items():
            # Word does not intersect with any documents
            if wordID not in self._indices['background']:
                continue

            word_background_prob = self._indices['background'][wordID]
            word_inverted_index = self._indices['inverted_index'][wordID]

            query_indices.append(
                (word_prob, word_background_prob, word_inverted_index))

        # For every document, calculate its cross entropy score
        for docname in self._docscores:
            # Loop through query
            entropy_sum = 0.
            for word_prob, word_background_prob, word_inverted_index in query_indices:
                # Get doc prob if in inverted_index, else set to 0.
                docprob = word_inverted_index.get(docname, 0.)
                doclength = self._indices['doclengs'][docname]

                smoothed_docprob = self.smooth_docprob(
                    docprob, doclength, word_background_prob)

                weighted_entropy = entropy_weight * \
                    cross_entropy(word_prob, smoothed_docprob)

                entropy_sum += weighted_entropy
            # Update(add), not assign
            self._docscores[docname] += entropy_sum

        return self._docscores

    @staticmethod
    def smooth_docprob(docprob, doclength, word_background_prob, alpha=1000):
        # Get smoothing weight
        alpha_d = doclength / (doclength + alpha)
        # Smooth by interpolation with background probability
        smoothed_docprob = (1 - alpha_d) * \
            word_background_prob + alpha_d * docprob
        return smoothed_docprob
