import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import ast
from apscheduler.schedulers.background import BackgroundScheduler

# Find team names
def find_teams(soup):
    scorebox = soup.find("div", class_="scorebox").find_all("strong")
    count = 0

    if (len(scorebox) != 2):
      raise Exception ("Find Team Error: Can't find tag in soup")
    
    for s in scorebox:
        if (s.find("a", href = re.compile("/en/squads/"))):
            count+=1

            if count==1:
                home_team = s.find("a", href = re.compile("/en/squads/")).text
            if count==2:
                away_team = s.find("a", href = re.compile("/en/squads/")).text
    
    return home_team, away_team


# Find scores for each team
def find_score(soup):
    scorebox = soup.find_all("div", class_="scores")

    if (len(scorebox) != 2):
      raise Exception ("Find Score Error: Can't find tag in soup")

    home_team_score = scorebox[0].find("div", class_="score").text
    away_team_score = scorebox[1].find("div", class_="score").text
    return home_team_score, away_team_score

# Find home and away lineups
def find_lineup(soup):
    field_wrap = soup.find("div", id="field_wrap")
    lineup = field_wrap.find_all("div", class_="lineup")

    if (len(lineup) != 2):
      raise Exception ("Find Lineup Error: Can't find tag in soup")

    home_lineup = lineup[0].find_all("tr")
    away_lineup = lineup[1].find_all("tr")
    
    home_starting_lineup = []
    home_bench_lineup = []

    for row in home_lineup:
        if ((row.find("a") and len(home_starting_lineup)<11)):
            home_starting_lineup.append(row.find("a").text)
        elif ((row.find("a") and len(home_starting_lineup)>=11)):
            home_bench_lineup.append(row.find("a").text)
    
    away_starting_lineup = []
    away_bench_lineup = []

    for row in away_lineup:
        if ((row.find("a") and len(away_starting_lineup)<11)):
            away_starting_lineup.append(row.find("a").text)
        elif ((row.find("a") and len(away_starting_lineup)>=11)):
            away_bench_lineup.append(row.find("a").text)
    
    return home_starting_lineup, home_bench_lineup, away_starting_lineup, away_bench_lineup

# Find goal, substituion and red card timings
# Substitutions: Array of "sub-timing", "sub-out-player", "sub-in-player"
def find_event_timings(soup):
    events_wrap = soup.find("div", id="events_wrap")
    home_team_events = events_wrap.find_all("div", class_="event a")
    away_team_events = events_wrap.find_all("div", class_="event b")
    
    home_team_goal_timings = []
    away_team_goal_timings = []
    home_team_sub_timings = []
    away_team_sub_timings = []
    home_team_red_card_timings = []
    away_team_red_card_timings = []
    
  # Home Team
    for event in home_team_events:
      # Goals
        if (event.find("div", class_="event_icon goal") or event.find("div", class_="event_icon penalty_goal")):
            text = event.find_all("div")[0].text
            text = re.findall('[0-9]+', text)[0]
            home_team_goal_timings.append(int(text))
      # Substitutes
        elif (event.find("div", class_="event_icon substitute_in")):
            sub_timing = event.find_all("div")[0].text
            sub_timing = int(re.findall('[0-9]+', sub_timing)[0])
            sub_players = event.find_all("a", href = True)
            # Only sub out
            if (len(sub_players) == 1):
              sub_in_player = "-"
              sub_out_player = sub_players[0].text
              home_team_sub_timings.append([sub_timing, sub_out_player, sub_in_player])
            # Sub out and sub in
            elif (len(sub_players) == 2):
              sub_in_player = sub_players[0].text
              sub_out_player = sub_players[1].text
              home_team_sub_timings.append([sub_timing, sub_out_player, sub_in_player])
            else:
              raise Exception("Substitutes: Invalid number of players")
      # Red Card
        elif (event.find("div", class_="event_icon yellow_red_card")):
            timing = event.find_all("div")[0].text
            timing = int(re.findall('[0-9]+', timing)[0])
            player = event.find_all("a", href = True)
            if (len(player) == 1):
              player = player[0].text
              home_team_red_card_timings.append([timing, player])
            elif (len(player) > 1):
              raise Exception("Red Card: Invalid number of players")

  # Away Team
    for event in away_team_events:
      # Goals
        if (event.find("div", class_="event_icon goal") or event.find("div", class_="event_icon penalty_goal")):
            text = event.find_all("div")[0].text
            text = re.findall('[0-9]+', text)[0]
            away_team_goal_timings.append(int(text))
      # Substitutes
        elif (event.find("div", class_="event_icon substitute_in")):
            sub_timing = event.find_all("div")[0].text
            sub_timing = int(re.findall('[0-9]+', sub_timing)[0])
            sub_players = event.find_all("a", href = True)
            # Only sub out
            if (len(sub_players) == 1):
              sub_in_player = "-"
              sub_out_player = sub_players[0].text
              away_team_sub_timings.append([sub_timing, sub_out_player, sub_in_player])
            # Sub out and sub in
            elif (len(sub_players) == 2):
              sub_in_player = sub_players[0].text
              sub_out_player = sub_players[1].text
              away_team_sub_timings.append([sub_timing, sub_out_player, sub_in_player])
            else:
              raise Exception("Substitutes: Invalid number of players")
      # Red Card
        elif (event.find("div", class_="event_icon yellow_red_card") or event.find("div", class_="event_icon red_card")):
            timing = event.find_all("div")[0].text
            timing = int(re.findall('[0-9]+', timing)[0])
            player = event.find_all("a", href = True)
            if (len(player) == 1):
              player = player[0].text
              away_team_red_card_timings.append([timing, player])
            elif (len(player) > 1):
              raise Exception("Red Card: Invalid number of players")
    
    return home_team_goal_timings, away_team_goal_timings, home_team_sub_timings, away_team_sub_timings, home_team_red_card_timings, away_team_red_card_timings

# Find match data
def find_match_data(url, df):
    data = requests.get(url)
    soup = BeautifulSoup(data.content, "html.parser")
    home_team, away_team = find_teams(soup)
    home_team_score, away_team_score = find_score(soup)
    home_starting_lineup, home_bench_lineup, away_starting_lineup, away_bench_lineup = find_lineup(soup)
    home_team_goal_timings, away_team_goal_timings, home_team_sub_timings, away_team_sub_timings, home_team_red_card_timings, away_team_red_card_timings = find_event_timings(soup)

    df = df.append({
        "Season": "test",
        "Home Team": home_team,
        "Away Team": away_team,
        "Home Team Score": home_team_score,
        "Away Team Score": away_team_score,
        "Home Starting Lineup": home_starting_lineup,
        "Home Bench Lineup": home_bench_lineup,
        "Away Starting Lineup": away_starting_lineup,
        "Away Bench Lineup": away_bench_lineup,
        "Home Goal Timings": home_team_goal_timings,
        "Away Goal Timings": away_team_goal_timings,
        "Home Sub Timings": home_team_sub_timings,
        "Away Sub Timings": away_team_sub_timings,
        "Home Red Card Timings": home_team_red_card_timings,
        "Away Red Card Timings": away_team_red_card_timings
    }, ignore_index = True)

    return df

# Write match data
def write_match_data(source_file_path, dest_file_path, max_count, scheduler):
    print("Start of Function")
    df = pd.DataFrame(columns=["Season", "Home Team", "Away Team", "Home Team Score", "Away Team Score", "Home Starting Lineup", 
                               "Home Bench Lineup", "Away Starting Lineup", "Away Bench Lineup", "Home Goal Timings", 
                               "Away Goal Timings", "Home Sub Timings", "Away Sub Timings", "Home Red Card Timings",
                               "Away Red Card Timings"])
    
    source_df = pd.read_csv(source_file_path)
    season = source_df.at[0, 'Season']
    match_urls = ast.literal_eval(source_df.at[0, 'Match URL'])
    print("Season:", season)
    print("Original Length:", len(match_urls))

    # Shutdown scheduler
    if season == None:
        scheduler.shutdown()

    count = 0
    while (len(match_urls) > 0):        
        count+=1
        if count > max_count:
            break
        popped_url = match_urls.pop(0)
        print(popped_url)
        data = requests.get(popped_url)
        soup = BeautifulSoup(data.content, "html.parser")
        print("soup:", soup)
        home_team, away_team = find_teams(soup)
        home_team_score, away_team_score = find_score(soup)
        home_starting_lineup, home_bench_lineup, away_starting_lineup, away_bench_lineup = find_lineup(soup)
        home_team_goal_timings, away_team_goal_timings, home_team_sub_timings, away_team_sub_timings, home_team_red_card_timings, away_team_red_card_timings = find_event_timings(soup)

        df = pd.concat([df, pd.DataFrame({
          "Season": [season],
          "Home Team": [home_team],
          "Away Team": [away_team],
          "Home Team Score": [home_team_score],
          "Away Team Score": [away_team_score],
          "Home Starting Lineup": [home_starting_lineup],
          "Home Bench Lineup": [home_bench_lineup],
          "Away Starting Lineup": [away_starting_lineup],
          "Away Bench Lineup": [away_bench_lineup],
          "Home Goal Timings": [home_team_goal_timings],
          "Away Goal Timings": [away_team_goal_timings],
          "Home Sub Timings": [home_team_sub_timings],
          "Away Sub Timings": [away_team_sub_timings],
          "Home Red Card Timings": [home_team_red_card_timings],
          "Away Red Card Timings": [away_team_red_card_timings]
        })], ignore_index = True)
        
        # Edit the source_df to reflect the new ma
        source_df.at[0, 'Match URL'] = match_urls

        # Drop first row if empty
        if (len(match_urls) == 0):
            source_df = source_df.drop(0)
            source_df = source_df.reset_index(drop=True)
            try:
              season = source_df.at[0, 'Season']
              match_urls = ast.literal_eval(source_df.at[0, 'Match URL'])
            except:
                print("Last Season")
            
#     Edit the initial files
    source_df.to_csv(source_file_path, index = False)
    df.to_csv(dest_file_path, mode = "a", index = False)

    print("Season:", season)
    print("Final Length:", len(match_urls))
    print("End of Function")
    return df

if __name__ == "__main__":
    print("Start of Scraping")
    scheduler = BackgroundScheduler(daemon=True)
    # write_match_data("match_url.csv", "match_data.csv", 2, scheduler)
    scheduler.add_job(write_match_data, 'interval', args=["match_url_test.csv", "match_data_test.csv", 5, scheduler], minutes=1)
    scheduler.start()
    print("Scheduler running: ", scheduler.get_jobs())
