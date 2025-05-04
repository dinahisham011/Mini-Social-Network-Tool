# Mini-Social-Network-Tool:
An interactive desktop application for analyzing and visualizing social network graphs:
  - Define and customize node and edge attributes (size, color, shape, labels)
  - Visualize networks with various layout algorithms (force-directed, hierarchical)
  - Calculate and analyze key graph metrics (degree, clustering coefficient, average path length, etc.)
  - Filter nodes based on centrality measures
  - Apply and compare multiple community detection algorithms (Louvain, Girvan-Newman)
  - Evaluate clustering using internal and external validation methods
  - Perform link analysis using algorithms like PageRank and Betweenness Centrality
  - Work with both directed and undirected graphs loaded from CSV files
Built with Python (NetworkX, Matplotlib, Tkinter) for researchers and data analysts exploring complex network data.

# Demo:

![Demo](https://github.com/dinahisham011/Mini-Social-Network-Tool/raw/main/assets/Demo.gif)

# Features:
  - Custom node/edge attributes (size, color, label, shape)
  - Multiple layout algorithms (force-directed, radial, etc.)
  - Graph metrics: degree, clustering, path length, etc.
  - Node filtering by centrality and community
  - Community detection: Louvain, Girvan-Newman
  - Side-by-side comparison of community detection results
  - Community evaluation metrics (internal and external)
  - Link analysis: PageRank, Betweenness Centrality
  - Support for directed and undirected graphs
  - Load data from CSV files (nodes + edges)
# Technologies Used:
  - Python
  - Tkinter
  - Networkx
# Poject Structure:
  ```
Mini-Social-Network-Analysis-Tool/
│
├── Dataset/          # Folder for input CSV files (nodes.csv, edges.csv)
│ ├── nodes.csv
│ └── edges.csv
│
├── main.py            # Entry point that runs the application
├── Layout.py          # Contains the Tkinter GUI layout code
├── community.py       # Community detection algorithms (Louvain, Girvan-Newman)
├── Filter.py          # Filtering logic for nodes based on centrality
├── Node_Metrics.py    # Calculates node-level metrics (degree, clustering, etc.)
├── Graph_Build.py     # Builds and processes the network graph from CSV files
├── Link_Analysis.py   # PageRank and Betweenness link analysis methods
├── Metrics.py         # General graph-level metrics and statistics
│
├── README.md          # Project overview and instructions
└── requirements.txt   # Python dependencies

```

# How to use:
  1- Clone the repository:
  ```
  git clone https://github.com/yourusername/social-network-analysis-tool.git
  cd social-network-analysis-tool
  ```
  2- Install dependencies:
  ```
pip install -r requirements.txt
```
  3- Run the application:
```
python src/main.py
```
4- Upload your ```nodes.csv``` and ```edges.csv``` to start analyzing.

# Future Improvements:
  - Export graphs as images or JSON
  - Applying more community detection algorithm
  - Adding more customization options
  - Applying more Filtering option
  - Implement weights to the analysing features

# Input File Format:
  - nodes.csv should contain:
    ``` id, Label(any attributes more or less)```
  - edges.csv should contain:
    ``` source, target```

# Notes to consider before running the Tool:
  - The ```Note That:``` section in the GUI is specific for the primaryschool data only which is provided in Dataset folder
  - To run Community Detection method without errors make sure that line 92 in ```Community.py``` file is modified to suite your ```nodes.csv``` data
  ```
id_to_class = dict(zip(self.nodes_df['ID'], self.nodes_df['Label']))
```
Label must be any attribute from ```nodes.csv``` other tha ID
