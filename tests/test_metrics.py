from iscr.searchengine import metrics

def test_kl_divergence():
    p = { 1: 0.5, 2: 0.4, 4: 0.1 }
    q = { 1: 0.2, 2: 0.3, 3: 0.5 }

    assert metrics.kl_divergence(p,q) == -0.5732181949177899

    q = { 5: 1.0 }

    assert metrics.kl_divergence(p,q) == 0.0

    q = { 2: 0.7, 5: 0.3 }

    assert metrics.kl_divergence(p,q) == 0.22384631517416903

def test_evalAP():
	ret = [ (1, 100), (2, 99), (3, 98) ]
	ans = { 1: 1, 3: 1 }
	assert metrics.evalAP(ret,ans) == 0.8333333333333333

def test_cross_entropy():
	assert metrics.cross_entropy(0.5, 0.3) == -0.25541281188299536
	assert metrics.cross_entropy(0.2, 0.0) == 0.
