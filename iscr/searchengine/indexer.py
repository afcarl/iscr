"""
	Builds index from transcripts
"""
from collections import defaultdict
from glob import glob
import os
import time

from pympler import asizeof
from tqdm import tqdm

from .metrics import normalize
from .utils import save_to_pickle, convert_size


class Indexer(object):
    def __init__(self, data_dir=None):
        if data_dir is None:
            self.data_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'data')
        else:
            self.data_dir = data_dir

    def run_indexing(self, transcript_dir, query_file=None, out_dir=None):
        print("[Indexer] Building word count...")

        if out_dir is None:
            transcript_name = os.path.join(os.path.basename(transcript_dir))
            out_dir = os.path.join(self.data_dir, transcript_name)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        docpaths = sorted(glob(os.path.join(transcript_dir, '*')))

        if query_file is not None:
            print(
                "[Indexer] Query file specified. Building lex with query_file and documents...")
            files_to_read = [query_file] + docpaths
        else:
            print(
                "[Indexer] Query file not specified. Building lex with documents only...")
            files_to_read = docpaths

        # Build lex dictionary
        lex_pickle = os.path.join(out_dir, 'lex.pickle')
        lex_dict = self._build_lex_dict(files_to_read, lex_pickle)

        # Build docmodels
        document_pickle = os.path.join(out_dir, 'document.pickle')
        documents = self._build_docmodels(lex_dict, docpaths, document_pickle)

        # Build indices
        index_pickle = os.path.join(out_dir, 'indices.pickle')
        indices = self._build_indices(documents, index_pickle)

    ######################
    #	Build Word Count #
    ######################
    def _build_lex_dict(self, files_to_read, lex_pickle=None):
        print("[Indexer] Building lex dictionary...")
        lex_dict = {}
        lex_idx = 0
        # Tokens
        for filepath in tqdm(files_to_read):
            with open(filepath, 'r') as fin:
                tokens = fin.read().split()
            for word in tokens:
                if word not in lex_dict:
                    lex_dict[word] = lex_idx
                    lex_idx += 1
        if lex_pickle is not None:
            print("[Indexer] Saving lex dict to pickle...")
            save_to_pickle(lex_pickle, lex_dict)
        return lex_dict

    def _build_docmodels(self, lex_dict, docpaths, document_pickle=None):
        print("[Indexer] Building document models...")
        documents = {}
        for filepath in tqdm(docpaths):
            with open(filepath, 'r') as fin:
                text = fin.read()

            docname = os.path.basename(filepath)

            wordcount_obj = text_to_wordcount(lex_dict, text)
            documents[docname] = {'wordcount': wordcount_obj}

        if document_pickle is not None:
            print("[Indexer] Saving document word count to pickle...")
            save_to_pickle(document_pickle, documents)
        return documents

    ############################
    #        Indexing  		   #
    #	  1. doclengs		   #
    #	  2. background		   #
    # 	  3. inverted index    #
    ############################
    def _build_indices(self, documents, index_pickle=None):
        print("[Indexer] Indexing...")
        _start_time = time.time()

        background = defaultdict(float)
        doclengs = {}
        inverted_index = defaultdict(dict)

        L = len(documents)

        for doc_idx in documents:
            doc_wc = documents[doc_idx]['wordcount']
            doc_lm = normalize(doc_wc, inplace=False)

            for word_idx, word_prob in doc_lm.items():
                background[word_idx] += word_prob
                inverted_index[word_idx][doc_idx] = word_prob

            doclengs[doc_idx] = sum(doc_wc.values())

        # Normalize background to probability
        background = normalize(background, inplace=False)

        # Group to one object
        indices = {'doclengs': doclengs,
                   'inverted_index': inverted_index,
                   'background': background}

        _end_time = time.time()
        print("[Indexer] Indexing done in {} seconds.".format(
            _end_time - _start_time))
        print("[Indexer] Total Memory of indices: {}".format(
            convert_size(asizeof.asizeof(indices))))

        # Save to pickle
        if index_pickle is not None:
            print("[Indexer] Saving indices to pickle...")
            save_to_pickle(index_pickle, indices)

        return indices

######################
#  Helper Functions  #
######################


def text_to_wordcount(lex_dict, text):
    # Record inverted index if specified
    wc = defaultdict(int)
    for word in text.split():
        word_idx = lex_dict[word]
        wc[word_idx] += 1
    return wc


if __name__ == "__main__":
    transcript_dir = '../../data/PTV.dnn.onebest.jieba'
    query_file = '../../data/query/PTV.utf8.jieba.query'

    indexer = Indexer()
    indexer.run_indexing(transcript_dir=transcript_dir, query_file=query_file)
