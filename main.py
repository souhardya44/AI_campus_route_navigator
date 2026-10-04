from campus_map import load_campus
from agents import Pathfinder, Orbit

def print_result(agent_name, result):
    print(f"\n{agent_name}")
    print("Route:", " -> ".join(result.route) if result.route else "No route found")
    print(f"Cost: {result.cost:.0f} m")
    print(f"Nodes explored: {result.explored}")
    print(f"Time: {result.elapsed:.6f} s")

def main():
    graph = load_campus()
    pathfinder = Pathfinder(graph)
    orbit = Orbit(graph)

    locations = sorted(graph.nodes)
    print("AI Campus Route Navigator")
    print("Available locations:")
    for i, name in enumerate(locations, 1):
        print(f"{i:2}. {name}")

    start = input("\nEnter starting location: ").strip()
    goal = input("Enter destination: ").strip()

    if start not in graph.nodes or goal not in graph.nodes:
        print("Invalid location. Please use a location exactly as listed above.")
        return

    print_result("PATHFINDER", pathfinder.solve(start, goal))
    print_result("ORBIT", orbit.solve(start, goal))

if __name__ == "__main__":
    main()
