import pandas as pd

shots = pd.read_csv("data/shots.csv")

print("Shots loaded:", len(shots))

columns_to_keep = ["x", "y", "distance", "angle", "shot_body_part", 
                   "shot_type", "shot_technique", "shot_first_time", 
                   "shot_open_goal", "under_pressure", "is_goal",
                   "gk_distance", "defenders_in_path"] 
shots = shots[columns_to_keep]

bool_columns = ["shot_first_time", "shot_open_goal", "under_pressure"]
shots[bool_columns] = shots[bool_columns].fillna(False).astype(int)

# Add y_offset feature
shots["y_offset"] = (shots["y"] - 40).abs()

shots = pd.get_dummies(shots, columns=["shot_body_part", "shot_type", "shot_technique"])

shots = shots[shots["shot_type_Penalty"] == 0]

final_columns = ["distance", "angle", "shot_first_time", "shot_open_goal", 
                 "under_pressure", "shot_body_part_Head", "shot_body_part_Left Foot",
                 "shot_body_part_Right Foot", "shot_type_Corner", "shot_type_Free Kick",
                 "shot_type_Open Play", "shot_technique_Normal", "shot_technique_Volley",
                 "shot_technique_Half Volley", "shot_technique_Lob",
                 "gk_distance", "defenders_in_path", "is_goal"]

# Fill missing goalkeeper distance with average
avg_gk_distance = shots["gk_distance"].mean()
shots["gk_distance"] = shots["gk_distance"].fillna(avg_gk_distance)

shots = shots[final_columns]

print("Final dataset shape:", shots.shape)
print("Goals:", shots["is_goal"].sum())

shots.to_csv("data/shots_clean.csv", index=False)
print("Clean data saved!")