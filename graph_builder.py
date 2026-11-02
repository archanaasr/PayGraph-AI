import networkx as nx

def build_transaction_graph(df):
    G=nx.DiGraph()
    for row in df.itertuples():
        G.add_node(row.sender_id, kind="account")
        G.add_node(row.receiver_id, kind="merchant" if str(row.receiver_id).startswith("M") else "account")
        if G.has_edge(row.sender_id,row.receiver_id):
            G[row.sender_id][row.receiver_id]["weight"] += 1
            G[row.sender_id][row.receiver_id]["amount"] += float(row.amount)
        else:
            G.add_edge(row.sender_id,row.receiver_id,weight=1,amount=float(row.amount))
    return G

def graph_summary(G):
    return {"nodes":G.number_of_nodes(),"edges":G.number_of_edges(),"components":nx.number_weakly_connected_components(G) if G.is_directed() else nx.number_connected_components(G)}
