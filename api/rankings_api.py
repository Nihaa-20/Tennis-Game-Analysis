import requests
import os
import json
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("SPORTRADAR_API_KEY")

# Doubles Rankings API endpoint
URL = f"https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key={API_KEY}"

def fetch_rankings():
    response = requests.get(URL)
    response.raise_for_status()  # Raises error if request failed
    return response.json()

def save_raw_data(data):
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/double_rankings.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("Raw rankings data saved successfully")

if __name__ == "__main__":
    data = fetch_rankings()
    save_raw_data(data)
