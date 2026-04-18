from fastapi import FastAPI
from pydantic import BaseModel
import pickle, numpy as np

app = FastAPI(title="Fraud Detection API")
model = pickle.load(open('fraud_model.pkl', 'rb'))

class Transaction(BaseModel):
    amount: float
    hour: int
    is_electronics: int
    tx_per_day: int

# TWÓJ KOD
# Endpoint POST /score
# Przyjmij Transaction, zwróć: {"is_fraud": bool, "fraud_probability": float}

@app.post("/score")
def score(tx: Transaction):
    data = np.array([[tx.amount, tx.hour, tx.is_electronics, tx.tx_per_day]])
    
    prob = model.predict_proba(data)[0][1]
    pred = model.predict(data)[0]
    
    return {
        "is_fraud": bool(pred),
        "fraud_probability": float(prob)
    }
    
@app.get("/health")
def health():
    return {"status": "ok"}
