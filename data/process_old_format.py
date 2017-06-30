from glob import glob
import os

from pympler import asizeof

from iscr.searchengine.indexer import Indexer
from iscr.searchengine.utils import save_to_pickle, convert_size

def parse_file_to_pickle(data_dir, out_dir):
	data_name = os.path.basename(data_dir)

	lex_file = os.path.join(data_dir, 'PTV.utf8.lex')
	lex_dict = read_lex(lex_file)

	query_pickle = os.path.join(data_dir,'query.pickle')
	query_answer = read_query_answer(query_pickle)

	docleng_file = os.path.join(data_dir,data_name + '.doclength')
	docmodel_dir = os.path.join(data_dir,'docmodel')

	documents = read_docmodels(docmodel_dir, docleng_file)

    # Save to directory
	if not os.path.isdir(out_dir):
		os.makedirs(out_dir)
	out_pickle = os.path.join(out_dir,'wordcount.pickle')

	print("Saving lex...")
	lex_pickle = os.path.join(out_dir,'lex.pickle')
	save_to_pickle(lex_pickle,lex_dict)

	print("Saving query answer...")
	query_pickle = os.path.join('.','queries','onebest_CMVN.query.pickle')
	save_to_pickle(query_pickle, query_answer)

	print("Saving documents...")
	document_pickle = os.path.join(out_dir,'document.pickle')
	save_to_pickle(document_pickle,documents)

	indexer = Indexer()
	index_pickle = os.path.join(out_dir,'indices.pickle')
	indices = indexer._build_indices(documents, index_pickle)

def read_lex(lex_file):
	lex_dict = {}
	with open(lex_file,'r') as fin:
		for idx, line in enumerate(fin.readlines(), 1):
			lex_dict[ line.strip() ] = idx
	return lex_dict

def read_query_answer(query_pickle):

	query = {}

	with open(query_pickle,'rb') as fin:
		queries = pickle.load(fin)

	for (q_lm, a_dict, q_idx) in queries:
		query[ q_idx ] = {
			'wordcount': q_lm,
			'answer': a_dict
		}

	return query

def read_docmodels(docmodel_dir, docleng_file):

	doclengs = read_lm_file(docleng_file,isdocname=True)

	documents = {}
	for doc_file in glob(os.path.join(docmodel_dir,'*')):

		doc_name = os.path.basename(doc_file)

		doc_idx = int(doc_name[1:])

		doc_lm = read_lm_file(doc_file,isdocname=False)

		# Rebuild word count file
		doc_wc = {}
		sum_count = 0
		for word_idx, word_prob in doc_lm.items():
			count =  round(doclengs[ doc_idx ] * word_prob)
			doc_wc[ word_idx ] = count
			sum_count += count

		assert sum_count == doclengs[ doc_idx ]

		documents[ doc_name ] = { 'wordcount': doc_wc }

	return documents

def read_lm_file(lm_file, isdocname = False):
	lm = {}
	with open(lm_file,'r') as fin:
		for line in fin.readlines():
			tokens = line.split()
			key = int(tokens[0]) if not isdocname else int(tokens[0][1:])
			val = float(tokens[1])
			lm[ key ] = val
	return lm


if __name__ == "__main__":
	data_dir = './data/onebest_CMVN'
	out_dir = './iscr/searchengine/data/PTV.onebest.CMVN'
	parse_file_to_pickle(data_dir, out_dir)
