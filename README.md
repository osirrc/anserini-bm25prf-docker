# Implemented BM25 + Pesudo Relevance Feedback with Anserini

## Prepare
```
python run.py prepare \
  --repo mathewzz/bm25prf   \
  --tag latest \
  --collections robust04=/home/ryan/sync/ir/collections/disk45=trectext
```

## Search
```
python run.py search \
  --repo mathewzz/bm25prf \
  --tag latest \
  --output $(pwd)/out \
  --qrels qrels/qrels.robust2004.txt \
  --topic topics.robust04.301-450.601-700.txt \
  --collection robust04
```