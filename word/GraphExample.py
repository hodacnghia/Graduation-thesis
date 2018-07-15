import numpy as np
from scipy.spatial.distance import squareform
import networkx as nx
import pylab as plt

nb_nodes = 20

distances = squareform(np.random.uniform(
    size=int(nb_nodes * (nb_nodes - 1) / 2)))
distances[np.diag_indices(nb_nodes)] = np.ones(nb_nodes)

complete_graph = nx.Graph()
for i in range(nb_nodes):
    for j in range(i+1, nb_nodes):
        complete_graph.add_edge(i, j, weight=distances[i, j])

t = nx.eigenvector_centrality(complete_graph)
print(t[0],
      "eigenvector_centrality")
nx.draw(complete_graph, with_labels=True)
plt.show()

print(nx.eigenvector_centrality(complete_graph),
      "eigenvector_centrality")
print(nx.closeness_centrality(complete_graph),
      "closeness_centrality")
print(nx.closeness_centrality(complete_graph),
      "closeness_centrality")
print(nx.betweenness_centrality(complete_graph),
      "betweenness_centrality")
print(nx.betweenness_centrality(complete_graph),
      "betweenness_centrality")
print(nx.degree(complete_graph),
      "degree")
print(nx.degree(complete_graph),
      "degree")
print(nx.eccentricity(complete_graph),
      "eccentricity")
print(nx.eccentricity(complete_graph),
      "eccentricity")
