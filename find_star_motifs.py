# visualizes simple temporal wcc subgraphs on networkx

import networkx as nx
import matplotlib.pyplot as plt
import csv

isomorphs = dict()


def get_timestamps():
    timestamps = set()
    with open('clean_venmo.csv') as csvfile:
        csv_F = csv.reader(csvfile,delimiter=',')
        for row in csv_F:
            timestamp = row[3]
            timestamps.add(timestamp[:14])

    return timestamps

def find_isomorph(c):
    for i in isomorphs:
        if nx.is_isomorphic(c, i):
            return i
    return c

def has_star_motif(c):
<<<<<<< HEAD
    # for node in c:
    #     if len(list(nx.all_neighbors(c, node))) > 2:
    #         pos = nx.spring_layout(c)
=======
    for node in c:
        if len(list(nx.all_neighbors(c, node))) > 2:

            # counts motifs
            motif = find_isomorph(c)
            if motif not in isomorphs:
                isomorphs[motif] = 0
            isomorphs[motif] = 1


            pos = nx.spring_layout(c)
>>>>>>> da538e85ec62ea67ae5570dcfac6a893579fb58b

    #         # draw nodes
    #         nx.draw_networkx_nodes(c,pos=pos)
    #         nx.draw_networkx_edges(c,pos=pos)
    #         messages=nx.get_edge_attributes(c,'message')
    #         print(messages)
    #         nx.draw_networkx_edge_labels(c, pos=pos,edge_labels=messages)

    #         plt.show()

    #         return
    # return 

    d_append = {}

    for n in c:
        in_neighbors = len(list(c.predecessors(n)))
        out_neighbors = len(list(c.successors(n)))

        if in_neighbors + out_neighbors > 2:
            star_tuple = (in_neighbors, out_neighbors)
            if star_tuple not in d_append:
                d_append[star_tuple] = 1
            else:
                d_append[star_tuple] += 1

    return d_append


<<<<<<< HEAD
=======
            return
    return
>>>>>>> da538e85ec62ea67ae5570dcfac6a893579fb58b


def find_temporal_graphs_at_time(timestring):
    G = nx.DiGraph()

    ctr = 0
    with open('clean_venmo.csv') as csvfile:
        csv_F = csv.reader(csvfile,delimiter=',')
        for row in csv_F:
            timestamp = row[3]
            if timestamp.startswith(timestring):
                payer = row[0]
                receiver = row[1]
                message = row[2]
                G.add_edge(payer, receiver, message = message, id = ctr)
            ctr += 1
            if ctr % 1000000 == 0:
                print(ctr)


    print("***********    DONE WITH UPLOADING GRAPH    **************")
    print(timestring)
    print("num nodes:", len(G))
    print("edge number:", G.size())
    print("num wccs:", nx.number_weakly_connected_components(G))

    sig_wccs = [c for c in list(nx.weakly_connected_component_subgraphs(G)) if len(c) >= 3]
    print("num wccs > 3", len(sig_wccs))

    d = {}

    for c in sig_wccs:
<<<<<<< HEAD
        d.update(has_star_motif(c))
        print(d)
=======
        has_star_motif(c)
    print(isomorphs)
>>>>>>> da538e85ec62ea67ae5570dcfac6a893579fb58b


def main():

    timestamps = get_timestamps()

    for timestring in timestamps:
        # timestring explanation
        # chooses only nodes and edges belonging in a certain time period.
        # for example:
        # 2018-08-07T02 means it only picks transactions from 2AM on August 7, 2018.
        find_temporal_graphs_at_time(timestring)


if __name__ == '__main__':
    main()
