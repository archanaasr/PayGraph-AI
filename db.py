import sqlite3
from pathlib import Path
import pandas as pd
DB_PATH = Path(__file__).resolve().parents[1] / "paygraph.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    with get_connection() as conn:
        conn.executescript(schema)

def save_transactions(df):
    if df.empty: return
    cols = ["transaction_id","sender_id","receiver_id","merchant_id","amount","timestamp","frequency_24h","account_age_days","category","payment_status","is_fraud","source"]
    data = df.reindex(columns=cols).copy()
    data.to_sql("transactions", get_connection(), if_exists="append", index=False)

def load_transactions():
    init_db()
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM transactions ORDER BY timestamp DESC", conn)
