from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("models/xg_model.pkl")

@app.get("/")
def home():
    return {"message": "xG Predictor API is running!"}

@app.get("/predict")
def predict(distance: float, angle: float, body_part: str, 
            shot_type: str, technique: str,
            first_time: int = 0, open_goal: int = 0, 
            pressure: int = 0, gk_distance: float = 2.0,
            defenders: int = 0):
    
    # Penalties always get fixed xG regardless of other features
    if shot_type.lower() == "penalty":
        return {"xG": 0.76, "note": "Penalty — fixed xG"}

@app.get("/predict")
def predict(distance: float, angle: float, body_part: str, 
            shot_type: str, technique: str,
            first_time: int = 0, open_goal: int = 0, 
            pressure: int = 0, gk_distance: float = 2.0,
            defenders: int = 0):
    
    shot = {
        "distance": distance,
        "angle": angle,
        "shot_first_time": first_time,
        "shot_open_goal": open_goal,
        "under_pressure": pressure,
        "shot_body_part_Head": 1 if body_part.lower() == "head" else 0,
        "shot_body_part_Left Foot": 1 if body_part.lower() == "left" else 0,
        "shot_body_part_Right Foot": 1 if body_part.lower() == "right" else 0,
        "shot_type_Corner": 1 if shot_type.lower() == "corner" else 0,
        "shot_type_Free Kick": 1 if shot_type.lower() == "freekick" else 0,
        "shot_type_Open Play": 1 if shot_type.lower() == "openplay" else 0,
        "shot_technique_Normal": 1 if technique.lower() == "normal" else 0,
        "shot_technique_Volley": 1 if technique.lower() == "volley" else 0,
        "shot_technique_Half Volley": 1 if technique.lower() == "halfvolley" else 0,
        "shot_technique_Lob": 1 if technique.lower() == "lob" else 0,
        "gk_distance": gk_distance,
        "defenders_in_path": defenders
    }

    shot_df = pd.DataFrame([shot])
    xg = model.predict_proba(shot_df)[:, 1][0]
    return {"xG": round(float(xg), 3)}