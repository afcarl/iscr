from iscr.searchengine import metrics

def test_normalize():
    p = { 1: 1, 2: 3 }
    assert metrics.normalize(p, inplace=False) == { 1 : 0.25, 2: 0.75 }

def test_evalAP():
	ret = [ (1, 100), (2, 99), (3, 98) ]
	ans = { 1: 1, 3: 1 }
	assert metrics.evalAP(ret,ans) == 0.8333333333333333

def test_cross_entropy():
	assert metrics.cross_entropy(0.5, 0.3) == -0.25541281188299536
	assert metrics.cross_entropy(0.2, 0.0) == 0.
