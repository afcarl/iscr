import os

from iscr import utils

def test_pickle():
	obj = { 1: 2, 3: 4}

	test_pickle_file = 'test.pickle'

	utils.save_to_pickle(test_pickle_file, obj)

	obj2 = utils.load_from_pickle(test_pickle_file)

	assert obj == obj2

	os.remove(test_pickle_file)

def test_normalize():
    p = { 1: 1, 2: 3 }
    assert utils.normalize(p, inplace=False) == { 1 : 0.25, 2: 0.75 }
