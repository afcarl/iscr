import argparse
from glob import glob
import os
import pickle

import jieba
from tqdm import tqdm

from iscr.utils import load_from_pickle, save_to_pickle

def segment_jieba(text):
    return ' '.join(list(jieba.cut(text)))

def segment_ckip(text):
    raise NotImplementedError


def segment_file(segment, filepath):
    ret = ""
    with open(filepath, 'r') as fin:
        for line in fin.readlines():
            line = ''.join(line.split()) + '\n'
            ret += segment(line)
    return ret


def run_segment(segment, query_file, out_query_file, transcript_dir, out_transcript_dir):
    # Segment query
    segmented_query = segment_file(segment, query_file)
    with open(out_query_file, 'w') as fout:
        fout.write(segmented_query)

    # Segment Documents
    if not os.path.isdir(out_transcript_dir):
        os.makedirs(out_transcript_dir)

    for filepath in tqdm(glob(os.path.join(transcript_dir, '*'))):
        filename = os.path.basename(filepath)
        segmented_transcript = segment_file(segment, filepath)
        out_filename = os.path.join(out_transcript_dir, filename)
        with open(out_filename, 'w') as fout:
            fout.write(segmented_transcript)


segment_dict = {
    'unigram': segment_unigram,
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
    parser.add_argument('-u', '--user', type=str,
                        default='./data/query/query_dict_for_jieba.txt')
    args = parser.parse_args()

    if args.user:
        print("Loading {} for jieba...".format(args.user))
        jieba.load_userdict(args.user)

    segment = segment_dict[args.segment]

    run_segment(segment, args.query_file, args.out_query_file,
                args.transcript_dir, args.out_transcript_dir)
