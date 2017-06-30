import json


def run_parsing(query_utf8_file, ans_file, out_file):

	query = {}

	with open(query_utf8_file,'r') as fin:
		for query_idx, line in enumerate(fin.readlines(),1):
			query[ query_idx ] = { 'query': line.strip(), 'answer': {} }

	with open(ans_file,'r') as fin:
		for line in fin.readlines():
			query_idx, _, docname, _ = line.split()
			query[ int(query_idx) ]['answer'][ docname ] = 1

	with open(out_file,'w',encoding='utf-8') as fout:
		json.dump(query, fout, ensure_ascii=False, sort_keys=True, indent=4)

if __name__ == "__main__":
	ans_file = 'PTV.ans'
	query_utf8_file = 'PTV.utf8.query'
	out_file = 'PTV.queries.json'

	run_parsing(query_utf8_file, ans_file, out_file)
