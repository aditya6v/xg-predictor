import pandas as pd
from statsbombpy import sb
from features import calculate_distance, calculate_angle

from features import get_goalkeeper_distance_to_goal, count_defenders_in_path

def get_shots_from_match(match_id) :
    events = sb.events(match_id = match_id)

    shots = events[events["type"]=="Shot"]

    return shots 

def get_all_shots(competition_id, season_id):
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    
    all_shots = []

    for match_id in matches["match_id"]:
        shots = get_shots_from_match(match_id)
        all_shots.append(shots)
    
    return pd.concat(all_shots, ignore_index=True)

shots_2022 = get_all_shots(competition_id = 43, season_id = 106)
shots_2018 = get_all_shots(competition_id = 43, season_id = 3)

all_shots = pd.concat([shots_2022, shots_2018], ignore_index=True)

all_shots["x"] = all_shots["location"].apply(lambda loc: loc[0])
all_shots["y"] = all_shots["location"].apply(lambda loc: loc[1])

all_shots["distance"] = all_shots.apply(lambda row: calculate_distance(row["x"], row["y"]), axis=1)
all_shots["angle"] = all_shots.apply(lambda row: calculate_angle(row["x"], row["y"]), axis=1)

all_shots["gk_distance"] = all_shots.apply(
    lambda row: get_goalkeeper_distance_to_goal(row["shot_freeze_frame"]) 
    if isinstance(row["shot_freeze_frame"], list) else None, axis=1)

all_shots["defenders_in_path"] = all_shots.apply(
    lambda row: count_defenders_in_path(row["shot_freeze_frame"], row["x"], row["y"]) 
    if isinstance(row["shot_freeze_frame"], list) else 0, axis=1)

print("Total shots:", len(all_shots))
print(all_shots[["player", "distance", "angle", "shot_outcome"]].head())

all_shots["is_goal"] = (all_shots["shot_outcome"] == "Goal").astype(int)

print(all_shots["is_goal"].value_counts())

all_shots.to_csv("data/shots.csv", index=False)
print("Data saved to data/shots.csv")