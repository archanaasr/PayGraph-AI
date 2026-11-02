from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, accuracy_score
import pandas as pd
from utils.preprocessing import prepare_features

def train_classifier(X, y):
    if len(X)<10 or y.nunique()<2:
        model=RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
        model.fit(X,y)
        return model, {"note":"Insufficient class diversity for holdout evaluation; fitted on available rows."}
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    model=RandomForestClassifier(n_estimators=200,max_depth=10,class_weight="balanced",random_state=42)
    model.fit(Xtr,ytr)
    pred=model.predict(Xte)
    prob=model.predict_proba(Xte)[:,1]
    metrics={"accuracy":round(accuracy_score(yte,pred),4),"precision":round(precision_score(yte,pred,zero_division=0),4),
             "recall":round(recall_score(yte,pred,zero_division=0),4),"f1":round(f1_score(yte,pred,zero_division=0),4)}
    if yte.nunique()>1: metrics["roc_auc"]=round(roc_auc_score(yte,prob),4)
    return model,metrics

def score_transactions(df):
    X=prepare_features(df)
    model,_=train_classifier(*prepare_features(df,include_label=True))
    out=df.copy()
    out["risk_score"]=model.predict_proba(X)[:,1]
    return out
