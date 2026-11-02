import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
import uuid

def generate_transactions(n=500, seed=42):
    rng = np.random.default_rng(seed)
    users = [f"U{i:03d}" for i in range(1,81)]
    merchants = [f"M{i:03d}" for i in range(1,16)]
    now = datetime.now(timezone.utc)
    rows=[]
    for i in range(n):
        fraud = int(rng.random() < 0.09)
        sender = rng.choice(users)
        receiver = rng.choice(users if fraud and rng.random()<.35 else merchants)
        amount = float(np.round(rng.lognormal(3.0 if not fraud else 4.2, .65),2))
        if fraud and rng.random()<.35: amount *= 5
        ts = now - timedelta(minutes=int(rng.integers(0,60*24*30)))
        rows.append({
            "transaction_id": f"PG-{uuid.uuid4().hex[:12]}",
            "sender_id": sender, "receiver_id": receiver,
            "merchant_id": receiver if str(receiver).startswith("M") else "",
            "amount": amount, "timestamp": ts.isoformat(),
            "frequency_24h": int(rng.integers(1,5) if not fraud else rng.integers(6,30)),
            "account_age_days": int(rng.integers(30,3000) if not fraud else rng.integers(1,180)),
            "category": rng.choice(["retail","food","travel","digital","services"]),
            "payment_status": "COMPLETED", "is_fraud": fraud, "source":"synthetic"
        })
    # Add a small synthetic circular cluster to make graph demonstrations visible.
    for i in range(min(5,n)):
        rows[i]["sender_id"] = f"CLUSTER_{i}"
        rows[i]["receiver_id"] = f"CLUSTER_{(i+1)%5}"
        rows[i]["is_fraud"] = 1
    return pd.DataFrame(rows)
