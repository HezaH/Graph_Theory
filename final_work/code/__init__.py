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

def main(folder: str):
    # Dictionary to store the loaded graphs
    graphs = {}

    # Iterates through all files in the folder
    for file in os.listdir(folder):
        if file.endswith(".g6"):
            file_path = os.path.join(folder, file)
            
            try:
                graph_list = load_graphs_from_graph6_file(file_path)
                graphs[file] = graph_list
                
                # A) Graph visualization
                for i, G in enumerate(graph_list):
                    visualize_graph(G, title=f"{file} - graph {i}")

            except Exception as e:
                print(f"Failed to read {file}: {e}")

    # Display the loaded graphs information
    for name, graph_list in graphs.items():
        total_nodes = sum(G.number_of_nodes() for G in graph_list)
        total_edges = sum(G.number_of_edges() for G in graph_list)
        print(f"{name}: {total_nodes} nodes, {total_edges} edges")


if __name__ == "__main__":
    main(folder=os.path.join("final_work", "data_base"))