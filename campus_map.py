from search import CampusGraph

def load_campus(path="campus.json"):
    return CampusGraph.from_json(path)
