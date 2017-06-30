from collections import defaultdict
import os
import time

from .metrics import normalize, cross_entropy
from .utils import load_from_pickle, save_to_pickle

class SearchEngine(object):
	def __init__(self, lex_pickle, index_pickle, build_wordcount=False):

		print("[SearchEngine] Loading lex from {}".format(lex_pickle))
		self.lex_dict = load_from_pickle(lex_pickle)

		print("[SearchEngine] Loading index from {}".format(index_pickle))
		self.indices = load_from_pickle(index_pickle)

	def retrieve(self, query, negquery = None, alpha=1000, beta=0.1):
		"""
			Retrieves result using query and negquery if negquery exists
		"""
		# Set result key by docname
		result = {}
		for key in self.indices['doclengs']:
			result[ key ] = -9999

		# Query
		for wordID, weight in query.items():
			existDoc = {}
			for docID, val in self.indices['inverted_index'][wordID].items():
				existDoc[docID] = 1

				# smooth doc model by background
				alpha_d = self.indices['doclengs'][docID]/(self.indices['doclengs'][docID]+alpha)
				qryprob = weight
				docprob = (1-alpha_d)*self.indices['background'][wordID]+alpha_d*val

				# Adds to result
				if result[docID] != -9999:
					result[docID] += cross_entropy(qryprob,docprob)
				else:
					result[docID] = cross_entropy(qryprob,docprob)

		# Run background model
		for docID, val in result.items():
			if not docID in existDoc and wordID in self.indices['background']:
				alpha_d = self.indices['doclengs'][docID] / ( self.indices['doclengs'][docID] + alpha )
				qryprob = weight
				docprob = (1-alpha_d) * self.indices['background'][wordID]

				if result[docID] != -9999:
					result[docID] += cross_entropy(qryprob,docprob)
				else:
					result[docID] = cross_entropy(qryprob,docprob)

		# Run through negative query
		if negquery:
			for wordID, weight in negquery.items():
				existDoc = {}
				for docID, val in self.indices['inverted_index'][wordID].items():
					existDoc[docID] = 1
					# smooth doc model by background
					alpha_d = self.indices['doclengs'][docID]/(self.indices['doclengs'][docID]+alpha)
					qryprob = weight
					docprob = (1-alpha_d)*self.indices['background'][wordID]+alpha_d*val

					if result[docID] != -9999:
						result[docID] -= beta * cross_entropy(qryprob,docprob)
					else:
						result[docID] = -1 * beta * cross_entropy(qryprob,docprob)

					# Run through background model
					for docID, val in result.items():
						if not docID in existDoc and wordID in self.indices['background']:
							alpha_d = self.indices['doclengs'][docID]/(self.indices['doclengs'][docID]+alpha)
							qryprob = weight
							docprob = (1-alpha_d) * self.indices['background'][wordID]

						if result[docID] != -9999:
							result[docID] -= beta * cross_entropy(qryprob,docprob)
						else:
							result[docID] = -1 * beta * cross_entropy(qryprob,docprob)

		sorted_ret = sorted(result.items(),key=lambda x: x[1],reverse=True)
		return sorted_ret


if __name__ == "__main__":
	pass
