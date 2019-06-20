
# OSIRRC Docker Image for Anserini+BM25PRF
[![Build Status](https://travis-ci.com/osirrc/anserini-bm25prf-docker.svg?branch=master)](https://travis-ci.com/osirrc/anserini-bm25prf-docker)

[**Zhaohao Zeng**](https://github.com/matthew-z) and [**Tetsuya Sakai**](https://github.com/tetsuyasakai) 

This readme is heavily based (i.e. copied from) the Anserini readme.

This is the docker image for implementing BM25 + Pseudo Relevance Feedback (PRF) [1] with Anserini [2]. The image is conforming to the [OSIRRC jig](https://github.com/osirrc/jig/) for the [Open-Source IR Replicability Challenge (OSIRRC) at SIGIR 2019](https://osirrc.github.io/osirrc2019/).

This image is available on [Docker Hub](https://hub.docker.com/r/osirrc2019/anserini-bm25prf).
<!-- The [OSIRRC 2019 image library](https://github.com/osirrc/osirrc2019-library) contains a log of successful executions of this image. -->

This image implemented Bm25+Pseudo Relevance Feedback(PRF) with Anserini.

+ Supported test collections: `robust04`
+ Supported hooks: `init`, `index`, `search` and `train`


## Quick Start

The following `jig` command can be used to index TREC disks 4/5 for `robust04`:

```sh
python run.py prepare \
  --repo osirrc2019/anserini-bm25prf \
  --tag latest \
  --collections robust04=/path/to/disk45=trectext
```

The following `jig` command can be used to perform a retrieval run on the collection with the `robust04` test collection with default hyper-parameters.

```sh
python run.py search \
  --repo osirrc2019/anserini-bm25prf \
  --output out \
  --qrels qrels/qrels.robust04.txt \
  --topic topics/topics.robust04.txt \
  --collection robust04 \ 
  --top_k 1000
```

The following `jig` command can be used to tune the hyper-parameters.
Note that the grid search may take several hours.
```sh
python run.py train \
   --repo osirrc2019/anserini-bm25prf \
   --tag latest \
   --topic topics/topics.robust04.txt \
   --qrels $(pwd)/qrels/qrels.robust04.txt \
   --validation_split $(pwd)/sample_training_validation_query_ids/robust04_validation.txt \
   --test_split $(pwd)/sample_training_validation_query_ids/robust04_test.txt \
   --model_folder $(pwd)/trained \
   --collection robust04
```


## Expected Results on [TREC 2004 Robust](http://trec.nist.gov/data/robust/04.testset.gz).

The following numbers should be able to be re-produced using the scripts provided by the jig.

#### BM25+PRF with Default Hyper-paramteres 

Hyper-paramteres: k1=0.9 b=0.4 k1_prf=0.9 b_prf=0.4 num_new_termss=20 num_docs=10 new_term_weight=0.2

Command:
```sh
python run.py search \
  --repo osirrc2019/anserini-bm25prf   \
  --output out \
  --qrels qrels/qrels.robust04.txt \
  --topic topics/topics.robust04.txt \
  --collection robust04 
```

|Metric | Score |
|----|----|
| MAP |  0.2928 |
| P@30 | 0.3438 |


#### Tuning BM25+PRF

Command:
```sh
python run.py train \
   --repo osirrc2019/anserini-bm25prf \
   --tag latest \
   --topic topics/topics.robust04.txt \
   --qrels $(pwd)/qrels/qrels.robust04.txt \
   --validation_split $(pwd)/sample_training_validation_query_ids/robust04_validation.txt \
   --test_split $(pwd)/sample_training_validation_query_ids/robust04_test.txt \
   --model_folder $(pwd)/trained \
   --collection robust04
```
Tuned Hyper-paramteres: 

| Paramteres | k1 | b | k1_prf | b_prf | num_new_terms | num_docs | new_term_weight |
|----|----|----|----|----|----|----|----|
| Value |  0.9 | 0.2 | 0.9 | 0.6 | 40 | 10 | 0.1 |


#### BM25+PRF with Tuned Hyper-paramteres 
Hyper-paramteres: k1=0.9 b=0.2 k1_prf=0.9 b_prf=0.6 num_new_temrs=40 num_docs=10 new_term_weight=0.1 

Command:
```sh
 python run.py search \
  --repo osirrc2019/anserini-bm25prf \
  --output out \
  --qrels qrels/qrels.robust04.txt \
  --topic topics/topics.robust04.txt \
  --collection robust04 \
  --opts k1=0.9 b=0.2 k1_prf=0.9 b_prf=0.6 num_new_temrs=40 num_docs=10 new_term_weight=0.1 
```

|Metric | Score |
|----|----|
| MAP |  0.2916 |
| P@30 | 0.3396 |

Yes, the tuned hyper-paramteres make the performance worse.......



## Reference

[1] Stephen E. Robertson, and Karen Spärck Jones. Simple, proven approaches to text retrieval. University of Cambridge Computer Laboratory, 1994.

[2] Peilin Yang, Hui Fang, and Jimmy Lin. Anserini: Enabling the Use of Lucene for Information Retrieval Research. SIGIR 2017