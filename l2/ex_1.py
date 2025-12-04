import networkx as nx
import matplotlib.pyplot as plt

# Criando um grafo simples
G = nx.Graph()

# Adicionando vértices (nós)
V = [1, 2, 3, 4, 5 ,6]
G.add_nodes_from(V)

# Adicionando arestas
E = [(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,5),(4,5)]
G.add_edges_from(E)

# Desenhando o grafo
plt.figure(figsize=(6, 6))
nx.draw(G, with_labels=True, node_color='lightblue', node_size=800, font_size=12, font_weight='bold')
plt.title("Exemplo de Grafo com NetworkX", fontsize=14)
plt.show()
