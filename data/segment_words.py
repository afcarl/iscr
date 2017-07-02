import argparse
from glob import glob
import os
import pickle
import sys

sys.path.append('.')

from tqdm import tqdm

from ckipclient import CKIPClient
from iscr.utils import load_from_pickle, save_to_pickle


class FileOrDirectoryMismatchException(Exception):
	pass

client = None  # For CKIP

def segment_jieba(text, is_line=False):
	result = list(jieba.cut(text))
	if is_line:
		return ' '.join(result)
	else:
		return '\n'.join(result).replace('\n\n\n','\n').strip('\n')


def segment_ckip(text, is_line=False):
	result = client.segment(text, pos=False)[0]
	if is_line:
		return ' '.join(result) + '\n'
	else:
		return '\n'.join(result)


def load_segment_function(segment_method):
	segment_function = segment_dict[args.segment]
	return segment_function


def segment_file(segment, filepath, retain_line=False):
	text = ""
	with open(filepath, 'r') as fin:
		if retain_line:
			for line in tqdm(fin.readlines()):
				text += segment(''.join(line.split()) + '\n', is_line=True)
			ret = text.strip('\n')
		else:
			for line in fin.readlines():
				text += ''.join(line.split()) + '\n'
			ret = segment(text)
	return ret


def run_segment(segment, input, output, retain_line, skip_exists=False):
	segment_function = load_segment_function(segment)

	if os.path.isfile(input) and not os.path.isdir(output):
		if skip_exists and os.path.exists(output):
			print("{} already exists, skipping...".format(output))
		else:
			segmented_file = segment_file(segment_function, input, retain_line)
			with open(output,'w') as fout:
				fout.write(segmented_file)

	elif os.path.isdir(input):
		if not os.path.exists(output):
			os.makedirs(output)
		else:
			assert os.path.isdir(output)

		for filepath in tqdm(glob(os.path.join(input, '*'))):
			filename = os.path.basename(filepath)
			out_filename = os.path.join(output, filename)
			if skip_exists and os.path.exists(out_filename):
				print("{} already exists, skipping...".format(out_filename))
				continue

			segmented_file = segment_file(segment_function, filepath, retain_line)
			with open(out_filename, 'w') as fout:
				fout.write(segmented_file)
	else:
		raise FileOrDirectoryMismatchException("Input and output should both be files or directories!")

segment_dict = {
	'jieba': segment_jieba,
	'ckip': segment_ckip,
}

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--segment', type=str,
						default='jieba', help='jieba | ckip')
	parser.add_argument('-i', '--input', type=str)
	parser.add_argument('-o', '--output', type=str)
	parser.add_argument('-r', '--retain_line', action='store_true')
	parser.add_argument('--skip_exists', action='store_true')
	args = parser.parse_args()

	print(vars(args))

	segment_method = args.segment

	if segment_method == 'ckip':
		client = CKIPClient('140.109.19.104', 1501,
							'iammrhelo', 'hl4su3a8')
	elif segment_method == jieba:
		import jieba

	run_segment(args.segment, args.input, args.output, args.retain_line, args.skip_exists)
