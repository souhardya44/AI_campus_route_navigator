import csv
from campus_map import load_campus
from agents import Pathfinder, Orbit

EXPERIMENTS = [
    ("Reception of Calcutta University", "Library"),
    ("Canteen, CU Technology Campus", "New Building 2 (Workshop Building)"),
    ("Entry Gate 1 (G1)", "CSE Laboratory"),
    ("Auditorium Hall", "CSE_AKC Seminar Hall"),
    ("Library", "Canteen, CU Technology Campus"),
    ("CSE_Reflexon Room", "Entry Gate 4 (G4)"),
]

def run_experiments():
    graph = load_campus()
    pathfinder = Pathfinder(graph)
    orbit = Orbit(graph)
    rows = []

    for start, goal in EXPERIMENTS:
        for agent in (pathfinder, orbit):
            result = agent.solve(start, goal)
            rows.append({
                "start": start,
                "destination": goal,
                "agent": agent.name,
                "route": " -> ".join(result.route),
                "path_cost_m": round(result.cost, 2),
                "nodes_explored": result.explored,
                "time_seconds": round(result.elapsed, 6),
            })

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows

if __name__ == "__main__":
    run_experiments()
    print("Saved results.csv")
