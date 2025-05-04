import tkinter as tk
from tkinter import messagebox, ttk

import networkx as nx

# Node_Metrics.py is for handling node's metrics
def show_node_metrics(self):

    # If statement will display an error if the user tried to display the graph without uploading the dataset.
    if self.nodes_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Nodes CSV file first !!!')
        return
    elif self.edges_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Edges CSV file first !!!')
        return

    # The if statement checks is the user has checked the directed graph option.
    if self.Checkbutton1.get() == 0:
        I = nx.Graph()
    else:
        I=nx.DiGraph()

    # For loop to add nodes to draw the graph
    for _, row in self.nodes_df.iterrows():
        I.add_node(row['ID'])

    # # For loop to add edges to draw the graph
    for _, row in self.edges_df.iterrows():
        I.add_edge(row['Source'], row['Target'])

    # Opening a new window to show node's metrics results
    top = tk.Toplevel(self.root)
    top.title("Node's Metrics and Statistics")
    ttk.Label(top, text="Node's Metrics and Statistics").pack()
    stats_text = tk.Text(top, width=60, height=25)
    stats_text.pack(padx=10, pady=10)

    # Get the typed node ID
    node_id = int(self.node_id_entry.get())

    # Compute node degree
    node_degree = I.degree(node_id)

    # Compute cluster coefficient
    node_cluster = nx.clustering(I, node_id)

    # Compute closeness centrality
    node_closeness_centrality = nx.closeness_centrality(I, node_id)

    # Compute harmonic centrality
    node_harmonic_centrality = nx.harmonic_centrality(I, node_id)

    # Printing out the node's metrics outputs
    stats_text.insert(tk.END, f"Node Degree: {node_degree}\n")
    stats_text.insert(tk.END, f'Node Cluster Coefficient: {node_cluster}\n')
    stats_text.insert(tk.END, f"Node Closeness Centrality: {node_closeness_centrality}\n")
    stats_text.insert(tk.END, f"Node Harmonic Centrality: {node_harmonic_centrality}\n")