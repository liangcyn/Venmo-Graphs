# simple script manipulating and visualizing a mid-sized weakly connected component.
import snap
import networkx as nx
import matplotlib.pyplot as plt
import csv


G = snap.LoadEdgeList(snap.PNEANet, "clean_venmo.csv", 0, 1, ',')

# add edge attributes
with open("clean_venmo.csv", encoding='utf-8') as csv_file:
	reader = csv.reader(csv_file, delimiter=",")
	for row in reader:
		payer = int(row[0])
		payee = int(row[1])
		message = row[2]
		timestamp = row[3]
		eid = G.GetEId(payer, payee)
		G.AddStrAttrDatE(eid, message, "Message")
		G.AddStrAttrDatE(eid, timestamp, "Timestamp")

# get weakly connected components
Components = snap.TCnComV()
snap.GetWccs(G, Components)
ctr = 0
wcc_sizes = []

# get the sizes of the weakly connected components
for CnCom in Components:
	wcc_sizes.append(CnCom.Len())
	ctr += 1

CnCom = snap.TIntV()

i = -1

# get a mid-sized
for node in G.Nodes():
	i = node.GetId()
	print(i)
	snap.GetNodeWcc(G, i, CnCom)
	print("CnCom.Len() = %d" % (CnCom.Len()))
	if CnCom.Len() < 10 and CnCom.Len() > 5:
		break

G_CnCom = snap.TIntV()
snap.GetNodeWcc(G, i, G_CnCom)

print("total components", ctr)
print("avg component size,", sum(wcc_sizes)/len(wcc_sizes))

# convert snap.py WCC to NetworkX subgraph for easier visualization tools.
nxG = nx.DiGraph()

ctr = 0

sub_g = snap.GetSubGraph(G, G_CnCom)

for edge in sub_g.Edges():
	payer = edge.GetSrcNId()
	payee = edge.GetDstNId()

	# print edge attributes
	eid = G.GetEId(payer, payee)
	message = G.GetStrAttrDatE(eid, "Message")
	timestamp = G.GetStrAttrDatE(eid, "Timestamp")
	print("edge %d (%d,%d), message %s, timestamp %s" % (eid, payer, payee, message, timestamp))

	if nxG.has_edge(payer, payee):
		nxG[payer][payee]['weight'] += 1
	else:
		nxG.add_edge(payer, payee, weight = 1)

print(ctr)
print("done adding edges")

fig= plt.figure(figsize=(24,36))

elarge = [(u, v) for (u, v, d) in nxG.edges(data=True) if d['weight'] > 1]
esmall = [(u, v) for (u, v, d) in nxG.edges(data=True) if d['weight'] <= 1]

pos = nx.spring_layout(nxG)

# draw nodes
nx.draw_networkx_nodes(nxG, pos, node_size=30)

# draw edges with varying weights
nx.draw_networkx_edges(nxG, pos, edgelist=elarge,
                       width=5)
nx.draw_networkx_edges(nxG, pos, edgelist=esmall,
                       width=2, alpha=0.5)
labels = nx.get_edge_attributes(nxG,'weight')
nx.draw_networkx_edge_labels(nxG,pos,edge_labels=labels)
fig.savefig('graph.png')
