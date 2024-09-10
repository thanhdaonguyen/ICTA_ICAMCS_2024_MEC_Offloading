
from base.Initializer import Initializer
from base.Dijkstra import Dijkstra
from base.Parameters import Parameters, Experiment
from base.Setting import Setting
import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()
params = Parameters()
Parameters.initializeParameter(Experiment.DELAY_REQUIREMENT, (0.001, 0.09), Setting.CT_types_delay_experiment[1], "")
initializer = Initializer()
all_servers, access_servers, level2_servers, level3_servers = initializer.initializeServers()
node_colors = {}
print('haha')

for server in access_servers:
    node_colors[server.name] = (0, 1, 1, 0.5)
    for adj in server.adjacent_servers:
        G.add_edge(server.name, adj[0].name)

for server in level2_servers:
    node_colors[server.name] = (1, 1, 0, 0.5)
    for adj in server.adjacent_servers:
        G.add_edge(server.name, adj[0].name)

for server in level3_servers:
    node_colors[server.name] = (1, 0, 1, 0.5)
    for adj in server.adjacent_servers:
        G.add_edge(server.name, adj[0].name)

graph = Initializer.createAdjacentListGraph(all_servers)

print(Dijkstra(graph, 1, 28))
colors = [node_colors[node] for node in G.nodes()]

# Step 5: Draw the graph
nx.draw(G, with_labels=True, node_color=colors, node_size=500, edge_color='k')

# Display the plot
plt.show()

