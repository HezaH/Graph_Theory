import os
import networkx as nx
import matplotlib.pyplot as plt

def load_graphs_from_graph6_file(path):
    """
    Reads a .g6 file that can contain one or more graphs (one per line).
    Returns a list of NetworkX graphs.
    """
    graphs = []
    with open(path, "rb") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            # Ignores optional ">>graph6<<" header if it appears
            if line == b">>graph6<<":
                continue
            # Graph6 typically starts without ":"; Sparse6 starts with ":".
            if line.startswith(b":"):
                # Sparse6 line
                G = nx.from_sparse6_bytes(line)
            else:
                # Graph6 line
                G = nx.from_graph6_bytes(line)
            graphs.append(G)
    return graphs

def visualize_graph(G, title="Graph Visualization"):
    """
    Function to visualize a graph using NetworkX and Matplotlib.
    
    Parameters:
    - G: NetworkX graph
    - title: title displayed in the figure
    """
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G, seed=42)  # layout to position the nodes
    
    nx.draw(
        G, pos,
        with_labels=True,
        node_color="lightblue",
        node_size=800,
        font_size=10,
        font_weight="bold",
        edge_color="gray"
    )
    
    plt.title(title, fontsize=14)
    plt.show()

def calculate_centralities(G: nx.Graph, centralities: dict):
    """
    Calculates and displays centrality measures for a graph.
    
    Parameters:
    - G: NetworkX graph
    - centralities: dictionary {name: centrality_function}
    """
    for name, method in centralities.items():
        print(f"\n>>> {name} Centrality:")
        try:
            values = method(G)  # applies the function to the graph
            for node, value in values.items():
                print(f"Node {node}: {value:.4f}")
        except Exception as e:
            print(f"Error calculating {name}: {e}")

def evaluate_connectivity(G):
    """
    Evaluate basic connectivity measures of a graph.
    
    Parameters:
    - G: NetworkX graph
    
    Returns:
    - dictionary with:
        * number of connected components
        * size of the largest connected component
        * diameter of the graph (largest component)
    """
    # Number of connected components
    num_components = nx.number_connected_components(G)
    
    # Largest connected component
    components = list(nx.connected_components(G))
    largest_component = max(components, key=len)
    largest_size = len(largest_component)
    
    # Subgraph induced by the largest component
    largest_subgraph = G.subgraph(largest_component)
    
    # Diameter of the largest component
    diameter = nx.diameter(largest_subgraph)
    
    result = {
        "Number of connected components": num_components,
        "Size of largest component": largest_size,
        "Graph diameter": diameter
    }
    for key, value in result.items():
        print(f"{key}: {value}")


def main(folder: str):
    # Dictionary to store the loaded graphs
    graphs = {}

    dict_centralities = {
        "Degree": nx.degree_centrality,
        "Closeness": nx.closeness_centrality,
        "Betweenness": nx.betweenness_centrality,
        "Eigenvector": nx.eigenvector_centrality
    }
    dict_connectivity = {
        "Node Connectivity": nx.node_connectivity,
        "Edge Connectivity": nx.edge_connectivity,
        "Algebraic Connectivity": nx.algebraic_connectivity
    }

    # Iterates through all files in the folder
    for file in os.listdir(folder):
        if file.endswith(".g6"):
            file_path = os.path.join(folder, file)
            
            try:
                graph_list = load_graphs_from_graph6_file(file_path)
                graphs[file] = graph_list
                
                for i, G in enumerate(graph_list):
                    #! A) Graph visualization
                    visualize_graph(G, title=f"{file} - graph {i}")
                    #! B) Centrality calculations
                    calculate_centralities(G, dict_centralities)
                    #! C) Connectivity evaluation
                    evaluate_connectivity(G)
                    #! C2) Algebraic connectivity
                    calculate_centralities(G, dict_connectivity)
                    
            except Exception as e:
                print(f"Failed to read {file}: {e}")

    # Display the loaded graphs information
    for name, graph_list in graphs.items():
        total_nodes = sum(G.number_of_nodes() for G in graph_list)
        total_edges = sum(G.number_of_edges() for G in graph_list)
        print(f"{name}: {total_nodes} nodes, {total_edges} edges")


if __name__ == "__main__":
    main(folder=os.path.join("final_work", "data_base"))