import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import init_db, save_transactions, load_transactions
from utils.synthetic_generator import generate_transactions
from utils.preprocessing import prepare_features
from models.anomaly_detector import train_anomaly_detector, score_anomalies
from models.fraud_classifier import train_classifier, score_transactions
from graph.graph_builder import build_transaction_graph, graph_summary
from ai.investigation_assistant import investigate
from config.settings import get_settings

st.set_page_config(page_title="PayGraph AI", page_icon="🛡️", layout="wide")
st.markdown("""<style>
.stApp {background:#0b1020;color:#edf2ff}
[data-testid="stMetric"] {background:#151d33;padding:16px;border-radius:12px;border:1px solid #283653}
section[data-testid="stSidebar"] {background:#111a2d}
</style>""", unsafe_allow_html=True)

init_db()
st.sidebar.title("🛡️ PayGraph AI")
page = st.sidebar.radio("Navigate", ["Overview", "Transactions", "Fraud Network", "ML Analytics", "AI Investigation", "PayPal Sandbox"])
st.sidebar.caption("Graph-based payment risk intelligence")

if "df" not in st.session_state:
    st.session_state.df = load_transactions()

def refresh_data():
    st.session_state.df = load_transactions()

if page == "Overview":
    st.title("PayGraph AI")
    st.caption("Connecting the dots. Predicting fraud. Securing every payment.")
    if st.button("Generate demo transactions"):
        df = generate_transactions(600, seed=42)
        save_transactions(df)
        refresh_data()
        st.success("Synthetic demo transactions generated and saved.")
    df = st.session_state.df
    if df.empty:
        st.info("Generate demo transactions to explore the dashboard.")
    else:
        if "risk_score" not in df:
            df = score_transactions(df)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Transactions", f"{len(df):,}")
        c2.metric("Payment volume", f"${df.amount.sum():,.2f}")
        c3.metric("High-risk", int((df.risk_score >= .7).sum()))
        c4.metric("Labelled fraud (demo)", int(df.get("is_fraud", pd.Series(dtype=int)).sum()))
        fig = px.histogram(df, x="risk_score", nbins=20, title="Transaction risk score distribution")
        st.plotly_chart(fig, use_container_width=True)
        daily = df.assign(date=pd.to_datetime(df.timestamp).dt.date).groupby("date").amount.sum().reset_index()
        st.plotly_chart(px.line(daily, x="date", y="amount", title="Payment volume over time"), use_container_width=True)

elif page == "Transactions":
    st.title("Transaction Monitoring")
    df = st.session_state.df
    if df.empty:
        st.info("Generate demo transactions on Overview first.")
    else:
        if "risk_score" not in df:
            df = score_transactions(df)
        risk = st.selectbox("Risk filter", ["All", "Low", "Medium", "High"])
        if risk != "All":
            bounds = {"Low": (0,.4), "Medium": (.4,.7), "High": (.7,1.01)}[risk]
            df = df[(df.risk_score >= bounds[0]) & (df.risk_score < bounds[1])]
        st.dataframe(df.sort_values("risk_score", ascending=False), use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), "paygraph_transactions.csv", "text/csv")

elif page == "Fraud Network":
    st.title("Fraud Network Explorer")
    df = st.session_state.df
    if df.empty:
        st.info("Generate demo transactions first.")
    else:
        G = build_transaction_graph(df)
        summary = graph_summary(G)
        a,b,c = st.columns(3)
        a.metric("Nodes", summary["nodes"]); b.metric("Payment links", summary["edges"]); c.metric("Components", summary["components"])
        import networkx as nx
        pos = nx.spring_layout(G, seed=7)
        edge_x, edge_y = [], []
        for u,v in G.edges():
            edge_x += [pos[u][0],pos[v][0],None]; edge_y += [pos[u][1],pos[v][1],None]
        node_x=[pos[n][0] for n in G.nodes()]; node_y=[pos[n][1] for n in G.nodes()]
        fig = px.scatter(x=node_x, y=node_y, title="Account relationship graph")
        fig.update_traces(marker=dict(size=10, color="#8b5cf6"))
        fig.add_scatter(x=edge_x,y=edge_y,mode="lines",line=dict(width=1,color="#64748b"),hoverinfo="skip")
        fig.update_layout(showlegend=False, xaxis_visible=False, yaxis_visible=False)
        st.plotly_chart(fig,use_container_width=True)
        st.caption("Graph is a relationship exploration view. Synthetic fraud labels are for demonstration only.")

elif page == "ML Analytics":
    st.title("Machine Learning Analytics")
    df = st.session_state.df
    if df.empty:
        st.info("Generate demo transactions first.")
    else:
        X, y = prepare_features(df, include_label=True)
        model, metrics = train_classifier(X, y)
        st.json(metrics)
        anom = train_anomaly_detector(X)
        scored = score_anomalies(anom, X)
        st.metric("Anomalies flagged", int((scored < 0).sum()))
        st.write("Feature columns:", list(X.columns))

elif page == "AI Investigation":
    st.title("AI Investigation Assistant")
    df = st.session_state.df
    if df.empty:
        st.info("Generate demo transactions first.")
    else:
        txid = st.selectbox("Select transaction", df.transaction_id.tolist())
        row = df[df.transaction_id == txid].iloc[0].to_dict()
        question = st.text_area("Investigation question", "Explain the risk indicators and suggest next review steps.")
        if st.button("Generate investigation summary"):
            st.markdown(investigate(row, question))

elif page == "PayPal Sandbox":
    st.title("PayPal Sandbox Integration")
    st.warning("Sandbox only. Configure credentials in your .env file. Never enter live credentials into this demo.")
    st.write("This demo can create a PayPal Sandbox order through the backend API.")
    amount = st.number_input("Order amount (USD)", min_value=1.0, value=10.0, step=1.0)
    if st.button("Create Sandbox Order"):
        try:
            from paypal.orders import create_order
            result = create_order(amount)
            st.json(result)
        except Exception as e:
            st.error(str(e))
    st.caption("Payment/order data from PayPal is not automatically labelled as fraudulent.")
