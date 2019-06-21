#!/usr/bin/env python3
import json
import numpy as np
import multiprocessing
from runner import Runner, Params, Bm25PRFParams, Bm25Params

K1_RANGE = np.arange(0.1, 1, 0.1)
B_RANGE = np.arange(0.1, 1, 0.1)

PRF_K1_RANGE = np.arange(0.2, 1, 0.1)
PRF_B_RANGE = np.arange(0.1, 1, 0.1)

TERM_WEIGHT_RANGE = [0.1, 0.2, 0.5, 1]
N_TERMS_RANGE = [0, 5, 10, 20, 40]
N_DOCS_RANGE = [5, 10, 20]

# # test 
# K1_RANGE = [0.1, 0.5]
# B_RANGE = [0.2, 0.3]

# PRF_K1_RANGE = [0.1, 0.5]
# PRF_B_RANGE = [0.2, 0.3]

# TERM_WEIGHT_RANGE = [0.1,  1]
# N_TERMS_RANGE = [0,  40]
# N_DOCS_RANGE = [5, 40]


def get_eval_result(runner) -> float:
    return runner()

def bm25_runner(index, topics, output, qrel, k1, b) -> Runner:
    params = Bm25Params(k1=k1, b=b)
    runner = Runner(index, topics, output,
                    model_params=params, eval_method="P.20", qrel_path=qrel)
    return runner


def bm25prf_runner(index, topics, output, qrel, k1, b, k1_prf, b_prf, num_terms, num_docs, weight) -> Runner:
    params = Bm25PRFParams(k1=k1, b=b, k1_prf=k1_prf, b_prf=b_prf,
                           new_term_weight=weight, num_new_terms=num_terms, num_docs=num_docs)
    runner = Runner(index, topics, output,
                    model_params=params, eval_method="map", qrel_path=qrel)
    return runner

def tune_bm25_params(index, topics, output, qrel) -> Params:
    runners = []
    for k1 in K1_RANGE:
        for b in B_RANGE:
            runners.append(bm25_runner(index, topics, output, qrel, k1, b))
    return parallel_tune(runners)


def tune_bm25prf_params(index, topics, output, qrel, k1, b) -> Params:
    runners = []
    for k1_prf in PRF_K1_RANGE:
        for b_prf in PRF_B_RANGE:
            for weight in TERM_WEIGHT_RANGE:
                for num_docs in N_DOCS_RANGE:
                    for num_terms in N_TERMS_RANGE:
                        runners.append(bm25prf_runner(index, topics, output, qrel, k1, b, k1_prf, b_prf,
                                                    num_terms, num_docs, weight))
    return parallel_tune(runners)


def parallel_tune(runners: Runner) -> Params:
    print("%d to run" % len(runners))
    pool = multiprocessing.Pool()
    scores = pool.map(get_eval_result, runners)
    pool.terminate()
    best_runner = None
    highest_score = -999
    for score, runner in zip(scores, runners):
        if score > highest_score:
            highest_score = score
            best_runner = runner
    print("Best Score: %.3f" % highest_score)
    print("Best Params: %s" % best_runner.model_params)
    return best_runner.model_params


def main(index, topics, output, qrels):
    bm25_params = tune_bm25_params(index, topics, output, qrels)
    bm25prf_params = tune_bm25prf_params(index, topics, output, qrels, bm25_params["k1"], bm25_params["b"])
    with open("tuned_params.json", "w") as f:
        json.dump(bm25prf_params, f)
    