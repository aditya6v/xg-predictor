from statsbombpy import sb

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

for comp_id, season_id, label in competitions:
    matches = sb.matches(competition_id=comp_id, season_id=season_id)
    print(f"{label}: {len(matches)} matches")