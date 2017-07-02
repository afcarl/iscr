from glob import glob
import os
import sys

sys.path.append('..')

from tqdm import tqdm

from iscr import utils
import reader


def run_reformat(data_dir, out_dir, lex_file, query_pickle):
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	data_name = os.path.basename(data_dir)
	print("Reading lex...")
	encoded_lex_file = os.path.join(data_dir,data_name + '.lex')
	encoded_lex_dict = reader.readLex(encoded_lex_file)

	print("Reading background...")
	background_file = os.path.join(data_dir, data_name +'.background')
	background = reader.readBackground(background_file, encoded_lex_dict)

	print("Reading doclengs...")
	docleng_file = os.path.join(data_dir, data_name+'.doclength')
	doclengs = reader.readDocLength(docleng_file)

	# Change key from index to docname
	print("Change doclengths keys to document names...")
	namekey_doclengs = {}
	for doc_idx, length in doclengs.items():
		docname = 'T' + str(doc_idx).zfill(4)
		namekey_doclengs[ docname ] = length


	print("Reading inverted index...")
	index_file = os.path.join(data_dir, data_name +'.index')
	inverted_index = reader.readInvIndex(index_file)

	print("Converting inverted index docnames...")
	named_inverted_index = {}
	for wordID, docs_prob in inverted_index.items():
		named_docs_prob = {}
		for docID, prob in docs_prob.items():
			docname = 'T' + str(docID).zfill(4)
			named_docs_prob[ docname ] = prob
		named_inverted_index[ wordID ] = named_docs_prob

	print("Reading document models...")
	documents_lm = {}
	docmodel_dir = os.path.join(data_dir,'docmodel','*')
	for docpath in tqdm(glob(docmodel_dir)):
		docname = os.path.basename(docpath)
		documents_lm[ docname ] = reader.readDocModel(docpath)

	print("Converting documents language model to wordcount with document lengths")
	documents_wc = {}
	for docname, lm in tqdm(documents_lm.items()):
		wc = {}
		length = namekey_doclengs[ docname ]
		for word_idx, word_prob in lm.items():
			wc[ word_idx ] = round(word_prob * length)
		documents_wc[ docname ] = wc

	print("Saving lex to pickle...")
	lex_dict = reader.readLex(lex_file)
	lex_pickle = os.path.join(out_dir,'lex.pickle')
	utils.save_to_pickle(lex_pickle, lex_dict)

	print("Saving documents to pickle...")
	document_pickle = os.path.join(out_dir,'document.pickle')
	utils.save_to_pickle(document_pickle, documents_wc)

	print("Saving indices to pickle...")
	indices = {
		'background': background,
		'doclengs': namekey_doclengs,
		'inverted_index': named_inverted_index
		}

	index_pickle = os.path.join(out_dir,'indices.pickle')
	utils.save_to_pickle(index_pickle, indices)

	print("Saving query to pickle...")
	old_query_pickle = os.path.join(data_dir,'query.pickle')
	old_query = utils.load_from_pickle(old_query_pickle)
	query = {}
	for query_lm, ans_dict, q_idx in old_query:
		query_wc = {}
		length = len(query_lm.keys())
		for word_idx, word_prob in query_lm.items():
			count = round(word_prob * length)
			assert count == 1, query_lm
			query_wc[ word_idx ] = count

		query[ q_idx ] = {
			'answer': ans_dict,
			'wordcount': query_wc,
			'languagemodel': query_lm,
		}

	utils.save_to_pickle(query_pickle, query)


if __name__ == "__main__":
	data_dir = '../data/lattice_CMVN'
	out_dir = '../iscr/ranker/collections/PTV.lattice.CMVN.paper'
	lex_file = '../data/PTV.utf8.lex'
	query_pickle = '../queries/PTV.lattice.CMVN.paper.query.pickle'
	run_reformat(data_dir, out_dir, lex_file, query_pickle)
