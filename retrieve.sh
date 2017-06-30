echo "Producing Onebest CMVN paper results..."
python scripts/test_retrieval.py -q ./queries/PTV.onebest.CMVN.paper.query.pickle -d ./iscr/searchengine/collections/PTV.onebest.CMVN.paper/
echo
echo "Producing Lattice CMVN paper results..."
python scripts/test_retrieval.py -q ./queries/PTV.lattice.CMVN.paper.query.pickle -d ./iscr/searchengine/collections/PTV.lattice.CMVN.paper/
echo
echo "Producing DNN onebest jieba results"
python scripts/test_retrieval.py -q ./queries/PTV.dnn.onebest.jieba.query.pickle -d ./iscr/searchengine/collections/PTV.dnn.onebest.jieba
echo
echo "Producing Reference jieba results"
python scripts/test_retrieval.py -q queries/PTV.reference.jieba.query.pickle -d ./iscr/searchengine/collections/PTV.reference.jieba/
