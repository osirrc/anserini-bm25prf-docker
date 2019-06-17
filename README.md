# OSIRRC Docker Image for Anserini+BM25PRF

[**Zhaohao Zeng**](https://github.com/matthew-z)

This readme is heavily based (i.e. copied from) the Anserini readme.

This is the docker image for BM25PRF conforming to the [OSIRRC jig](https://github.com/osirrc/jig/) for the [Open-Source IR Replicability Challenge (OSIRRC) at SIGIR 2019](https://osirrc.github.io/osirrc2019/).

This image is available on [Docker Hub](https://hub.docker.com/r/matthewzz/anserini_bm25prf).
<!-- The [OSIRRC 2019 image library](https://github.com/osirrc/osirrc2019-library) contains a log of successful executions of this image. -->

This image implemented Bm25+Pseudo Relevance Feedback(PRF) with Anserini.

+ Supported test collections: `robust04`
+ Supported hooks: `init`, `index`, `search`, `interact`


## Quick Start

The following `jig` command can be used to index TREC disks 4/5 for `robust04`:

```bash
python run.py prepare \
  --repo matthewzz/anserini_bm25prf   \
  --tag latest \
  --collections robust04=/path/to/disk45=trectext
```

The following `jig` command can be used to perform a retrieval run on the collection with the `robust04` test collection with default params.

```
python run.py search \
  --repo matthewzz/anserini_bm25prf   \
  --output out \
  --qrels qrels/qrels.robust04.txt \
  --topic topics/topics.robust04.txt \
  --collection robust04 \ 
  --top_k 100
```

The following `jig` command can be used to tune the hyper-parameters (first 50 topics in `robust04` will be used as validation set).
Note that the grid search may take several hours.
```
python run.py interact \
  --repo matthewzz/anserini_bm25prf \
  --tag latest \
```


## Expected Results

The following numbers should be able to be re-produced using the scripts provided by the jig.


### robust04
[TREC 2004 Robust Track Topics](http://trec.nist.gov/data/robust/04.testset.gz).
+ **BM25+PRF**: k1=0.9, b=0.4, k1_prf=0.9, b_prf=0.4, num_new_temrs=20, num_docs=10, new_term_weight=0.2

|Metric | Score |
|----|----|
| MAP |  0.2928 |
| P@30 | 0.3438 |

