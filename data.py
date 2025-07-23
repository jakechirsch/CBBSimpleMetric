##### IMPORTS #####
from bs4 import BeautifulSoup
import requests
import sys
import time

def get_team_schedule(team_slug, year):
    time.sleep(4)
    url = f"https://www.sports-reference.com/cbb/schools/{team_slug}/{year}-schedule.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {"id": "schedule"})
    if not table:
        print(f"No data found for {team_slug.upper()} {year}")
        sys.exit()

    games = []
    for row in table.tbody.find_all("tr"):
        if row.get("class") == ["thead"]:
            continue  # skip section headers
        date = row.find("td", {"data-stat": "date_game"}).text.strip()
        game_type = row.find("td", {"data-stat": "game_type"}).text.strip()
        loc = row.find("td", {"data-stat": "game_location"}).text.strip()
        opp_cell = row.find("td", {"data-stat": "opp_name"})
        opp = opp_cell.text.strip()
        is_d1 = opp_cell.find("a") is not None
        result = row.find("td", {"data-stat": "game_result"}).text.strip()
        pf = row.find("td", {"data-stat": "pts"}).text.strip()
        pa = row.find("td", {"data-stat": "opp_pts"}).text.strip()
        ot = row.find("td", {"data-stat": "overtimes"}).text.strip()
        if not pf:
            continue
        game_dict = {"date": date,
                     "game_type": game_type,
                     "location": loc,
                     "opponent": opp,
                     "result": result,
                     "points_for": pf,
                     "points_against": pa,
                     "overtimes": ot,
                     "is_d1_opponent": is_d1}
        games.append(game_dict)
    print(team_slug)
    return games