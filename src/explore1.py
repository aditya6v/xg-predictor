from statsbombpy import sb

competitions = sb.competitions()
print(competitions[["competition_id", "competition_name", "season_id", "season_name"]].to_string())