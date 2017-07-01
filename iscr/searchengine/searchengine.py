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
		self.result = {}
		for docname in self.indices['doclengs'].keys():
			self.result[docname] = sys.float_info.min

	def retrieve(self, query, negquery=None):
		"""
			Returns a list of tuples [(docname, score),...]
			For MAP, every docname has to exist
		"""
		self.refresh_results()

		self._retrieve(query, 1)
		if negquery is not None:
			self._retrieve(negquery, -0.1)

		sorted_ret = sorted(self.result.items(), key=lambda x: x[1], reverse=True)
		return sorted_ret

	def _retrieve(self, query, entropy_weight=1.):
		# Query
		for wordID, word_prob in query.items():
			# Check if query word intersects with documents
			if wordID not in self.indices['background']:
				continue

			# Recored scored documents for this word
			unscored_docs = set(self.docnames)

			word_background_prob = self.indices['background'][wordID]
			word_inverted_index = self.indices['inverted_index'][wordID].items()
			for docID, docprob in word_inverted_index:
				unscored_docs.remove(docID)

				doclength = self.indices['doclengs'][ docID ]

				weighted_entropy = entropy_weight * \
					entropy_between_word_and_smoothed_doc(
						word_prob, docprob, doclength, word_background_prob)

				# Adds to result
				if self.result[docID] != sys.float_info.min:
					self.result[docID] += weighted_entropy
				else:
					self.result[docID] = weighted_entropy

			# Smooth background for those unscored
			for docID in unscored_docs:
				doclength = self.indices['doclengs'][ docID ]

				weighted_entropy = entropy_weight * \
					entropy_between_word_and_smoothed_doc(
						word_prob, 0., doclength, word_background_prob)

				# Adds to result
				if self.result[docID] != sys.float_info.min:
					self.result[docID] += weighted_entropy
				else:
					self.result[docID] = weighted_entropy

def smooth_weight_from_docleng(length, alpha=1000):
	return length / (length + alpha)

def interpolate_with_smoothing_weight(p1, p2, alpha_d):
	return (1 - alpha_d) * p1 + alpha_d * p2

def entropy_between_word_and_smoothed_doc(word_prob, docprob, doclength, word_background_prob):
	alpha_d = smooth_weight_from_docleng(doclength)
	smoothed_docprob = interpolate_with_smoothing_weight(word_background_prob, docprob, alpha_d)
	entropy = cross_entropy(word_prob, smoothed_docprob)
	return entropy


if __name__ == "__main__":
	pass
