from dataclasses import dataclass
from pathlib import Path
@dataclass
class DataIngestionConfig:
  base_url: str
  search_endpoint: str
  total_pages: int
  save_file: Path
  CSV_data_path: Path