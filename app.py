import numpy as np
import time
from data_generation import generate_data
from visualizations import plot_tour_graph
import matplotlib.pyplot as plt

# -------------------------------
# Solver Function
# -------------------------------
def nearest_neighbor_solver_with_penalties(coords, time_windows, travel_time):
    num_cities = len(coords)
    visited = [False] * num_cities
    current_city = 0
    visited[current_city] = True
    route = [current_city]
    total_cost = 0
    current_time = 0

    while len(route) < num_cities:
        nearest_city = None
        min_distance = float('inf')

        for next_city in range(num_cities):
            if not visited[next_city] and travel_time[current_city, next_city] < min_distance:
                nearest_city = next_city
                min_distance = travel_time[current_city, next_city]

        # Travel
        current_time += min_distance

        # Penalties
        earliest, latest = time_windows[nearest_city]
        penalty = 0
        if current_time < earliest:
            penalty += earliest - current_time
            current_time = earliest
        elif current_time > latest:
            penalty += current_time - latest

        total_cost += min_distance + penalty
        visited[nearest_city] = True
        route.append(nearest_city)
        current_city = nearest_city

    # Return to origin
    return_distance = travel_time[current_city, route[0]]
    current_time += return_distance
    earliest, latest = time_windows[route[0]]
    penalty = 0
    if current_time < earliest:
        penalty += earliest - current_time
        current_time = earliest
    elif current_time > latest:
        penalty += current_time - latest

    total_cost += return_distance + penalty
    route.append(route[0])

    return route, total_cost


# -------------------------------
# Helper Function
# -------------------------------
def convert_route_to_adjacency_matrix(route, num_cities):
    adj_matrix = np.zeros((num_cities, num_cities))
    for i in range(len(route) - 1):
        adj_matrix[route[i], route[i + 1]] = 1
    return adj_matrix


# -------------------------------
# Main Interactive Console App
# -------------------------------
def main():
    print("🚗 Nearest Neighbor TSP Solver with Time Windows")
    num_cities = int(input("Enter the number of cities: "))
    seed = int(input("Enter random seed (e.g., 42): ") or 42)
    lagrangian_lower_bound = float(input("Enter Lagrangian lower bound (optional, default 100): ") or 100)

    print("\nGenerating data...")
    coords, time_windows, travel_time = generate_data(num_cities, seed=seed)

    print("Solving...")
    start_time = time.time()
    route, total_cost = nearest_neighbor_solver_with_penalties(coords, time_windows, travel_time)
    solve_time = time.time() - start_time

    opt_gap = ((total_cost - lagrangian_lower_bound) / lagrangian_lower_bound) * 100

    print("\n✅ Solution Found!")
    print(f"Total Cost: {total_cost:.4f}")
    print(f"Solve Time: {solve_time:.4f} seconds")
    print(f"Optimality Gap: {opt_gap:.2f}%")
    print("Tour Path:", route)

    adj_matrix = convert_route_to_adjacency_matrix(route, num_cities)
    print("\nPlotting tour...")
    plot_tour_graph(coords, adj_matrix, title="Nearest Neighbor Tour")

    plt.show()


if __name__ == "__main__":
    main()
