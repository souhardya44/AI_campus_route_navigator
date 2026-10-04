"""
AI Campus Route Navigator
Assignment X_03

Graph data is loaded from campus.json. Search algorithms are implemented
from scratch; no pathfinding library is used.
"""
import heapq, json, math, time
from pathlib import Path

CSE_ZONE = {"CSE Laboratory", "CSE_AKC Seminar Hall", "CSE_Reflexon Room"}
TOWER_ENTRIES = {"Tower 2 Front Entry", "Tower 2 Rear Entry"}

class CampusGraph:
    def __init__(self, data):
        self.nodes = data["nodes"]
        self.edges = data["edges"]
        self.adj = {name: [] for name in self.nodes}
        for e in self.edges:
            self.adj[e["from"]].append((e["to"], e["weight_m"]))
            self.adj[e["to"]].append((e["from"], e["weight_m"]))

    @classmethod
    def from_json(cls, path="campus.json"):
        with open(path, "r", encoding="utf-8") as f:
            return cls(json.load(f))

    def heuristic(self, node, goal):
        a, b = self.nodes[node], self.nodes[goal]
        # A conservative straight-line estimate.
        return math.hypot(a["x"]-b["x"], a["y"]-b["y"]) * 0.55

    def valid_neighbors(self, state):
        """
        state = (node, mode, previous_node)
        mode:
          normal    : ordinary campus traversal
          cse       : inside CSE zone
          cse_exit  : at Lift Area after leaving CSE; must go to Tower 2 entry
        """
        node, mode, previous = state
        for nxt, weight in self.adj[node]:
            if mode == "normal":
                if nxt in CSE_ZONE:
                    # Entry to CSE is permitted only through Tower 2 Entry -> Lift -> CSE.
                    if node == "Lift Area" and previous in TOWER_ENTRIES:
                        yield nxt, weight, "cse"
                else:
                    yield nxt, weight, "normal"

            elif mode == "cse":
                # Once inside, only CSE-labelled locations or Lift may be visited.
                if nxt in CSE_ZONE:
                    yield nxt, weight, "cse"
                elif nxt == "Lift Area":
                    yield nxt, weight, "cse_exit"

            elif mode == "cse_exit":
                # Exit must be CSE -> Lift -> Tower 2 Entry -> other campus locations.
                if node == "Lift Area" and nxt in TOWER_ENTRIES:
                    yield nxt, weight, "normal"


class SearchResult:
    def __init__(self, route, cost, explored, elapsed):
        self.route = route
        self.cost = cost
        self.explored = explored
        self.elapsed = elapsed


class SearchEngine:
    def __init__(self, graph):
        self.graph = graph

    def _run(self, start, goal, strategy):
        initial = (start, "normal", None)
        counter = 0
        heap = []
        h0 = self.graph.heuristic(start, goal)
        initial_score = h0
        heapq.heappush(heap, (initial_score, 0.0, counter, initial))

        best_g = {initial: 0.0}
        parent = {initial: None}
        explored = 0
        t0 = time.perf_counter()

        while heap:
            score, g, _, state = heapq.heappop(heap)
            if g != best_g.get(state):
                continue

            explored += 1
            if state[0] == goal:
                route = []
                cur = state
                while cur is not None:
                    route.append(cur[0])
                    cur = parent[cur]
                route.reverse()
                return SearchResult(route, g, explored, time.perf_counter() - t0)

            for nxt, weight, mode in self.graph.valid_neighbors(state):
                new_state = (nxt, mode, state[0])
                new_g = g + weight
                if new_g < best_g.get(new_state, float("inf")):
                    best_g[new_state] = new_g
                    parent[new_state] = state
                    counter += 1
                    h = self.graph.heuristic(nxt, goal)
                    priority = h if strategy == "greedy" else new_g + h
                    heapq.heappush(heap, (priority, new_g, counter, new_state))

        return SearchResult([], float("inf"), explored, time.perf_counter() - t0)

    def greedy_best_first(self, start, goal):
        return self._run(start, goal, "greedy")

    def a_star(self, start, goal):
        return self._run(start, goal, "astar")


class Agent:
    def __init__(self, name, search_method, graph):
        self.name = name
        self.search_method = search_method
        self.engine = SearchEngine(graph)

    def solve(self, start, goal):
        return self.search_method(self.engine, start, goal)


class Pathfinder(Agent):
    def __init__(self, graph):
        super().__init__("PATHFINDER", SearchEngine.greedy_best_first, graph)


class Orbit(Agent):
    def __init__(self, graph):
        super().__init__("ORBIT", SearchEngine.a_star, graph)
