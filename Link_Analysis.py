import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx

# Link_Analysis is made to handle link analysis techniques

def linkAnalysis(self):
    # If statement will display an error if the user tried to display the graph without uploading the dataset.
    if self.nodes_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Nodes CSV file first !!!')
        return
    elif self.edges_df is None:
        messagebox.showerror('Graph Error', 'Error: Upload the Edges CSV file first !!!')
        return

    # If statement to make sure that the user checked the Directed Graph checkbox
    if self.Checkbutton1.get() == 0:
        messagebox.showerror('Link Analysis Error', 'Error: Select the Directed Graph Checkbox !!!')
    else:
        # Opening a new window to show pagerank results
        top = tk.Toplevel(self.root)
        top.title("Link Analysis")
        ttk.Label(top, text="PageRank").pack()
        stats_text = tk.Text(top, width=60, height=25)
        stats_text.pack(padx=10, pady=10)

        # Text configration to highlight results
        stats_text.tag_configure('high', foreground='green', font=('TkDefaultFont', 10, 'bold'))
        stats_text.tag_configure('medium', foreground='blue')
        stats_text.tag_configure('low', foreground='gray')

        DG = nx.DiGraph()

        # For loop to add nodes to draw the graph
        for _, row in self.nodes_df.iterrows():
            node_id = row['ID']
            DG.add_node(node_id)

        # For loop to add edges to draw the graph
        for _, row in self.edges_df.iterrows():
            DG.add_edge(row['Source'], row['Target'])

        # Computing pagerank
        DG_pageranke = nx.pagerank(DG)
        sorted_pagerank = sorted(DG_pageranke.items(), key=lambda item: item[1], reverse=True)

        # Headers for PageRank output
        stats_text.insert(tk.END, f"{'Node ID':<15}PageRank Score\n")
        stats_text.insert(tk.END, "-" * 35 + "\n")

        # Applying the text configration and printing pagerank results
        for node_id, score in sorted_pagerank:
            if score >= 0.05:
                tag = 'high'
            elif score >= 0.02:
                tag = 'medium'
            else:
                tag = 'low'
            stats_text.insert(tk.END, f"{node_id:<15}{score:.5f}\n", tag)

        # Opening a second window to show betweeness results
        top2 = tk.Toplevel(self.root)
        top2.title("Link Analysis")
        ttk.Label(top2, text="Betweeness Centrality").pack()
        stats_text2 = tk.Text(top2, width=60, height=25)
        stats_text2.pack(padx=10, pady=10)
        stats_text2.tag_configure('high', foreground='green', font=('TkDefaultFont', 10, 'bold'))
        stats_text2.tag_configure('medium', foreground='blue')
        stats_text2.tag_configure('low', foreground='gray')

        # Computing betweeness centrality
        DG_betweenness = nx.betweenness_centrality(DG, normalized=True)
        sorted_betweenness = sorted(DG_betweenness.items(), key=lambda x: x[1], reverse=True)

        # Headers for Betweeness Centrality
        stats_text2.insert(tk.END, f"{'Node ID':<15}{'Betweenness Centrality'}\n", 'high')
        stats_text2.insert(tk.END, f"{'-' * 40}\n")

        # Applying the text configration and printing betweeness centrality results
        for node_id, score in sorted_betweenness:
            if score >= 0.1:
                tag = 'high'
            elif score >= 0.02:
                tag = 'medium'
            else:
                tag = 'low'
            stats_text2.insert(tk.END, f"{node_id:<15}{score:.5f}\n", tag)