import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

shots = pd.read_csv("data/shots_clean.csv")

X = shots.drop(columns=["is_goal"])
y = shots["is_goal"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training shots:", len(X_train))
print("Testing shots:", len(X_test))

model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)

model.fit(X_train, y_train)

#print("Model trained!")

y_pred = model.predict_proba(X_test)[:, 1]

for i in range(5):
    print(f"Predicted xG: {y_pred[i]:.2f} | Actual outcome: {y_test.iloc[i]}")

from sklearn.metrics import roc_auc_score

auc = roc_auc_score(y_test, y_pred)
print(f"AUC Score: {auc:.3f}")

from sklearn.metrics import brier_score_loss

brier = brier_score_loss(y_test, y_pred)
print(f"Brier Score: {brier:.4f}")

import joblib

joblib.dump(model, "models/xg_model.pkl")
print("Model saved!")