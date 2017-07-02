from iscr.evalute import average_precision

def test_average_precision():
	ret = [ (1, 100), (2, 99), (3, 98) ]
	ans = { 1: 1, 3: 1 }
	assert average_precision(ret,ans) == 0.8333333333333333
