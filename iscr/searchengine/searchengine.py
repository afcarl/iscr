from .metrics import cross_entropy
from ..utils import load_from_pickle


class SearchEngine(object):
	def __init__(self, lex_pickle, index_pickle):
		# Use this if input is text
		print("[SearchEngine] Loading lex from {}".format(lex_pickle))
		self._lex_dict = load_from_pickle(lex_pickle)

		print("[SearchEngine] Loading index from {}".format(index_pickle))
		self._indices = load_from_pickle(index_pickle)

		print("[SearchEngine] Initializing document scores")
		self.init_docscores()

	def __call__(self, lex_pickle, index_pickle):
		self.__init__(lex_pickle, index_pickle)

	def init_docscores(self):
		self._docscores = {}
		for docname in self._indices['doclengs']:
			self._docscores[docname] = 0.
		return self._docscores

	def refresh_docscores(self):
		for docname in self._docscores:
			self._docscores[docname] = 0.
		return self._docscores

	def retrieve(self, query, negquery=None):
		"""
			Returns a list of tuples [(docname, score),...]
			For MAP, every docname has to exist
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
			Iterate through every document to calculate scores
		"""
		# Loop through query first to lower access time
		query_indices = []
		for wordID, word_prob in query.items():
			# Word does not intersect with any documents
			if wordID not in self._indices['background']:
				continue

			word_background_prob = self._indices['background'][wordID]
			word_inverted_index = self._indices['inverted_index'][wordID]

			query_indices.append((word_prob, word_background_prob, word_inverted_index))

		# For every document, calculate its cross entropy score
		for docname in self._docscores:
			# Loop through query
			entropy_sum = 0.
			for word_prob, word_background_prob, word_inverted_index in query_indices:
				# Get doc prob if in inverted_index, else set to 0.
				docprob = word_inverted_index.get(docname, 0.)
				doclength = self._indices['doclengs'][docname]

				smoothed_docprob = smooth_docprob(
					docprob, doclength, word_background_prob)

				weighted_entropy = entropy_weight * \
					cross_entropy(word_prob, smoothed_docprob)

				entropy_sum += weighted_entropy
			# Update(add), not assign
			self._docscores[docname] += entropy_sum

		return self._docscores

#######################
#	Helper Functions  #
#######################
def smooth_docprob(docprob, doclength, word_background_prob, alpha=1000):
	# Get smoothing weight
	alpha_d = doclength / (doclength + alpha)
	# Smooth by interpolation with background probability
	smoothed_docprob = (1 - alpha_d) * word_background_prob + alpha_d * docprob
	return smoothed_docprob
