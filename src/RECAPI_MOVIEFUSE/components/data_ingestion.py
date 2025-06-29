import os
import time
import json
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from logger import logging
from exception import CustomException
from RECAPI_MOVIEFUSE.entity.config_entity import DataIngestionConfig
import sys

load_dotenv()

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def fetching_data_from_api(self):
        try:
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {os.getenv('API_KEY')}"
            }

            all_movies = []

            # Create necessary directories
            Path(self.config.save_file).parent.mkdir(parents=True, exist_ok=True)
            Path(self.config.images_dir).mkdir(parents=True, exist_ok=True)

            for page in range(1, self.config.total_pages + 1):
                url = f"{self.config.base_url}{self.config.search_endpoint}?page={page}"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    logging.info(f"✅ Page {page} fetched successfully.")
                    data = response.json()

                    for movie in data.get("results", []):
                        poster_path = movie.get("poster_path")
                        if poster_path:
                            full_image_url = f"{self.config.image_base_url}{poster_path}"
                            movie["full_poster_url"] = full_image_url

                            image_file_path = Path(self.config.images_dir) / f"{movie['id']}.jpg"
                            if not image_file_path.exists():  # Avoid re-downloading
                                image_response = requests.get(full_image_url, stream=True)
                                if image_response.status_code == 200:
                                    with open(image_file_path, "wb") as img_file:
                                        for chunk in image_response.iter_content(1024):
                                            img_file.write(chunk)
                                    logging.info(f"🖼️ Image saved for movie ID {movie['id']}")
                                else:
                                    logging.warning(f"❌ Failed to download image for movie ID {movie['id']}")
                        else:
                            movie["full_poster_url"] = ""

                        all_movies.append(movie)
                else:
                    logging.warning(f"❌ Failed to fetch page {page}: Status Code {response.status_code}")

                time.sleep(0.25)

            with open(self.config.save_file, "w", encoding="utf-8") as f:
                json.dump(all_movies, f, ensure_ascii=False, indent=2)
                logging.info(f"✅ Fetched data saved to {self.config.save_file}")

        except Exception as e:
            logging.error("❗ An error occurred during fetching data from the API.")
            raise CustomException(e, sys)

    def convert_json_to_csv(self):
        try:
            with open(self.config.save_file, "r", encoding="utf-8") as f:
                movies = json.load(f)
                logging.info(f"📦 Loaded JSON data from {self.config.save_file}")

            processed_movies = []
            for movie in movies:
                processed_movies.append({
                    "id": movie.get("id"),
                    "title": movie.get("title"),
                    "original_language": movie.get("original_language"),
                    "release_date": movie.get("release_date"),
                    "overview": movie.get("overview"),
                    "popularity": movie.get("popularity"),
                    "vote_average": movie.get("vote_average"),
                    "vote_count": movie.get("vote_count"),
                    "genre_ids": ",".join(str(gid) for gid in movie.get("genre_ids", [])),
                    "poster_url": movie.get("full_poster_url", "")
                })

            df = pd.DataFrame(processed_movies)
            Path(self.config.CSV_data_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(self.config.CSV_data_path, index=False)
            logging.info(f"✅ CSV file saved successfully at {self.config.CSV_data_path}")

        except Exception as e:
            logging.error("❗ An error occurred during conversion from JSON to CSV.")
            raise CustomException(e, sys)
