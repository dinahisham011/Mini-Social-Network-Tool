from tkinter import messagebox, ttk
import networkx as nx
import tkinter as tk

# Metrics.py is made to handle graph metrics and statistics

def show_metrics(self):

    # If statement will display an error if the user tried to display the graph without uploading the dataset.
    if self.nodes_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Nodes CSV file first !!!')
        return
    elif self.edges_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Edges CSV file first !!!')
        return

    # The if statement checks is the user has checked the directed graph option.
    if self.Checkbutton1.get() == 0:
        B = nx.Graph()
    else:
        B=nx.DiGraph()

    # For loop to add nodes to draw the graph
    for _, row in self.nodes_df.iterrows():
        node_id = row['ID']
        B.add_node(node_id)

    # For loop to add edges to draw the graph
    for _, row in self.edges_df.iterrows():
        B.add_edge(row['Source'], row['Target'])

    # Gets number of nodes and edges
    numberOfNodes = B.number_of_nodes()
    numberOfEdges = B.number_of_edges()

    # Opening a new window to show graph's metrics results
    top = tk.Toplevel(self.root)
    top.title("Graph's Metrics and Statistics")
    ttk.Label(top, text="Graph's Metrics and Statistics").pack()
    stats_text = tk.Text(top, width=60, height=25)
    stats_text.pack(padx=10, pady=10)

    # Computing average degree
    degrees = dict(B.degree())
    averageDegree = sum(degrees.values()) / numberOfNodes

    # Computing cluster coefficient
    averageClustering = nx.average_clustering(B)

    # Computing average closeness centrality
    closenesses = nx.closeness_centrality(B)
    averageCloseness = sum(closenesses.values()) / numberOfNodes

    # Computing average betweeness centrality
    betweenesses = nx.betweenness_centrality(B)
    averageBetweeness = sum(betweenesses.values()) / numberOfNodes

    # Computing average harmonic centrality
    harmonices = nx.harmonic_centrality(B)
    averageHarmonics = sum(harmonices.values()) / numberOfNodes

    # Checking the checkbox again to handle average path length
    if self.Checkbutton1.get()==0:
        # in case of undirected graph nothing to handle
        averagePathLength = nx.average_shortest_path_length(B)
    else:
        # in case of directed graph must check if the graph is strongly connected
        if not nx.is_strongly_connected(B):
            largest = max(nx.strongly_connected_components(B), key=len)
            subgraph = B.subgraph(largest)
            averagePathLength = nx.average_shortest_path_length(subgraph)
        else:
            averagePathLength = nx.average_shortest_path_length

    # Printing out the graph's metrics outputs
    stats_text.insert(tk.END, f"Number of the Nodes: {numberOfNodes}\n")
    stats_text.insert(tk.END, f"Number of the Edges: {numberOfEdges}\n")
    stats_text.insert(tk.END, f"Average Degree: {averageDegree}\n")
    stats_text.insert(tk.END, f"Average Cluster Coefficient: {averageClustering}\n")
    stats_text.insert(tk.END, f"Average Path Length: {averagePathLength}\n")
    stats_text.insert(tk.END, f"Average Degree: {averageDegree}\n")
    stats_text.insert(tk.END, f"Average Closeness Centrality: {averageCloseness}\n")
    stats_text.insert(tk.END, f"Average Betweeness Centrality: {averageBetweeness}\n")
    stats_text.insert(tk.END, f"Average Harmonic Centrality: {averageHarmonics}\n")

    # Computing degree distribution
    degree_count = {}
    for degree in degrees.values():
        if degree not in degree_count:
            degree_count[degree] = 0
        degree_count[degree] += 1
    for degree, frequency in sorted(degree_count.items()):
        stats_text.insert(tk.END, f"Degree: {degree}, Frequency: {frequency}\n")

    # Scrollbar
    scrollbar = tk.Scrollbar(top, command=stats_text.yview)
    stats_text.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")