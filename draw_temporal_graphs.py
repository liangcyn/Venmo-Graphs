# visualizes simple temporal wcc subgraphs on networkx 

import networkx as nx
import matplotlib.pyplot as plt
import csv

G = nx.MultiDiGraph()

ctr = 0
with open('clean_venmo.csv') as csvfile:
    csv_F = csv.reader(csvfile,delimiter=',')
    for row in csv_F:
        payer = row[0]
        receiver = row[1]
        message = row[2]
        timestamp = row[3]
        if timestamp.startswith("2018-08-07T02"):
            G.add_edge(payer, receiver, message = message, timestamp = timestamp)
        ctr += 1
        if ctr % 1000 == 0:
            print(ctr)

print("***********    DONE WITH UPLOADING GRAPH    **************")
print("num nodes:", len(G))
print("edge number:", G.size())
print("num wccs:", nx.number_weakly_connected_components(G))

# draws wcc subgraphs of more than 3 nodes
for c in list(nx.weakly_connected_component_subgraphs(G)):

    if len(c) >= 3:
        pos = nx.spring_layout(c)

        # draw nodes
        nx.draw_networkx_nodes(c,pos=pos)
        nx.draw_networkx_edges(c,pos=pos)
        plt.show()

