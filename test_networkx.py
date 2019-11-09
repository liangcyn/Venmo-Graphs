# visualizes simple temporal wcc subgraphs on networkx 

import networkx as nx
import matplotlib.pyplot as plt
import csv

def find_temporal_graphs_at_time(timestring):
    G = nx.MultiDiGraph()

    ctr = 0
    with open('clean_venmo.csv') as csvfile:
        csv_F = csv.reader(csvfile,delimiter=',')
        for row in csv_F:
            payer = row[0]
            receiver = row[1]
            message = row[2]
            timestamp = row[3]
            if timestamp.startswith(timestring):
                G.add_edge(payer, receiver, message = message, timestamp = timestamp)
            ctr += 1
            if ctr % 1000000 == 0:
                print(ctr)

    print("***********    DONE WITH UPLOADING GRAPH    **************")
    print(timestring)
    print("num nodes:", len(G))
    print("edge number:", G.size())
    print("num wccs:", nx.number_weakly_connected_components(G))
    print("num wccs > 3", len([c for c in list(nx.weakly_connected_component_subgraphs(G)) if len(c) >= 3]))

    # draws wcc subgraphs of more than 3 nodes
    for c in list(nx.weakly_connected_component_subgraphs(G)):

        if len(c) >= 3:
            pos = nx.spring_layout(c)

            # draw nodes
            nx.draw_networkx_nodes(c,pos=pos)
            nx.draw_networkx_edges(c,pos=pos)
            plt.show()

def main():
    for n in range(10):
        # timestring explanation
        # chooses only nodes and edges belonging in a certain time period.
        # for example:
        # 2018-08-07T02 means it only picks transactions from 2AM on August 7, 2018.
        timestring = "2018-08-07T02:%i" %n
        find_temporal_graphs_at_time(timestring)


if __name__ == '__main__':
    main()
