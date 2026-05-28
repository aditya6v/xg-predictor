from statsbombpy import sb

competitions = sb.competitions()

world_cup = competitions[competitions["competition_name"]=="FIFA World Cup"]

print(world_cup[["competition_id", "season_id", "season_name"]])


matches_2022 = sb.matches(competition_id = 43, season_id = 106)
matches_2018 = sb.matches(competition_id=43, season_id=3)

print("2022 matches:", len(matches_2022))
print("2018 matches:", len(matches_2018))

first_match_id = matches_2022.iloc[0]["match_id"]
events = sb.events(match_id=first_match_id)
print(events["type"].unique())

shots = events[events["type"] == "Shot"]
print(shots.columns.tolist())

key_columns = ["player", "minute", "location", "shot_body_part", 
               "shot_type", "shot_outcome", "shot_statsbomb_xg", 
               "under_pressure"]

print(shots[key_columns].head())
