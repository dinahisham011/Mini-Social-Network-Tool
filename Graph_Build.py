from tkinter import messagebox
import networkx as nx
from matplotlib import pyplot as plt

# Graph_Build is made to draw the graph based on custom nodes and edge attributes chosen by the user
def draw_graph(self,combo,nodes_df,edges_df,node_color,edge_color,node_size,edge_size,algorithm_combo,node_shape_combo):
    # If statement will display an error if the user tried to display the graph without uploading the dataset.
    if nodes_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Nodes CSV file first !!!')
        return
    elif edges_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Edges CSV file first !!!')
        return

    # The if statement checks is the user has checked the directed graph option.
    if self.Checkbutton1.get() == 0:
        G = nx.Graph()
    else:
        G=nx.DiGraph()

    # This gets the value from Label combobox so that the graph will be drowned using the chosen label
    node_label_col = combo.get()
    # For loop to add nodes to draw the graph
    for _, row in nodes_df.iterrows():
        node_id = row['ID']
        G.add_node(node_id, attr=row[node_label_col])

    # For loop to add edges to draw the graph
    for _, row in edges_df.iterrows():
        G.add_edge(row['Source'], row['Target'])

    # Get sizes selected and if error happened make a default value
    try:
        node_size = int(node_size.get())
    except ValueError:
        node_size = 300
    try:
        edge_width = int(edge_size.get())
    except ValueError:
        edge_width = 1

    # Gets Layout Algorithm from Layout Algorithm combobox so that the graph will be drowned using the chosen Algorithm
    if algorithm_combo.get() == "Force-Directed (Fruchterman-Reingold)":
        pos = nx.spring_layout(G)
    elif algorithm_combo.get() == "Hierarchical (Tree)":
        pos = nx.bipartite_layout(G, nodes=[n for n, d in G.degree() if d == 1])  # a basic approximation
    elif algorithm_combo.get() == "Hierarchical (Radial)":
        try:
            pos = nx.kamada_kawai_layout(G)  # Often used as a radial alternative
        except:
            pos = nx.spring_layout(G)
    elif algorithm_combo.get() == "Eigenvector":
        pos = nx.spectral_layout(G)
    elif algorithm_combo.get() == "Circular":
        pos = nx.circular_layout(G)
    elif algorithm_combo.get() == "Shell":
        pos = nx.shell_layout(G)
    elif algorithm_combo.get() == "Planar":
        try:
            pos = nx.planar_layout(G)
        except nx.NetworkXException:
            messagebox.showwarning("Planar Layout Error", "Graph is not planar. Falling back to spring layout.")
            pos = nx.spring_layout(G)
    else:
        pos = nx.spring_layout(G)

    # This gets the shape from shape combobox so that the graph will be drowned using the chosen shape
    node_shape_1 = node_shape_combo.get()

    # Getting the label to add to networkx
    labels = {node: G.nodes[node]['attr'] for node in G.nodes}

    # This rest of the code is to add edges, nodes and labels to networkx and customizing the figure
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

    nx.draw_networkx_nodes(G, pos,
                           node_color=node_color,
                           node_size=node_size,
                           node_shape=node_shape_1)
    nx.draw_networkx_edges(G, pos,
                           edge_color=edge_color,
                           width=edge_width)
    plt.title("Social Network Graph")
    plt.axis('off')
    plt.tight_layout()
    plt.show()