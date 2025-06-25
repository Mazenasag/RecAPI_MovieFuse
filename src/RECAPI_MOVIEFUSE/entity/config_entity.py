from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class DataIngestionConfig:
    base_url: str
    search_endpoint: str
    total_pages: int
    save_file: Path
    CSV_data_path: Path


@dataclass
class DataPreprocessingConfig:
    data_path: Path
    processed_data_dir: Path
    processed_data_file: Path


@dataclass
class ModelTrainingConfig:
    df_original: Path
    combined_path:Path
    model_name: str
    text_column: str
    numeric_columns: List[str]
    genre_columns: List[str]
    genre_weight: int
    similarity_top_n: int
    min_genre_overlap: int