from utils.synthetic_generator import generate_transactions
from utils.preprocessing import prepare_features
from graph.graph_builder import build_transaction_graph, graph_summary

def test_generator_and_features():
    df=generate_transactions(50)
    assert len(df)==50
    X,y=prepare_features(df,include_label=True)
    assert len(X)==50 and len(y)==50

def test_graph():
    df=generate_transactions(30)
    G=build_transaction_graph(df)
    s=graph_summary(G)
    assert s["nodes"]>0 and s["edges"]>0
