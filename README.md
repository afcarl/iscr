# Interactive Spoken Content Retrieval
---
## Getting Started

Run baseline result on dnn recognition results with jieba segmentation

Example data
  - ./data/PTV.query.txt (query file, an unsegmented query on each line)
  - ./data/PTV_transcription_charSeg (directory of dnn recognition transcripts)

1. Segment query and transcripts with jieba
```bash
# Segment query, retain line for each query
$python ./data/segment_words.py -i ./data/PTV.query.txt -o ./data/PTV.query.jieba.txt -r
# Segment transcripts, separate each word by line
$python ./data/segment_words.py -i ./data/PTV_transcription_charSeg -o ./transcripts/PTV.dnn.onebest.jieba
```
Now we have our jieba segmented query at './data/PTV.query.jieba.txt' and transcripts at './transcripts/PTV.dnn.onebest.jieba'

2. Run indexing with our indexer

  The indexing script is located at './scripts/run_indexing_for_segmented_transcripts.py'
```bash
# Create vocabulary with query & transcript words,
# run indexing(background, doclengs, inverted_index),
# then store it to the collection directory
$python ./scripts/run_indexing_for_segmented_transcripts.py -q ./data/PTV.query.jieba.txt -t ./transcripts/PTV.dnn.onebest.jieba -o ./collections/PTV.dnn.onebest.jieba/
```
  Indexing will create 3 pickle files in the collection directory
  - lex.pickle
  - document.pickle
  - indices.pickle


3. Create query & answer pickle file for ranking evaluation

  The scripts is located at './data/build_queries.py'
```bash
# Loads lex dict from collection directory, then process query text & group them by answer, save to query pickle
$python ./data/build_queries.py -l ./collections/PTV.dnn.onebest.jieba/lex.pickle -q ./data/PTV.query.jieba.txt -a ./data/PTV.ans -o ./queries/PTV.dnn.onebest.jieba.query.pickle
```
  Now we have our query_and_answer pickle at ./queries/PTV.dnn.onebest.jieba.query.pickle

4. Run ranking script

  Ranking script is located at './scripts/run_klranker_baseline.py'
```bash
# Loads query_answer pickle & transcript indices and outputs Mean Average Precision for the queries
$python scripts/run_klranker_baseline.py -q ./queries/PTV.dnn.onebest.jieba.query.pickle -d ./collections/PTV.dnn.onebest.jieba/
```

5. Psuedo relevance feedback

  Script is located at './scripts.run_pseudo_relevant_feedback.py'. This script assumes top 10 ranked documents are relevant and performs query regularized mixture expansion for second pass ranking. Please see
  './iscr/dialoguemanager.py' for details.
```bash
# Loads the same query & transcript pickle from 4
$python scripts/run_pseudo_relevant_feedback.py -q ./queries/PTV.dnn.onebest.jieba.query.pickle -d ./collections/PTV.dnn.onebest.jieba
```

### Options
  * Read old format: parse old files to current format
    - See './data/read_old_format.py' for details
  * Word segmentation
    - Jieba
    - CKIP([中研院斷詞系統](http://ckipsvr.iis.sinica.edu.tw/)):
      * you will need to register an account, see './data/ckipauth.json.backup' and ./data/ckipclient.py'
  * Indexing
  * Ranker

### Installation

Code is written in python35

```
pip install -r requirements.txt
```

To use it in another project, first execute

```
python setup.py install
```
then import
```python35
from iscr.ranker import KLRanker
```

## Development

If there's anything you want to add, fork and submit a pull request!

## Testing

**pytest** is used for testing
```
python -m pytest
```

To understand more, please read the [pytest documentation](https://docs.pytest.org/en/latest/)



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
