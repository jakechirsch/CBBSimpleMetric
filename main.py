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

# Load all teams' data
with open("data_2025.json", "r") as data_2025:
    teams = json.load(data_2025)
with open("name_to_slug.json", "r") as n_to_s:
    name_to_slug = json.load(n_to_s)
with open("slug_to_name.json", "r") as s_to_n:
    slug_to_name = json.load(s_to_n)

def point_diff_calculator():
    point_diffs = {}
    with open('teams.csv', 'r') as file:
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
                    game_score = int(game["points_for"]) - int(game["points_against"])
                    if game["location"] == "":
                        game_score += 3
                    elif game["location"] == "@":
                        game_score -= 3
                    point_diff += game_score
                    reg_games += 1
            point_diff /= reg_games
            point_diffs[row['Team']] = point_diff
    return point_diffs

def normalize(diffs):
    sorted_diffs = rank_teams(diffs)
    worst = sorted_diffs[len(sorted_diffs) - 1][1]
    best = sorted_diffs[0][1]
    out_of = best - worst
    scores = []
    for team_pair in sorted_diffs:
        scores.append((team_pair[0], 100 * (team_pair[1] - worst) / out_of))
    return scores

def weighted_point_diff_calculator(scores):
    sorted_scores = rank_teams(scores)
    point_diffs = {}
    for tup in sorted_scores:
        games = teams[tup[0]]
        if not games:
            print(f"No data found for {tup[0]}")
            sys.exit()
        point_diff = 0
        reg_games = 0
        for game in games:
            if game["game_type"] == "REG" and game["is_d1_opponent"]:
                diff = int(game["points_for"]) - int(game["points_against"])
                opponent = game["opponent"].split("\xa0", 1)[0]
                game_score = diff + scores[name_to_slug[opponent]]
                if game["location"] == "":
                    game_score += 3
                elif game["location"] == "@":
                    game_score -= 3
                point_diff += game_score
                reg_games += 1
        point_diff /= reg_games
        point_diffs[tup[0]] = point_diff
    return point_diffs

def rank_teams(diffs):
    return sorted(diffs.items(), key=lambda item: item[1], reverse=True)

def test_model(model):
    model_w = 0
    game_count = 0
    for team in teams:
        for t_game in teams[team]:
            if t_game["is_d1_opponent"]:
                game_count += 1
                t_opponent = t_game["opponent"].split("\xa0", 1)[0]
                if t_game["result"] == "W":
                    if model[team] > model[name_to_slug[t_opponent]]:
                        model_w += 1
                else:
                    if model[team] < model[name_to_slug[t_opponent]]:
                        model_w += 1
    print(f"{int(model_w / 2)}/{int(game_count / 2)}: {model_w / game_count}")

def print_ranking(ranking):
    rank = 1
    for team_slug, p_diff in ranking:
        print(f"{rank}. {slug_to_name[team_slug]}: {p_diff}")
        rank += 1

p_diffs = point_diff_calculator()
"""print_ranking(rank_teams(p_diffs))
test_model(p_diffs)"""
weighted = []
for _ in range(10):
    weighted = weighted_point_diff_calculator(p_diffs)
    p_diffs = weighted
weighted_ranking = normalize(weighted)
print_ranking(weighted_ranking)
test_model(p_diffs)