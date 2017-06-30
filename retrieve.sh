echo "Trying to reproduce onebest CMVN paper results..."
python scripts/test_retrieval.py -q ./queries/PTV.onebest.CMVN.paper.query.pickle -d ./iscr/searchengine/collections/PTV.onebest.CMVN.paper/

#echo "Trying to reproduce lattice CMVN paper results..."
#python scripts/test_retrieval.py -q ./queries/PTV.lattice.CMVN.paper.query.pickle -d ./iscr/searchengine/collections/PTV.lattice.CMVN.paper/

echo "DNN onebest jieba results"
python scripts/test_retrieval.py -q ./queries/PTV.dnn.onebest.jieba.query.pickle -d ./iscr/searchengine/collections/PTV.dnn.onebest.jieba
