import io
import os

from iscr import utils

def test_pickle():
	obj = { 1: 2, 3: 4}

	test_pickle_file = 'test.pickle'

	utils.save_to_pickle(test_pickle_file, obj)

	obj2 = utils.load_from_pickle(test_pickle_file)

	assert obj == obj2

	os.remove(test_pickle_file)

def test_json():
	obj = { 1: 2, 3: 4 }

	test_json_file = 'test.json'

	utils.save_to_json(test_json_file, obj)

	obj2 = utils.load_from_json(test_json_file)
	try:
		assert obj == obj2, 'Python json module converted keys to integer!'
	except:
		obj3 = {}
		for key, val in obj2.items():
			obj3[ int(key) ] = val
		assert obj == obj3

	os.remove(test_json_file)
