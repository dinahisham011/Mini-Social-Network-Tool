import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
from matplotlib import pyplot as plt
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.community.louvain import louvain_communities
from networkx.algorithms.community.quality import modularity
from networkx.algorithms.cuts import conductance
from sklearn.metrics import normalized_mutual_info_score

# Community.py is to handle community detection & comparison
def community_detection(self):
    # If statement will display an error if the user tried to display the graph without uploading the dataset.
    if self.nodes_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Nodes CSV file first !!!')
        return
    elif self.edges_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Edges CSV file first !!!')
        return

    # The if statement checks is the user has checked the directed graph option.
    if self.Checkbutton1.get() == 0:
        D = nx.Graph()
    else:
        D=nx.DiGraph()

    # For loop to add nodes to draw the graph
    for _, row in self.nodes_df.iterrows():
        D.add_node(row['ID'])

    # For loop to add edges to draw the graph
    for _, row in self.edges_df.iterrows():
        D.add_edge(row['Source'], row['Target'])

    # Method to calculate internal density that takes object graph from networkx and the communities detected
    def compute_internal_edge_density(G, communities):
        densities = []
        # For loop to get numbers of nodes and edges from community subgraph
        for community in communities:
            subgraph = G.subgraph(community)
            num_nodes = subgraph.number_of_nodes()
            num_edges = subgraph.number_of_edges()
            if num_nodes <= 1:
                densities.append(0)  # single node or empty community
            else:
                max_possible_edges = num_nodes * (num_nodes - 1) / 2
                density = num_edges / max_possible_edges
                densities.append(density)
        return sum(densities) / len(densities)  # average over all communities

    # Method to calculate average conductance that takes object graph from networkx and the communities detected
    def compute_average_conductance(G, communities):
        conductances = []
        for community in communities:
            if len(community) == 0 or len(community) == len(G):
                continue  # skip trivial cases
            conduct = conductance(G, community)
            conductances.append(conduct)
        if len(conductances) == 0:
            return 0
        return sum(conductances) / len(conductances)  # average over all communities

    # Opening a new window to show the results
    top = tk.Toplevel(self.root)
    top.title("Community Detection Comparison")
    ttk.Label(top, text="Community Detection Comparison").pack()
    stats_text = tk.Text(top, width=60, height=25)
    stats_text.pack(padx=10, pady=10)

    # Detecting communities using Girvan Newman
    community_girvan = girvan_newman(D)
    best_modularity = -1
    best_communities = None

    # For loop to find the best split and print Number of community detected with the modularity score
    for communities in community_girvan:
        communities_list = [list(c) for c in communities]
        current_modularity = modularity(D, communities_list)
        stats_text.insert(tk.END, f"----------Girvan Newman Evaluation----------\n")
        stats_text.insert(tk.END, f"Number of Communities Detected: {len(communities_list)}\n")
        stats_text.insert(tk.END, f"Modularity Score: {current_modularity}\n")
        print(f"Detected {len(communities_list)} communities - modularity: {current_modularity}")

        if current_modularity > best_modularity:
            best_modularity = current_modularity
            best_communities = communities_list
        else:
            break  # When modularity decrease → stop

    # Making a ground truth classes to compare with detected communities
        # Creating a dictionary mapping each node ID to its class
    id_to_class = dict(zip(self.nodes_df['ID'], self.nodes_df['Label']))
    ground_truth = [id_to_class[node] for node in D.nodes()]

    # Map Detected Communities to Nodes
    node_to_community = {}
        # For loop to assign a unique label "i" to each community and build a dictionary
    for i, community in enumerate(best_communities):
        for node in community:
            node_to_community[node] = i
        #This builds a list of detected community labels in the same order as the nodes in D.nodes()
        # so it can be directly compared to the ground_truth labels.
    detected_labels_girvan = [node_to_community[node] for node in D.nodes()]


    # Compute NMI for Girvan Newman
    nmi_girvan = normalized_mutual_info_score(ground_truth, detected_labels_girvan)

    # Compute Conductance for Girvan Newman
    conductance_girvan = compute_average_conductance(D, best_communities)

    # Compute density for Girvan Newman
    density_girvan = compute_internal_edge_density(D, best_communities)

    # Louvain Community Detection
    communities_louvain = louvain_communities(D, seed=42)
    modularity_louvain = modularity(D, communities_louvain)

    # Map Detected Communities to Nodes
    node_to_community_louvain = {}
    # For loop to assign a unique label "i" to each community and build a dictionary
    for i, community in enumerate(communities_louvain):
        for node in community:
            node_to_community_louvain[node] = i
            # This builds a list of detected community labels in the same order as the nodes in D.nodes()
            # so it can be directly compared to the ground_truth labels.
    detected_labels_louvain = [node_to_community_louvain[node] for node in D.nodes()]

    # Compute NMI for Louvain Algorithm
    nmi_louvain = normalized_mutual_info_score(ground_truth, detected_labels_louvain)

    # Compute Conductance for Louvain Algorithm
    conductance_louvain = compute_average_conductance(D, communities_louvain)

    # Compute Density for Louvain Algorithm
    density_louvain = compute_internal_edge_density(D, communities_louvain)

    # Printing out the community detection outputs
    stats_text.insert(tk.END, f"NMI Score vs Ground Truth: {nmi_girvan:.4f}\n")
    stats_text.insert(tk.END, f"Conductance: {conductance_girvan:.4f}\n")
    stats_text.insert(tk.END, f"Internal Edge Density: {density_girvan:.4f}\n\n\n")
    stats_text.insert(tk.END, f"----------Louvain Algorithm Evaluation----------\n")
    stats_text.insert(tk.END, f"Number of Communities Detected: {len(communities_louvain)}\n")
    stats_text.insert(tk.END, f"Modularity Score: {modularity_louvain}\n")
    stats_text.insert(tk.END, f"NMI Score vs Ground Truth: {nmi_louvain:.4f}\n")
    stats_text.insert(tk.END, f"Conductance: {conductance_louvain:.4f}\n")
    stats_text.insert(tk.END, f"Internal Edge Density: {density_louvain:.4f}\n\n\n")

    # Visualizing Louvain algorithm detected communities
    pos = nx.spring_layout(D, seed=42)
    colors_louvain = [node_to_community_louvain[n] for n in D.nodes()]
    plt.figure(figsize=(8, 6))
    nx.draw(D, pos, node_color=colors_louvain, with_labels=True, cmap=plt.cm.Set2, node_size=200)
    plt.title(f"Louvain Detected Communities\n(Modularity: {modularity_louvain:.4f})")
    plt.show()