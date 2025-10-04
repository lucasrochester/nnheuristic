
import matplotlib.pyplot as plt
import networkx as nx

# Plot the results using a tour graph
def plot_tour_graph(coords, route, title="Tour Graph"):
    G = nx.DiGraph()
    num_cities = len(coords)

    # Add nodes
    for i in range(num_cities):
        G.add_node(i, pos=(coords[i, 0], coords[i, 1]))

    # Add edges based on the route
    for i in range(num_cities):
        for j in range(num_cities):
            if route[i, j] > 0.5:
                G.add_edge(i, j)

    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(20, 20))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10, font_weight='bold')
    plt.title(title)
    plt.show()
