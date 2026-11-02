from sklearn.ensemble import IsolationForest

def train_anomaly_detector(X):
    model=IsolationForest(n_estimators=150,contamination="auto",random_state=42)
    return model.fit(X)

def score_anomalies(model,X):
    return model.predict(X)
