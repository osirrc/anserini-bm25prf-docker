import os
import sys
import subprocess




eval_command = "eval/trec_eval.9.0.4/trec_eval -m map src/main/resources/topics-and-qrels/qrels.robust2004.txt %s"

def evaluate(filepath):
    try:
        result = subprocess.getoutput(eval_command % filepath).split()
        score = float(result[-1])
        return score
    except:
        return 0

def check_path(result_root, prefix="run"):
    files = [f for f in os.listdir(result_root) if f.startswith(prefix)]
    best_score = 0
    best_file = None

    for f in files:
        filepath = os.path.join(result_root, f)
        score  = evaluate(filepath)
        if best_score < score:
            best_score = score
            best_file = f
    print("best score: %f" % best_score)
    print(best_file)


metric = sys.argv[2] if len(sys.argv) >= 3 else "map"
root = sys.argv[1] if len(sys.argv) >= 2 else "."

check_path(root)