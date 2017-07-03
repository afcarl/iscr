echo "Producing Onebest CMVN paper results..."
python scripts/run_klranker_baseline.py -q ./queries/PTV.onebest.CMVN.paper.query.pickle -d ./collections/PTV.onebest.CMVN.paper/
echo
echo "Producing Lattice CMVN paper results..."
python scripts/run_klranker_baseline.py -q ./queries/PTV.lattice.CMVN.paper.query.pickle -d ./collections/PTV.lattice.CMVN.paper/
echo
echo "Producing DNN onebest jieba results"
python scripts/run_klranker_baseline.py -q ./queries/PTV.dnn.onebest.jieba.query.pickle -d ./collections/PTV.dnn.onebest.jieba
echo
echo "Producing Reference jieba results"
python scripts/run_klranker_baseline.py -q queries/PTV.reference.jieba.query.pickle -d ./collections/PTV.reference.jieba/
echo
echo "Producing DNN onebest ckip results"
python scripts/run_klranker_baseline.py -q ./queries/PTV.dnn.onebest.ckip.query.pickle -d ./collections/PTV.dnn.onebest.ckip
echo
echo "Producing Reference ckip results"
python scripts/run_klranker_baseline.py -q queries/PTV.reference.ckip.query.pickle -d ./collections/PTV.reference.ckip/
