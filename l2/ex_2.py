import networkx as nx
import matplotlib.pyplot as plt

# Criando um grafo exemplo
G = nx.Graph()
edges = [(1,2), (2,3), (3,1),   # Bloco 1 (triângulo)
         (3,4), (4,5), (5,6), (6,4)]  # Bloco 2 (ciclo quadrado)
G.add_edges_from(edges)

# Encontrando pontos de articulação
articulacoes = list(nx.articulation_points(G))
print("Pontos de articulação:", articulacoes)

# Encontrando blocos (componentes biconexos)
blocos = list(nx.biconnected_components(G))
print("Blocos:", blocos)

# Criando grafo bloco-articulado (bipartido)
B = nx.Graph()

# Adicionando vértices para blocos e articulações
for i, bloco in enumerate(blocos):
    bloco_id = f"B{i+1}"  # nome do bloco
    B.add_node(bloco_id, bipartite=0)  # conjunto dos blocos
    for v in bloco:
        if v in articulacoes:
            B.add_node(v, bipartite=1)  # conjunto das articulações
            B.add_edge(bloco_id, v)     # ligação bloco ↔ articulação

# Desenhando o grafo bloco-articulado
plt.figure(figsize=(6,6))
pos = nx.spring_layout(B, seed=42)

nx.draw(B, pos, with_labels=True, node_color="lightgreen", node_size=800, font_size=10, font_weight="bold")
plt.title("Grafo Bloco-Articulado (Bipartido)", fontsize=14)
plt.show()
