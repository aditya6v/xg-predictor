import pandas as pd
from statsbombpy import sb
from features import calculate_distance, calculate_angle
from features import get_goalkeeper_distance_to_goal, count_defenders_in_path

def get_shots_from_match(match_id):
    events = sb.events(match_id=match_id)
    shots = events[events["type"] == "Shot"]
    return shots

def get_all_shots(competition_id, season_id):
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    all_shots = []
    for match_id in matches["match_id"]:
        shots = get_shots_from_match(match_id)
        all_shots.append(shots)
    return pd.concat(all_shots, ignore_index=True)


# ── List of competitions to pull ──
# Each entry is (competition_id, season_id, label)
competitions = [
    (43, 106, "World Cup 2022"),
    (43, 3,   "World Cup 2018"),
    (11, 4,   "La Liga 2018/2019"),
    (11, 42,  "La Liga 2019/2020"),
    (11, 90,  "La Liga 2020/2021"),
    (11, 1,   "La Liga 2017/2018"),
    (11, 2,   "La Liga 2016/2017"),
    (16, 4,   "Champions League 2018/2019"),
    (16, 1,   "Champions League 2017/2018"),
    (16, 27,  "Champions League 2015/2016"),
]


# ── Pull shots from every competition ──
all_parts = []
for comp_id, season_id, label in competitions:
    print(f"Loading {label}...")
    shots = get_all_shots(comp_id, season_id)
    print(f"  {len(shots)} shots")
    all_parts.append(shots)

all_shots = pd.concat(all_parts, ignore_index=True)

# ── Feature engineering (same as before) ──
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

all_shots["is_goal"] = (all_shots["shot_outcome"] == "Goal").astype(int)

print("\nTotal shots:", len(all_shots))
print(all_shots["is_goal"].value_counts())

all_shots.to_csv("data/shots.csv", index=False)
print("Data saved to data/shots.csv")