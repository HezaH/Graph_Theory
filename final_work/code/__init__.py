import os
import networkx as nx
import matplotlib.pyplot as plt

def visualizar_grafo(G, titulo="Visualização do Grafo"):
    """
    Função para visualizar um grafo usando NetworkX e Matplotlib.
    
    Parâmetros:
    - G: grafo do NetworkX
    - titulo: título exibido na figura
    """
    plt.figure(figsize=(6,6))
    pos = nx.spring_layout(G, seed=42)  # layout para posicionar os nós
    
    nx.draw(
        G, pos,
        with_labels=True,
        node_color="lightblue",
        node_size=800,
        font_size=10,
        font_weight="bold",
        edge_color="gray"
    )
    
    plt.title(titulo, fontsize=14)
    plt.show()

def main(folder: str):
    # Lista para armazenar os grafos lidos
    grafos = {}

    # Percorre todos os arquivos da foldder
    for arquivo in os.listdir(folder):
        if arquivo.endswith(".g6"):
            caminho_arquivo = os.path.join(folder, arquivo)
            
            # Lê o grafo no formato Graph6
            with open(caminho_arquivo, "rb") as f:
                G = nx.from_graph6_bytes(f.read())

            visualizar_grafo(G, titulo=arquivo)
            
            # Armazena no dicionário com o nome do arquivo como chave
            grafos[arquivo] = G
            
    # Exemplo: mostrar os grafos carregados
    for nome, G in grafos.items():
        print(f"{nome}: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")


if __name__ == "__main__":
    main(folder="final_work/data_base")