import re

def read_ids(path):
    ids = []
    with open(path) as f:
        for l in f:
            ids.append(int(l.strip()))
    return ids

def get_topic_number(topic):
    return int(re.search("Number: (\d+)", topic[0]).groups()[0])

def read_topics(path):
    with open(path) as f:
        lines = f.read()
        topics = re.findall(r"(<top>(.|\n)*?</top>)", lines)
        return {get_topic_number(t):t for t in topics}

def write_topics(topics, path):
    content = "\n\n".join("".join(t) for t in topics.values())
    with open(path, "w") as fout:
        fout.write(content)
        
def get_topics_by_ids(topics, ids, output_path):
    new_topics = {}
    for i in ids:
        new_topics[i] = topics[i]
    write_topics(new_topics, output_path)
    return 

def read_qrels(path):
    with open(path) as f:
        return f.readlines()
    
def get_qrels_by_ids(qrels, ids, output_path):
    ids_set = set(ids)
    new_qrels = []
    for line in qrels:
        if int(line.split()[0]) not in ids_set:
            continue
        new_qrels.append(line)
        
    with open(output_path, 'w') as fout:
        fout.write("".join(new_qrels))
    