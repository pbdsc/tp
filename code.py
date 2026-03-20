import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.GraphUtils import GraphUtils
from sklearn.utils import resample

# 1. Setup Parameters
n_iterations = 100
threshold = 0.70
data = df_pruned.to_numpy()
feature_names = df_pruned.columns.tolist()
n_nodes = len(feature_names)

# Initialize an adjacency matrix to count edge occurrences
# We track directed edges (i -> j)
edge_counts = np.zeros((n_nodes, n_nodes))

print(f"Running {n_iterations} bootstrap iterations...")

# 2. Bootstrap Loop
for i in range(n_iterations):
    # Sample with replacement (Bootstrap)
    sample_data = resample(df_pruned, n_samples=len(df_pruned), replace=True).to_numpy()
    
    # Run PC Algorithm
    # alpha=0.05 is the significance level for independence tests
    cg = pc(sample_data, alpha=0.05, indep_test='fisherz', verbose=False, show_progress=False)
    
    # Extract edges from the General Graph (G)
    # 1: i -> j, -1: i <- j, 2: i <-> j (undirected/bidirected)
    adj = cg.G.graph
    for row in range(n_nodes):
        for col in range(n_nodes):
            if adj[row, col] == 1: # Directed edge row -> col
                edge_counts[row, col] += 1

# 3. Apply Consensus Threshold
# Only keep edges that appeared in > 70% of runs
consensus_adj = (edge_counts / n_iterations) >= threshold

# 4. Create and Draw the Final Consensus DAG
G_final = nx.DiGraph()
G_final.add_nodes_from(feature_names)

for i in range(n_nodes):
    for j in range(n_nodes):
        if consensus_adj[i, j]:
            G_final.add_edge(feature_names[i], feature_names[j], 
                             weight=edge_counts[i, j]/n_iterations)

# 5. Visualization
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G_final, k=0.5)

# Draw nodes
nx.draw_networkx_nodes(G_final, pos, node_size=2500, node_color='lightgreen', alpha=0.9)
# Draw edges with widths based on their "Stability Score"
weights = [G_final[u][v]['weight'] * 5 for u, v in G_final.edges()]
nx.draw_networkx_edges(G_final, pos, width=weights, edge_color='black', 
                       arrowsize=25, connectionstyle='arc3,rad=0.1')
# Draw labels
nx.draw_networkx_labels(G_final, pos, font_size=10, font_weight='bold')

plt.title(f"Consensus Causal DAG (Bootstrap n={n_iterations}, Stability > {int(threshold*100)}%)")
plt.axis('off')
plt.tight_layout()
plt.show()

# Print identifying the direct causes of failure
if 'failure' in G_final:
    parents = list(G_final.predecessors('failure'))
    print(f"\nStable Root Causes identified for 'failure': {parents}")