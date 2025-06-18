import os
import time
import json
import requests
from dotenv import load_dotenv
from pathlib import Path
import yaml

# Load environment variables (.env)
load_dotenv()

# Load config from YAML
def load_config():
    config_path = Path("config/config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def fetch_movies():
    config = load_config()
    api_config = config["api"]
    output_config = config["output"]

    base_url = api_config["base_url"]
    endpoint = api_config["search_endpoint"]
    total_pages = api_config["total_pages"]
    save_path = output_config["raw_data_path"]

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    all_movies = []

    for page in range(1, total_pages + 1):
        url = f"{base_url}{endpoint}?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            all_movies.extend(data["results"])
        else:
            print(f"❌ Error on page {page}: {response.status_code}")

        time.sleep(0.25)  # Respect API rate limits

    # Ensure output directory exists
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(all_movies)} movies to {save_path}")
    return all_movies
