import tkinter as tk
from tkinter import colorchooser, filedialog, ttk, messagebox
import pandas as pd
import Community
import Filter
import Graph_Build
import Link_Analysis
import Metrics
import Node_Metrics

# Layout.py is for making the GUI form by Tkinter
class Layout:

    # Constructor to initialize used variables
    def __init__(self, root):
        self.max_centrality = None
        self.min_centrality = None
        self.centrality_combo = None
        self.edge_size_entry = None
        self.node_size_entry = None
        self.node_selected_color = None
        self.edge_selected_color = None
        self.layout_algorithm_combo = None
        self.node_shape_combo = None
        self.combo = None
        self.root = root
        self.layout_algorithm_option = ["Force-Directed (Fruchterman-Reingold)", "Hierarchical (Tree)",
                                        "Hierarchical (Radial)", "Eigenvector", "Circular", "Shell", "Planar"]
        self.node_shape_markers = ['o', 's', '^', 'D', 'P', 'v']
        self.attrs = []
        self.nodes_df = None
        self.edges_df = None
        self.Checkbutton1 = tk.IntVar()

    #Method that contain the Layout of the GUI while also calling other methods
    def LayoutForm(self):

        # Frames to handle the layout making its components in aligned form
        load_buttons_frame = tk.Frame(self.root)
        load_buttons_frame.pack(padx=10, pady=5)
        node_edge_attributes = tk.Frame(self.root)
        node_edge_attributes.pack(padx=10, pady=5)
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(padx=10, pady=5)
        metrics_frame = tk.Frame(self.root)
        metrics_frame.pack(padx=10, pady=5)
        commuinty_detection_frame = tk.Frame(self.root)
        commuinty_detection_frame.pack(padx=10, pady=5)
        filter_node_frame=tk.Frame(self.root)
        filter_node_frame.pack(padx=10,pady=5)

        # Directed graph checkbutton
        tk.Checkbutton(load_buttons_frame, text="Directed Graph", variable=self.Checkbutton1,
                       onvalue=1, offvalue=0, height=2, width=20, font=("Arial", 12)).pack(side="left", padx=5)

        # Load data csv file buttons
        tk.Button(load_buttons_frame, text="Load Nodes CSV file", command=self.when_load_nodes_button_clicked,
                  font=("Arial", 12), padx=5, pady=5, width=20).pack(side="left", padx=5)
        tk.Button(load_buttons_frame, text="Load Edges CSV file", command=self.when_load_edges_button_clicked,
                  font=("Arial", 12), padx=5, pady=5, width=20).pack(side="left", padx=5)

        # Color selection buttons that opens a color map
        tk.Button(node_edge_attributes, text="Choose Node Color", command=self.node_color,
                  font=("Arial", 12), padx=5, pady=5, width=20).pack(padx=10, pady=5, side="left")
        tk.Button(node_edge_attributes, text="Choose Edge Color", command=self.edge_color,
                  font=("Arial", 12), padx=5, pady=5, width=20).pack(padx=10, pady=5, side="left")

        # Entry textboxes to get the size of nodes and edges
        ttk.Label(node_edge_attributes, text="Node Size :", font=("Times New Roman", 10)).pack(side="left")
            # Setting default value
        var_node_size = tk.DoubleVar(value=150)
        self.node_size_entry = tk.Entry(node_edge_attributes, textvariable=var_node_size, width=20)
        self.node_size_entry.pack(padx=10, pady=5, side="left")
        ttk.Label(node_edge_attributes, text="Edge Size :", font=("Times New Roman", 10)).pack(side="left")
            # Setting default value
        var_edge_size = tk.DoubleVar(value=1)
        self.edge_size_entry = tk.Entry(node_edge_attributes, textvariable=var_edge_size, width=20)
        self.edge_size_entry.pack(padx=10, pady=5, side="left")

        # Node label combo box
        ttk.Label(filter_frame, text="Node Label :", font=("Times New Roman", 10)).pack(side="left")
        self.combo = ttk.Combobox(filter_frame, width=20)
        self.combo.pack(padx=10, pady=5, side="left")

        # Node Shape combo box
        ttk.Label(filter_frame, text="Node Shape :", font=("Times New Roman", 10)).pack(side="left")
        self.node_shape_combo = ttk.Combobox(filter_frame, width=20)
        self.node_shape_combo['values'] = self.node_shape_markers
        self.node_shape_combo.pack(padx=10, pady=5, side="left")
        self.node_shape_combo.set(self.node_shape_markers[0])

        # Layout Algorithm combo box
        ttk.Label(filter_frame, text="Layout Algorithm :", font=("Times New Roman", 10)).pack(side="left")
        self.layout_algorithm_combo = ttk.Combobox(filter_frame, width=20)
        self.layout_algorithm_combo['values'] = self.layout_algorithm_option
        self.layout_algorithm_combo.pack(padx=10, pady=5, side="left")
        self.layout_algorithm_combo.set(self.layout_algorithm_option[0])

        # Draw graph button that executes the Graph
        tk.Button(filter_frame, text="Draw Graph",
                  command=self.on_draw_graph_clicked,
                  font=("Arial", 12), padx=5, pady=5, width=20).pack(padx=10, pady=5, side="right")

        # Entry to get the Node ID chosen to make metrics on
        ttk.Label(metrics_frame, text="Node ID :", font=("Times New Roman", 10)).pack(side="left")
        var_node_id = tk.DoubleVar(value=1457)
        self.node_id_entry = tk.Entry(metrics_frame, textvariable=var_node_id, width=20)
        self.node_id_entry.pack(padx=10, pady=5, side="left")

        # Show specific node's metrics
        tk.Button(metrics_frame, text="Show Node's Metrics", command=self.on_show_node_metrics_clicked,
                  font=("Arial", 12), padx=5, pady=5, width=20).pack(padx=10, pady=5, side='left')

        # Show Graph's metrics
        tk.Button(metrics_frame, text="Show Graph's Metrics", command=self.on_show_metrics_clicked,
                  font=("Arial", 12), padx=5, pady=5, width=20).pack(padx=10, pady=5, side='left')

        # Show Community detection and comparison
        tk.Button(commuinty_detection_frame, text="Community Detection & Comparison", command=self.on_community_detection_clicked,
                  font=("Arial", 12), padx=5, pady=5, width=30).pack(padx=10, pady=5, side="left")

        # Show Link analysis
        tk.Button(commuinty_detection_frame, text="Link Analysis", command=self.on_link_analysis_clicked,
                  font=("Arial", 12), padx=5, pady=5, width=30).pack(padx=10, pady=5, side="left")

        # Centrality measurement combobox
        ttk.Label(filter_node_frame, text="Centrality Type:", font=("Times New Roman", 10)).pack(side="left")
        self.centrality_combo = ttk.Combobox(filter_node_frame, width=20)
        self.centrality_combo['values'] = ["Degree", "Betweenness", "Closeness"]
        self.centrality_combo.pack(padx=10, side="left")
        self.centrality_combo.set("Degree")

        # Min and Max Centrality Value Entry
        ttk.Label(filter_node_frame, text="Min:", font=("Times New Roman", 10)).pack(side="left")
        self.min_centrality = tk.Entry(filter_node_frame, width=20)
        self.min_centrality.pack(side="left", padx=5)
        ttk.Label(filter_node_frame, text="Max:", font=("Times New Roman", 10)).pack(side="left")
        self.max_centrality = tk.Entry(filter_node_frame, width=20)
        self.max_centrality.pack(side="left", padx=5)

        # Apply Filter Button
        tk.Button(filter_node_frame, text="Apply Filter", command=self.on_apply_filter_clicked,
                  font=("Arial", 12), padx=5, pady=5, width=20).pack(padx=10, pady=5, side="left")

        # Note to show Ranges of centrality measures
        text_box=tk.Text(width=50, height=7)
        text_box.insert(tk.END,"Note that:\n")
        text_box.insert(tk.END,"Min Degree Centrality value is : 0.08\n")
        text_box.insert(tk.END,"Max Degree Centrality value is :  0.55\n")
        text_box.insert(tk.END, "Min Betweeness Centrality value is :  0.00\n")
        text_box.insert(tk.END, "Max Betweeness Centrality value is :  0.0132\n")
        text_box.insert(tk.END, "Min Closeness Centrality value is :  0.467\n")
        text_box.insert(tk.END, "Max Closeness Centrality value is :  0.692\n")
        text_box.pack(padx=10,pady=5)

    # Method used to load edges' file from device
    def when_load_edges_button_clicked(self):
        file_path = filedialog.askopenfilename()
        self.edges_df = pd.read_csv(file_path)

    # Method to update node label combox once the nodes' file uploaded
    def update_combo_box(self):
        self.combo['values'] = self.attrs
        if self.attrs:
            self.combo.set(self.attrs[0])

    # Method used to load edges' file from device
    def when_load_nodes_button_clicked(self):
        file_path = filedialog.askopenfilename()
        print("Selected file:", file_path)
        try:
            self.nodes_df = pd.read_csv(file_path)
            # Get the labels of the nodes
            if self.nodes_df is not None:
                self.attrs = list(self.nodes_df.columns)
                self.update_combo_box()
        except Exception as e:
            print("Error loading CSV:", e)
        return self.nodes_df, self.attrs

    # Method to select edge color from color map
    def edge_color(self):
        color = colorchooser.askcolor(title="Choose Edge Color")
        if color[1]:
            self.edge_selected_color = color[1]
            print("Selected edge color:", self.edge_selected_color)

    # Method to select edge color from color map
    def node_color(self):
        color = colorchooser.askcolor(title="Choose Node Color")
        if color[1]:  # If user didn't cancel
            self.node_selected_color = color[1]
            print("Selected node color:", self.node_selected_color)

    # Method to call draw_graph method when Draw Graph button is clicked
    def on_draw_graph_clicked(self):
        Graph_Build.draw_graph(self,
            self.combo,
            self.nodes_df,
            self.edges_df,
            self.node_selected_color,
            self.edge_selected_color,
            self.node_size_entry,
            self.edge_size_entry,
            self.layout_algorithm_combo,
            self.node_shape_combo
        )

    # Method to call show_metrics method when Show Graph's Metrics button is clicked
    def on_show_metrics_clicked(self):
        Metrics.show_metrics(self)

    # Method to call show_node_metrics method when Show Node's Metrics button is clicked
    def on_show_node_metrics_clicked(self):
        Node_Metrics.show_node_metrics(self)

    # Method to call community_detection method when Community Detection & Comparison button is clicked
    def on_community_detection_clicked(self):
        Community.community_detection(self)

    # Method to call link_analysis method when Link Analysis button is clicked
    def on_link_analysis_clicked(self):
        Link_Analysis.linkAnalysis(self)

    # Method to call draw_filtered_graph  method when Apply Filters button is clicked
    def on_apply_filter_clicked(self):
        # Get the Centrality measure used to filter
        centrality_type = self.centrality_combo.get()
        try:
            # Get minimum and maximum numbers for centrality range
            min_val = float(self.min_centrality.get())
            max_val = float(self.max_centrality.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for min and max centrality.")
            return
        Filter.draw_filtered_graph(self,
            self.combo, self.nodes_df, self.edges_df,
            self.node_selected_color, self.edge_selected_color,
            self.node_size_entry, self.edge_size_entry,
            self.layout_algorithm_combo, self.node_shape_combo,
            centrality_type, min_val, max_val
        )