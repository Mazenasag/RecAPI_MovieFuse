import os
import sys
import re
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.exception import CustomException
from RECAPI_MOVIEFUSE.entity.config_entity import DataPreprocessingConfig


class MoviePreprocessing:
    def __init__(self, config: DataPreprocessingConfig):
        self.config = config
        self.scaler = StandardScaler()
        self.mlb = MultiLabelBinarizer()
        self.genre_map = {
            28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
            80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
            14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
            9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
            10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
        }

    def load_data(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.config.data_path)
            logging.info(f"Data loaded from {self.config.data_path}, shape: {df.shape}")
            return df
        except Exception as e:
            logging.error(f"Failed to load data: {e}")
            raise CustomException(f"Failed to load data: {e}", e)

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        initial_shape = df.shape
        df = df.dropna().drop_duplicates().reset_index(drop=True)
        logging.info(f"Removed duplicates and NAs: before {initial_shape}, after {df.shape}")
        return df

    def process_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
        return df

    def clean_text(self, text: str) -> str:
        if pd.isnull(text):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return text.strip()

    def clean_text_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df['title'] = df['title'].apply(self.clean_text)
        df['overview'] = df['overview'].apply(self.clean_text)
        return df

    def encode_genres(self, df: pd.DataFrame) -> pd.DataFrame:
        def parse_genre_ids(x):
            if isinstance(x, str) and pd.notnull(x):
                return list(map(int, x.split(',')))
            elif isinstance(x, list):
                return x
            else:
                return []

        df['genre_ids'] = df['genre_ids'].apply(parse_genre_ids)

        genre_encoded = pd.DataFrame(
            self.mlb.fit_transform(df['genre_ids']),
            columns=self.mlb.classes_,
            index=df.index
        )
        df = pd.concat([df, genre_encoded], axis=1).drop('genre_ids', axis=1)
        df = df.rename(columns=self.genre_map)
        return df

    def split_data(self, df: pd.DataFrame):
        train_df, test_df = train_test_split(
            df, test_size=0.2, random_state=42
        )
        logging.info(f"Split data: train={train_df.shape}, test={test_df.shape}")
        return train_df, test_df

    def scale_features(self, train_df: pd.DataFrame, test_df: pd.DataFrame):
        scale_cols = ['release_date', 'popularity', 'vote_average', 'vote_count']

        # Scale safely without modifying original structure
        train_scaled = pd.DataFrame(
            self.scaler.fit_transform(train_df[scale_cols]),
            columns=scale_cols,
            index=train_df.index
        )
        test_scaled = pd.DataFrame(
            self.scaler.transform(test_df[scale_cols]),
            columns=scale_cols,
            index=test_df.index
        )

        train_df[scale_cols] = train_scaled
        test_df[scale_cols] = test_scaled

        logging.info("Numerical features scaled successfully.")
        return train_df, test_df

    def save_data(self, data: pd.DataFrame, filename: Path):
        os.makedirs(self.config.processed_data_dir, exist_ok=True)
        save_path = os.path.join(self.config.processed_data_dir, filename)
        data.to_csv(save_path, index=False)
        logging.info(f"Data saved successfully to {save_path}")

    def preprocess(self):
        try:
            df = self.load_data()
            df = self.remove_duplicates(df)
            df = self.process_dates(df)
            df = df.drop('original_language', axis=1, errors='ignore')
            df = self.clean_text_columns(df)
            df = self.encode_genres(df)

            train_df, test_df = self.split_data(df)
            train_df, test_df = self.scale_features(train_df, test_df)

            self.save_data(train_df, self.config.processed_train_file)
            self.save_data(test_df, self.config.processed_test_file)

            logging.info("Preprocessing pipeline completed successfully.")
            return train_df, test_df, self.scaler

        except Exception as e:
            logging.error(f"Error in preprocessing: {e}")
            raise CustomException(f"Error in preprocessing: {e}", e)
