# AI Campus Route Navigator — Assignment X_03

**Student:** Souhardya banerjee  
**Roll:** 36 
**University:** University of Calcutta  
**Course:** AI/ML Laboratory, B.Tech. 5th Semester

## Project objective
This project converts the supplied CU Technology Campus map into a weighted graph and compares two routing agents:

- **PATHFINDER** — Greedy Best-First Search, `f(n) = h(n)`
- **ORBIT** — A*, `f(n) = g(n) + h(n)`

The implementation also enforces the assignment's special CSE-zone routing rule.

## Repository structure
```text
campus-navigator/
├── main.py
├── campus_map.py
├── search.py
├── agents.py
├── experiment.py
├── campus.json
├── results.csv
├── requirements.txt
├── REPORT.md
└── README.md
```

## How to run
Python 3.9+ is recommended.

```bash
python experiment.py
python main.py
```

No external pathfinding library is used.

## Graph design
`campus.json` stores:
- only locations shown on the supplied map,
- approximate coordinates,
- walkable connections,
- approximate walking costs,
- CSE-zone/tower-entry metadata.

The search algorithms load this file rather than hard-coding the campus graph.

## Heuristic
The heuristic is a straight-line estimate based on the approximate map coordinates. A conservative scale factor is used so the estimate remains below the corresponding map-based walking cost.

## CSE routing constraint
The search state contains the current location, routing mode, and previous location. A CSE-labelled location can only be entered through:

`Tower 2 Front/Rear Entry -> Lift Area -> CSE location`

While inside the CSE zone, only CSE-labelled locations and the Lift Area are permitted. Leaving the CSE zone requires:

`CSE location -> Lift Area -> Tower 2 Front/Rear Entry -> other campus location`

## Experimental results
See `results.csv`. Timing is machine-dependent; route costs and explored-node counts come from this implementation.

## Important academic note
The graph weights and connectivity are an explicit modelling choice based on the supplied map. They should be checked against your own campus knowledge before submission and explained during evaluation.
