from RECAPI_MOVIEFUSE.config.configuration import ConfigurationManager
from RECAPI_MOVIEFUSE.components.data_ingestion import DataIngestion
from exception import CustomException
from logger import logging
import sys

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()

    def main(self):
        try:
            logging.info(f"\n\n====== {STAGE_NAME} Started ======\n")
            
            # Load config and initialize ingestion
            data_ingestion_config = self.config_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)

            # Fetch from API and save images/JSON
            logging.info("🔍 Fetching data from API...")
            data_ingestion.fetching_data_from_api()

            # Convert to CSV
            logging.info("📄 Converting JSON to CSV...")
            data_ingestion.convert_json_to_csv()

            logging.info(f"\n\n====== {STAGE_NAME} Completed Successfully ======\n")

        except Exception as e:
            logging.error(f"❌ Exception occurred in {STAGE_NAME}")
            raise CustomException(e, sys)

if __name__ == '__main__':
    try:
        logging.info("🚀 Pipeline execution started.")
        pipeline = DataIngestionPipeline()
        pipeline.main()
        logging.info("✅ Pipeline execution finished successfully.")

    except Exception as e:
        logging.error("❌ Pipeline execution failed.")
        raise CustomException(e, sys)
