import pandas as pd

FEATURE_COLUMNS = ["amount","frequency_24h","account_age_days","hour","day_of_week","sender_tx_count","receiver_tx_count"]

def prepare_features(df, include_label=False):
    work=df.copy()
    ts=pd.to_datetime(work["timestamp"], errors="coerce", utc=True)
    work["hour"]=ts.dt.hour.fillna(0)
    work["day_of_week"]=ts.dt.dayofweek.fillna(0)
    work["sender_tx_count"]=work.groupby("sender_id")["transaction_id"].transform("count")
    work["receiver_tx_count"]=work.groupby("receiver_id")["transaction_id"].transform("count")
    X=work.reindex(columns=FEATURE_COLUMNS).fillna(0)
    y=work["is_fraud"].astype(int) if include_label and "is_fraud" in work else None
    return (X,y) if include_label else X
