# Brief Report — AI Campus Route Navigator

## 1. Objective
The assignment asks for a campus graph and two AI routing agents: PATHFINDER using Greedy Best-First Search and ORBIT using A*. The goal is to compare their routes, path costs, explored nodes, and execution time.

## 2. Graph construction
The graph uses only the named locations visible in the supplied campus map. Connections and weights were modelled from the map layout. The graph is stored separately in `campus.json`, so the search code is not tied to one hard-coded campus layout.

Approximate edge weights are represented in metres. They are modelling estimates, not surveyed walking distances.

## 3. Heuristic
For a node `n` and destination `d`, the heuristic is a scaled Euclidean distance between their approximate map coordinates:

`h(n) = 0.55 × sqrt((x_n-x_d)^2 + (y_n-y_d)^2)`

The same heuristic is used by both agents.

## 4. Algorithms
### PATHFINDER
PATHFINDER uses Greedy Best-First Search and prioritizes the node with the smallest `h(n)`. It therefore focuses on apparent closeness to the destination and does not include the distance already travelled in its priority.

### ORBIT
ORBIT uses A* and prioritizes `g(n)+h(n)`, where `g(n)` is the cost accumulated so far. This allows the search to balance progress toward the goal with the route already travelled.

## 5. CSE-zone constraint
The CSE Laboratory, CSE_AKC Seminar Hall, and CSE_Reflexon Room are treated as the CSE zone. Entry and exit are enforced through the Lift Area and Tower 2 Front/Rear Entry. The search state records the current routing mode and previous node, so invalid transitions are not generated.

## 6. Experimental observations
The included `results.csv` records six source-destination experiments, including ordinary routes and CSE-related routes.

Typical observations from this graph:
- Greedy Best-First can reach a destination with fewer explored nodes, but it is not guaranteed to minimize path cost.
- A* considers the accumulated cost and can select a longer-looking intermediate step when that produces a cheaper complete route.
- The two agents can return different routes when a locally attractive route has a higher accumulated cost.
- The CSE constraint can force detours that would otherwise look unnecessary.
- Execution times are very small for this graph and can vary between runs and machines, so they should be treated as indicative rather than absolute.

## 7. Conclusion
The experiment demonstrates the central question in the assignment: the location that appears closest to the destination is not necessarily the best next choice. Greedy Best-First Search optimizes only the heuristic estimate at each expansion, while A* combines the cost already travelled with the estimated remaining cost.

The project separates graph data, search algorithms, agents, experiments, and the user interface, satisfying the requested OOP/file-handling structure.
