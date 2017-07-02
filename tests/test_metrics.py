from iscr.ranker import metrics

def test_normalize():
    p = { 1: 1, 2: 3 }
    assert metrics.normalize(p, inplace=False) == { 1 : 0.25, 2: 0.75 }

def test_cross_entropy():
	assert metrics.cross_entropy(0.5, 0.3) == -0.25541281188299536
	assert metrics.cross_entropy(0.2, 0.0) == 0.
