from tkinter import messagebox, ttk
import networkx as nx
from matplotlib import pyplot as plt
import tkinter as tk

def draw_filtered_graph(self, combo, nodes_df, edges_df, node_color, edge_color, node_size,
                        edge_size, algorithm_combo, node_shape_combo, centrality_type, min_val, max_val):
    if nodes_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Nodes CSV file first !!!')
        return
    elif edges_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Edges CSV file first !!!')
        return
    if self.Checkbutton1.get() == 0:
        G = nx.Graph()
    else:
        G=nx.DiGraph()
    # Get Nodes
    node_label_col = combo.get()
    for _, row in nodes_df.iterrows():
        node_id = row['ID']
        G.add_node(node_id, attr=row[node_label_col])

    # Get edges
    for _, row in edges_df.iterrows():
        G.add_edge(row['Source'], row['Target'])

    # Get colors selected
    node_color = node_color  # fallback color if none selected
    edge_color = edge_color  # fallback color

    # Get sizes selected
    try:
        node_size = int(node_size.get())
    except ValueError:
        node_size = 300
    try:
        edge_width = int(edge_size.get())
    except ValueError:
        edge_width = 1

    if centrality_type == "Degree":
        centrality = nx.degree_centrality(G)
    elif centrality_type == "Betweenness":
        centrality = nx.betweenness_centrality(G)
    elif centrality_type == "Closeness":
        centrality = nx.closeness_centrality(G)

    filtered_nodes = [node for node, centrailty in centrality.items()
                      if min_val <= centrailty <= max_val]
    filtered_graph = G.subgraph(filtered_nodes).copy()
    # Get Layout Algorithm
    if algorithm_combo.get() == "Force-Directed (Fruchterman-Reingold)":
        pos = nx.spring_layout(filtered_graph)
    elif algorithm_combo.get() == "Hierarchical (Tree)":
        pos = nx.bipartite_layout(filtered_graph,
                                  nodes=[n for n, d in filtered_graph.degree() if d == 1])  # a basic approximation
    elif algorithm_combo.get() == "Hierarchical (Radial)":
        try:
            pos = nx.kamada_kawai_layout(filtered_graph)  # Often used as a radial alternative
        except:
            pos = nx.spring_layout(filtered_graph)
    elif algorithm_combo.get() == "Eigenvector":
        pos = nx.spectral_layout(filtered_graph)
    elif algorithm_combo.get() == "Circular":
        pos = nx.circular_layout(filtered_graph)
    elif algorithm_combo.get() == "Shell":
        pos = nx.shell_layout(filtered_graph)
    elif algorithm_combo.get() == "Planar":
        try:
            pos = nx.planar_layout(filtered_graph)
        except nx.NetworkXException:
            messagebox.showwarning("Planar Layout Error", "Graph is not planar. Falling back to spring layout.")
            pos = nx.spring_layout(filtered_graph)
    else:
        pos = nx.spring_layout(filtered_graph)

    node_shape_1 = node_shape_combo.get()
    labels = {node: G.nodes[node].get('attr', node) for node in filtered_graph.nodes}

    if len(filtered_graph.nodes) == 0:
        messagebox.showinfo("No Nodes", "No nodes match the selected centrality filter.")
        return

    plt.figure(figsize=(8, 6))

    # Validate the node shape (matplotlib supports a limited set)
    valid_shapes = {'o', 's', '^', 'v', '<', '>', '8', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X'}
    if node_shape_1 not in valid_shapes:
        node_shape_1 = 'o'  # default to circle
    top = tk.Toplevel(self.root)
    top.title("Filter")
    ttk.Label(top, text="Filtered Nodes").pack()
    stats_text = tk.Text(top, width=60, height=25)
    stats_text.pack(padx=10, pady=10)

    for idx, node in enumerate(filtered_graph):
        stats_text.insert(tk.END, f"Node {idx}: {node}\n")
    # Draw nodes, edges, and labels
    nx.draw_networkx_nodes(filtered_graph, pos, node_color=node_color, node_size=node_size, node_shape=node_shape_1)
    nx.draw_networkx_edges(filtered_graph, pos, edge_color=edge_color, width=edge_width)
    nx.draw_networkx_labels(filtered_graph, pos, labels, font_size=9)
    plt.title(f"Filtered Graph ({centrality_type} ∈ [{min_val}, {max_val}])")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
