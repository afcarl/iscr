import argparse
from glob import glob
import os
import pickle
import sys

sys.path.append('.')

import jieba
from tqdm import tqdm

from ckipclient import CKIPClient
from iscr.utils import load_from_pickle, save_to_pickle

client = None  # For CKIP


def segment_jieba(text, retain_line=False):
	result = list(jieba.cut(text))
	return '\n'.join(result)


def segment_ckip(text, retain_line=False):
	result = client.segment(text, pos=False)
	if retain_line:
		return ' '.join(result[0]) + '\n'
	else:
		return '\n'.join(result[0])


def segment_file(segment, filepath, retain_line=False):
	text = ""
	with open(filepath, 'r') as fin:
		if retain_line:
			for line in tqdm(fin.readlines()):
				text += segment(''.join(line.split())+'\n', retain_line=True)
			ret = text
		else:
			for line in fin.readlines():
				text += ''.join(line.split()) + '\n'
			ret = segment(text)
	return ret


def run_segment(segment, query_file, out_query_file, transcript_dir, out_transcript_dir):
    # Segment query
	print("Segmenting query...")
	if os.path.exists(out_query_file):
		print("{} already exists, skipping...".format(out_query_file))
	else:
		segmented_query = segment_file(segment, query_file, retain_line=True)
		with open(out_query_file, 'w') as fout:
			fout.write(segmented_query)

    # Segment Documents
	if not os.path.isdir(out_transcript_dir):
		os.makedirs(out_transcript_dir)

	print("Segmenting documents...")
	for filepath in tqdm(glob(os.path.join(transcript_dir, '*'))):
		filename = os.path.basename(filepath)
		out_filename = os.path.join(out_transcript_dir, filename)
		if os.path.exists(out_filename):
			print("Skipping {}...".format(out_filename))
			continue

		segmented_transcript = segment_file(segment, filepath)
		with open(out_filename, 'w') as fout:
			fout.write(segmented_transcript)


segment_dict = {
    'jieba': segment_jieba,
    'ckip': segment_ckip,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--segment', type=str,
                        default='jieba', help='jieba | ckip')
    parser.add_argument('--query_file', type=str,
                        default='./data/query/PTV.utf8.query', help='raw query file')
    parser.add_argument('--transcript_dir', type=str,
                        default='./data/PTV_onebest_fromMATBN_charSeg/', help='transcription directory')
    parser.add_argument('--out_query_file', type=str,
                        default='./data/query/PTV.utf8.jieba.query', help='segmented query location')
    parser.add_argument('--out_transcript_dir', type=str,
                        default='./data/PTV.debug.jieba', help='segmented query location')
    args = parser.parse_args()

    segment = segment_dict[args.segment]
    if args.segment == 'ckip':
    	client = CKIPClient('140.109.19.104', 1501,
                        	'iammrhelo', 'hl4su3a8')

    run_segment(segment, args.query_file, args.out_query_file,
                args.transcript_dir, args.out_transcript_dir)
