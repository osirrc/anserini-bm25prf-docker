
# bm25_command = """
#  target/appassembler/bin/SearchCollection 
#  -topicreader Trec
#  -index %s
#  -topics %s 
#  -output %s
#  -bm25
#  -k1 %.2f
#  -b  %.2f
#  """.replace("\n", "")

# prf_command = """
#  target/appassembler/bin/SearchCollection 
#  -topicreader Trec
#  -index %s
#  -topics %s 
#  -output %s
#  -bm25
#  -k1 %.2f
#  -b  %.2f
#  -bm25prf
#  -bm25prf.k1 %.2f
#  -bm25prf.b %.2f
#  -bm25prf.newTermWeight %.2f
#  -bm25prf.fbTerms %d
#  -bm25prf.fbDocs %d
#  -bm25prf.outputQuery
#  """.replace("\n", "")


class Bm25Params(dict):
    def __init__(self, k1, b):
        super().__init__({
            "bm25": True,
            "k1": k1,
            "b": b,
        })

class Bm25PRFParams(Bm25Params):
    def __init__(self, k1, b, k1_prf, b_prf, new_term_weight, num_new_temrs, num_docs):
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
    def __init__(self, index, topics, output, search_collection_path="target/appassembler/bin/SearchCollection", topicreader="Trec", **kwargs):
        self.search_collection_path = search_collection_path
        self.params = {}
        self.params["topicreader"] = topicreader
        self.params["index"] = index
        self.params["output"] = output
        self.params["topics"] = topics
        self.params.update(kwargs)

    def command(self, **kwargs):
        params = self.params.copy()
        params.update(kwargs)

        command = [self.search_collection_path]

        for p, v in params.items():
            if v == True:
                command.append("-" + p)
            else:
                command.append("-" + p + " " + v)
        return " ".join(command)
