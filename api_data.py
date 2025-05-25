import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Load secrets and variables
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": RIOT_API_KEY}
GAME_NAME = os.getenv("GAME_NAME")
TAG_LINE = os.getenv("TAG_LINE")

# Get PUUID from Riot ID
def get_puuid(game_name, tag_line):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get(url, headers=HEADERS)
    return response.json()["puuid"]

# Get summoner info from PUUID
def get_summoner_info(puuid):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Get match IDs
def get_match_ids(puuid, count=20):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Get match data
def get_match_data(match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Get champion static data
def get_champion_data():
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    version = requests.get(version_url).json()[0]
    champ_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    response = requests.get(champ_url)
    return response.json()

# Save to JSON
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Pipeline
puuid = get_puuid(GAME_NAME, TAG_LINE)
summoner_info = get_summoner_info(puuid)
save_to_json(summoner_info, "summoner_info.json")

match_ids = get_match_ids(puuid)

for match_id in match_ids:
    match_data = get_match_data(match_id)
    save_to_json(match_data, f"{match_id}.json")

champion_data = get_champion_data()
save_to_json(champion_data, "champions.json")
