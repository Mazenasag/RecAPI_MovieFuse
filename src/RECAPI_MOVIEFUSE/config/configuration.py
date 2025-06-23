from RECAPI_MOVIEFUSE.constant import *
from RECAPI_MOVIEFUSE.utils.common import read_yaml , create_directories
from RECAPI_MOVIEFUSE.entity.config_entity import DataIngestionConfig ,DataPreprocessingConfig

class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_fetching
        create_directories([Path(config.save_file).parent])
        return DataIngestionConfig(
            base_url=config.base_url,
            search_endpoint=config.search_endpoint,
            total_pages=config.total_pages,
            save_file=Path(config.save_file),
            CSV_data_path=Path(config.CSV_data_path)
        )
        
    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        config = self.config.data_preprocessing
        create_directories([Path(config.processed_data_dir).parent])
        return DataPreprocessingConfig(
            data_path=Path(config.data_path),
            processed_data_dir=Path(config.processed_data_dir),
            processed_data_file=Path(config.processed_data_file),
        )
        