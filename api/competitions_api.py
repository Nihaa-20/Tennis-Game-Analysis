import requests
import os
import json
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("SPORTRADAR_API_KEY")

# Competitions API endpoint
URL = f"https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key={API_KEY}"

def fetch_competitions():
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()

def save_raw_data(data):
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/competitions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("Raw competitions data saved successfully")

if __name__ == "__main__":
    data = fetch_competitions()
    save_raw_data(data)
