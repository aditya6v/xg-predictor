import pandas as pd
from statsbombpy import sb

# Existing free kick analysis
shots = pd.read_csv("data/shots_clean.csv")
freekicks = shots[shots["shot_type_Free Kick"] == 1]
print("Total free kicks:", len(freekicks))
print("Goals from free kicks:", freekicks["is_goal"].sum())
print("Goal rate:", freekicks["is_goal"].mean().round(3))

# New freeze frame exploration
matches_2022 = sb.matches(competition_id=43, season_id=106)
first_match_id = matches_2022.iloc[0]["match_id"]
events = sb.events(match_id=first_match_id)

shots_only = events[events["type"] == "Shot"].copy()
shot = shots_only[shots_only["shot_freeze_frame"].notna()].iloc[0]

print("Player:", shot["player"])
print("Freeze frame:", shot["shot_freeze_frame"])

shots_raw = pd.read_csv("data/shots.csv")
freeze_frame_count = shots_raw["shot_freeze_frame"].notna().sum()
print("Shots with freeze frame data:", freeze_frame_count)
print("Total shots:", len(shots_raw))

from features import get_goalkeeper_position

# Use the freeze frame we already pulled
freeze_frame = shot["shot_freeze_frame"]

gk_x, gk_y = get_goalkeeper_position(freeze_frame)
print("Goalkeeper position:", gk_x, gk_y)

from features import get_goalkeeper_distance_to_goal

gk_dist = get_goalkeeper_distance_to_goal(freeze_frame)
print("Goalkeeper distance to goal centre:", gk_dist)

from features import count_defenders_in_path

shot_x = shot["location"][0]
shot_y = shot["location"][1]

defenders = count_defenders_in_path(freeze_frame, shot_x, shot_y)
print("Defenders in path:", defenders)

import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 8))

# Draw pitch
ax.set_facecolor("green")
ax.plot([0, 0, 120, 120, 0], [0, 80, 80, 0, 0], 'white', linewidth=2)

# Halfway line
ax.plot([60, 60], [0, 80], 'white', linewidth=2)

# Penalty boxes
# Penalty boxes
ax.plot([102, 120], [18, 18], 'white', linewidth=2)
ax.plot([102, 102], [18, 62], 'white', linewidth=2)
ax.plot([102, 120], [62, 62], 'white', linewidth=2)

ax.plot([0, 18], [18, 18], 'white', linewidth=2)
ax.plot([18, 18], [18, 62], 'white', linewidth=2)
ax.plot([0, 18], [62, 62], 'white', linewidth=2)


# Goals
ax.plot([120, 120], [36.34, 43.66], 'yellow', linewidth=6, label="Goal")
ax.plot([0, 0], [36.34, 43.66], 'yellow', linewidth=6)

# Shot location
ax.plot(shot_x, shot_y, 'ro', markersize=12, label="Shot")

# Players
for player in freeze_frame:
    x = player["location"][0]
    y = player["location"][1]
    if player["teammate"] == True:
        ax.plot(x, y, 'bs', markersize=8)
    else:
        ax.plot(x, y, 'rs', markersize=8)

ax.set_xlim(0, 125)
ax.set_ylim(0, 80)
ax.set_xlabel("Pitch length")
ax.set_ylabel("Pitch width")
ax.set_title("Shot freeze frame")
ax.legend()

print("Shot outcome:", shot["shot_outcome"])
print("StatsBomb xG:", shot["shot_statsbomb_xg"])
print("Shot location:", shot["location"])



plt.show()