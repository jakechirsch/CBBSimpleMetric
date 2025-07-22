##### IMPORTS #####
from bs4 import BeautifulSoup
import requests
import csv
import sys
import time

def get_team_schedule(team_slug, year):
    time.sleep(3.1)
    url = f"https://www.sports-reference.com/cbb/schools/{team_slug}/{year}-schedule.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {"id": "schedule"})
    if not table:
        print(f"No data found for {team_slug.upper()} {year}")
        return []

    games = []
    for row in table.tbody.find_all("tr"):
        if row.get("class") == ["thead"]:
            continue  # skip section headers
        date = row.find("td", {"data-stat": "date_game"}).text.strip()
        game_type = row.find("td", {"data-stat": "game_type"}).text.strip()
        loc = row.find("td", {"data-stat": "game_location"}).text.strip()
        opp = row.find("td", {"data-stat": "opp_name"}).text.strip()
        result = row.find("td", {"data-stat": "game_result"}).text.strip()
        pf = row.find("td", {"data-stat": "pts"}).text.strip()
        pa = row.find("td", {"data-stat": "opp_pts"}).text.strip()
        ot = row.find("td", {"data-stat": "overtimes"}).text.strip()
        game_dict = {"date": date,
                     "game_type": game_type,
                     "location": loc,
                     "opponent": opp,
                     "result": result,
                     "points_for": pf,
                     "points_against": pa,
                     "overtimes": ot}
        games.append(game_dict)
    return games

def point_diff_calculator():
    point_diffs = []
    with open('teams.txt', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            games = get_team_schedule(row['Team'], 2025)
            if not games:
                print(f"No data found for {row['Team']}")
                sys.exit()
            point_diff = 0
            for game in games:
                if game["game_type"] == "REG":
                    point_diff += int(game["points_for"]) - int(game["points_against"])
            point_diffs.append((row['Team'], point_diff))
    point_diffs.sort(key=lambda x: x[1], reverse=True)
    return point_diffs

def point_diff_score():
    diffs = point_diff_calculator()
    for team_pair in diffs:
        print(f"{team_pair[0]}: {team_pair[1]}")
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