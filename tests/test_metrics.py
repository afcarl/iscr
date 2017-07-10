from iscr.ranker import metrics

def test_cross_entropy():
	assert metrics.cross_entropy(0.5, 0.3) == -0.25541281188299536
	assert metrics.cross_entropy(0.2, 0.0) == 0.
