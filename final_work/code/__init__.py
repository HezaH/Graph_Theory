import os
import networkx as nx
import matplotlib.pyplot as plt
import statistics
import pandas as pd

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

def visualize_graph(G, title="Graph Visualization", file_name="graph.png"):
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G, seed=42)
    
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
    plt.savefig(file_name)   # save instead of show
    plt.close()              # close the figure so nothing opens

def plot_adjacency_matrix(G: nx.Graph, title: str = "Adjacency Matrix", file_name="adjacency_matrix.png"):
    """
    Exibe a matriz de adjacência do grafo como um heatmap.
    - Mostra rótulos de nós quando o grafo é pequeno (<= 20 nós).
    - Abre a janela de plot (plt.show()).
    """
    # Define ordem estável de nós (tenta ordenar caso comparáveis)
    nodes = list(G.nodes())
    try:
        nodes = sorted(nodes)
    except Exception:
        pass

    A = nx.to_numpy_array(G, nodelist=nodes, dtype=float)

    plt.figure(figsize=(6, 6))
    im = plt.imshow(A, cmap="Blues", interpolation="nearest")
    plt.title(title, fontsize=14)
    plt.xlabel("Nodes")
    plt.ylabel("Nodes")

    n = len(nodes)
    if n <= 20:
        plt.xticks(range(n), nodes, rotation=90)
        plt.yticks(range(n), nodes)
    else:
        plt.xticks([])
        plt.yticks([])

    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(file_name)   # save instead of show
    plt.close()              # close the figure so nothing opens

def calculate_centralities(G: nx.Graph, measures: dict):
    """
    Apply a set of measures (centralities/connectivities) to a graph.
    measures: dict {label: function}
    """
    results = {}
    for label, func in measures.items():
        try:
            if label == "Algebraic Connectivity":
                result = func(G, method="lanczos") #"tracemin"
            # Some functions require parameters (like Katz centrality)
            elif label == "Katz Centrality":
                result = func(G, alpha=0.005, beta=1.0, max_iter=2000)
            elif label == "PageRank":
                result = func(G, alpha=0.85)
            else:
                result = func(G)
            print(f"\n>>> {label}:")
            
            # If result is a dict (per-node values)
            if isinstance(result, dict):
                # Calculate summary statistics
                values = list(result.values())
                average_value = sum(values) / len(values)
                min_value = min(values)
                max_value = max(values)
                std_dev = statistics.pstdev(values)  # desvio padrão populacional
                
                # Print results
                results[label] = {
                    "Average": average_value,
                    "Minimum": min_value,
                    "Maximum": max_value,
                    "Standard Deviation": std_dev
                }
                print(f"Average_{label}: {average_value:.4f}")
                print(f"Minimum_{label}: {min_value:.4f}")
                print(f"Maximum_{label}: {max_value:.4f}")
                print(f"Standard_Deviation_{label}: {std_dev:.4f}")

            else:
                # Single numeric value
                print(f"Value: {result}")
                
        except Exception as e:
            print(f"Error computing {label}: {e}")
    return results

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
    print("\n>>> Connectivity Measures:")
    for key, value in result.items():
        print(f"{key}: {value}")
    return result

def main(folder: str):
    # Dictionary to store the loaded graphs
    graphs = {}

    dict_centralities = {
        #Standard centrality measures
        "Degree": nx.degree_centrality,
        "Closeness": nx.closeness_centrality,
        "Betweenness": nx.betweenness_centrality,
        "Eigenvector": nx.eigenvector_centrality,
        
        # Additional centrality measures
        "Katz Centrality": nx.katz_centrality,
        "PageRank": nx.pagerank,
        "Harmonic Centrality": nx.harmonic_centrality,
        "Current-flow Betweenness": nx.current_flow_betweenness_centrality
    }
    dict_connectivity = {
        #Standard connectivity measures
        "Node Connectivity": nx.node_connectivity,
        "Edge Connectivity": nx.edge_connectivity,
        "Algebraic Connectivity": nx.algebraic_connectivity,

        # Additional connectivity measures
        "Average Node Connectivity": nx.average_node_connectivity,
        "Graph Density": nx.density,  # razão entre arestas existentes e possíveis
        "Average Shortest Path Length": nx.average_shortest_path_length,  # eficiência global
        "Global Clustering Coefficient": nx.transitivity,  # tendência de formar triângulos
        "Minimum Node Cut": nx.minimum_node_cut,  # conjunto mínimo de vértices críticos
        "Minimum Edge Cut": nx.minimum_edge_cut   # conjunto mínimo de arestas críticas
    }
    results_df = pd.DataFrame()

    # Iterates through all files in the folder
    for file in os.listdir(folder):
        if file.endswith(".g6"):
            file_path = os.path.join(folder, file)
            print(f"\nProcessing file: {file}")
            try:
                graph_list = load_graphs_from_graph6_file(file_path)
                graphs[file] = graph_list
                
                for i, G in enumerate(graph_list):
                    #! A) Graph visualization
                    visualize_graph(G, title=f"{file} - graph {i}", file_name=f"graph_{file}_graph_{i}.png")
                    #! A2) Adjacency matrix
                    plot_adjacency_matrix(G, title=f"Adjacency Matrix - {file} - graph {i}", file_name=f"adjacency_{file}_graph_{i}.png")
                    #! B) Centrality calculations
                    results_centralities = calculate_centralities(G, dict_centralities)
                    #! C) Connectivity evaluation
                    dict_evaluate = evaluate_connectivity(G)
                    #! C2) Algebraic connectivity
                    results_connectivity = calculate_centralities(G, dict_connectivity)

                    new_row = {
                        "File": file,
                        "Graph_Index": i,
                        "Num_Nodes": G.number_of_nodes(),
                        "Num_Edges": G.number_of_edges(),
                        **{f"Centrality_{k}_{stat}": v for k, stats in results_centralities.items() for stat, v in stats.items()},
                        **{f"Connectivity_{k}_{stat}": v for k, stats in results_connectivity.items() for stat, v in stats.items()},
                        **{k: v for k, v in dict_evaluate.items()}
                    }
                    results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)

            except Exception as e:
                print(f"Failed to read {file}: {e}")

            print(f"\n>>> Finished processing {file}.")

    # Display the loaded graphs information
    for name, graph_list in graphs.items():
        total_nodes = sum(G.number_of_nodes() for G in graph_list)
        total_edges = sum(G.number_of_edges() for G in graph_list)
        print(f"{name}: {total_nodes} nodes, {total_edges} edges")

if __name__ == "__main__":
    main(folder=os.path.join("final_work", "data_base"))