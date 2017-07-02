import argparse
import sys
sys.path.append('.')

from iscr.ranker import Indexer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--transcript_dir', type=str, default='./transcripts/PTV.dnn.onebest.jieba',
                        help='Directory full of tokenized transcripts')
    parser.add_argument('-q', '--query_file', type=str, default='./data/PTV.query.txt',
                        help='Tokenized query files to add to dictionary')
    parser.add_argument('-o', '--out_dir', type=str, default='./iscr/ranker/collections/PTV.dnn.onebest.jieba',
                        help='Save indices to index directory')
    args = parser.parse_args()

    indexer = Indexer()
    indexer.run_indexing(transcript_dir=args.transcript_dir,
                         query_file=args.query_file, out_dir=args.out_dir)
