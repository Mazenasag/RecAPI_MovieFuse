import requests
from dotenv import load_dotenv
import os
import time
import json

load_dotenv()  # Loads variables from .env into environment

# print("API_KEY =", os.getenv("API_KEY"))

# url = "https://api.themoviedb.org/3/authentication"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}"
}

all_movies = []

for page in range(1, 51):  # 1 to 50 pages = 1,000 movies
    url = f"https://api.themoviedb.org/3/discover/movie?page={page}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        all_movies.extend(data['results'])
    else:
        print(f"Error on page {page}: {response.status_code}")
    time.sleep(0.25)  # Respect API rate limits

with open("movies_1000.json", "w", encoding="utf-8") as f:
    json.dump(all_movies, f, ensure_ascii=False, indent=2)