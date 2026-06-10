import joblib
import pandas as pd

model = joblib.load("models/xg_model.pkl")


def predict_xg(distance, angle, first_time, open_goal, pressure, 
               body_part, shot_type, technique, gk_distance, defenders):
    
    # Convert inputs to lowercase so capitalisation doesn't matter
    body_part = body_part.lower()
    shot_type = shot_type.lower()
    technique = technique.lower()

    # Penalties get fixed xG - they're always from same spot
    if shot_type.lower() == "penalty":
        return {"xG": 0.76}
    
    shot = {
        "distance": distance,
        "angle": angle,
        "shot_first_time": first_time,
        "shot_open_goal": open_goal,
        "under_pressure": pressure,
        "shot_body_part_Head": 1 if body_part == "head" else 0,
        "shot_body_part_Left Foot": 1 if body_part == "left" else 0,
        "shot_body_part_Right Foot": 1 if body_part == "right" else 0,
        "shot_type_Corner": 1 if shot_type == "corner" else 0,
        "shot_type_Free Kick": 1 if shot_type == "freekick" else 0,
        "shot_type_Open Play": 1 if shot_type == "openplay" else 0,
        "shot_technique_Normal": 1 if technique == "normal" else 0,
        "shot_technique_Volley": 1 if technique == "volley" else 0,
        "shot_technique_Half Volley": 1 if technique == "halfvolley" else 0,
        "shot_technique_Lob": 1 if technique == "lob" else 0,
        "gk_distance": gk_distance,
        "defenders_in_path": defenders
    }
    
    shot_df = pd.DataFrame([shot])
    xg = model.predict_proba(shot_df)[:, 1][0]
    return round(xg, 3)


# Test some shots
# print(predict_xg(6, 55, 0, 0, 0, "right", "openplay", "normal"))
# print(predict_xg(25, 10, 0, 0, 1, "right", "openplay", "normal"))
# print(predict_xg(22, 35, 1, 0, 1, "right", "freekick", "normal"))
# print(predict_xg(28, 15, 1, 0, 0, "right", "openplay", "normal"))
# print(predict_xg(6, 50, 0, 0, 0, "head", "corner", "normal"))

# print(predict_xg(22, 35, 1, 0, 1, "right", "freekick", "normal", 1.5, 4))
# print(predict_xg(6, 55, 0, 0, 0, "right", "openplay", "normal", 2.0, 0))
# print(predict_xg(6, 50, 0, 0, 0, "head", "corner", "normal", 3.0, 1))