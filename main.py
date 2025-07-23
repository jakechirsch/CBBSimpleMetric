##### IMPORTS #####
import csv
import json
from data import *

"""
# Save
with open("data_2025.json", "w") as f:
    json.dump(games, f, indent=2)

# Load
with open("data_2025.json", "r") as f:
    games = json.load(f)
"""

def point_diff_calculator():
    point_diffs = []
    with open("data_2025.json", "r") as f:
        teams = json.load(f)
    with open('teams.txt', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            games = teams[row['Team']]
            if not games:
                print(f"No data found for {row['Team']}")
                sys.exit()
            point_diff = 0
            reg_games = 0
            for game in games:
                if game["game_type"] == "REG" and game["is_d1_opponent"]:
                    point_diff += int(game["points_for"]) - int(game["points_against"])
                    reg_games += 1
            point_diff /= reg_games
            point_diffs.append((row['Team'], point_diff))
    point_diffs.sort(key=lambda x: x[1], reverse=True)
    return point_diffs

def point_diff_score():
    diffs = point_diff_calculator()
    worst = diffs[len(diffs) - 1][1]
    best = diffs[0][1]
    out_of = best - worst
    scores = []
    for team_pair in diffs:
        scores.append((team_pair[0], 100 * (team_pair[1] - worst) / out_of))
    return scores

ranking = point_diff_score()
for team in ranking:
    print(f"{team[0]}: {team[1]}")