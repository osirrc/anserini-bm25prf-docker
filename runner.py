import os
import subprocess

# TOPICS_DEV = "data/topics.dev.txt"
# TOPICS_TEST = "data/topics.test.txt"
# QRELS_DEV = "data/qrels.dev.txt"
# QRELS_TEST = "data/qrels.test.txt"

class Params(dict):
    pass

class Bm25Params(dict):
    def __init__(self, k1=0.9, b=0.4):
        super().__init__({
            "bm25": True,
            "k1": k1,
            "b": b,
        })

class Bm25PRFParams(Bm25Params):
    def __init__(self, k1=0.9, b=0.4, k1_prf=0.9, b_prf=0.4, new_term_weight=0.2, num_new_temrs=20, num_docs=10):
        super().__init__(k1, b)
        self.update({
            "bm25prf": True,
            "bm25prf.k1": k1_prf,
            "bm25prf.b": b_prf,
            "bm25prf.newTermWeight": new_term_weight,
            "bm25prf.fbTerms": num_new_temrs,
            "bm25prf.fbDocs": num_docs
        })


class Runner(object):
    def __init__(self, index, topics, 
                 output_dir="out",
                 search_collection_path="Anserini/target/appassembler/bin/SearchCollection",
                 eval_path="Anserini/eval/trec_eval.9.0.4/trec_eval",
                 topicreader="Trec",
                 model_params=None, eval_method="map", qrel_path=None, topk=500):

        self.search_collection_path = search_collection_path
        self.eval_path = eval_path
        self.output_dir = output_dir
        self.eval_method = eval_method
        self.qrel_path = qrel_path
        self.model_params = model_params

        self.params = {}
        self.params["topicreader"] = topicreader
        self.params["index"] = index
        self.params["topics"] = topics
        self.params.update(model_params)

    def _build_command(self):
        command = [self.search_collection_path]

        output_filename_builder = []

        for p, v in sorted(list(self.params.items())):
            if v == True:
                command.append("-" + p)
                output_filename_builder.append(p)
            else:
                if isinstance(v, float):
                    v = "%.2f"%v
                command.append("-" + p + " " + str(v))

                if not p.startswith("topic"):
                    output_filename_builder.append("%s=%s" % (p, v))

        ouput_filename = os.path.join(self.output_dir, "_".join(output_filename_builder))
        command.append("-output %s" % ouput_filename)
        cmd = " ".join(command)
        print(cmd)
        return cmd, ouput_filename

    def __call__(self) -> float:
        cmd, output_file = self._build_command()
        result = subprocess.getoutput(cmd)
        print(result)
        eval_command = "%s -m %s %s %s" % (self.eval_path,
                                           self.eval_method, self.qrel_path, output_file)
        eval_result = subprocess.getoutput(eval_command)
        print(eval_result)
        score = float(eval_result.split("\t")[-1])
        return score