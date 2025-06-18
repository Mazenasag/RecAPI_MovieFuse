from RECAPI_MOVIEFUSE.config.configuration import ConfigurationManager
from RECAPI_MOVIEFUSE.components.data_ingestion import DataIngestion
from exception import CustomException
import sys
from logger import logging

STAGE_NAME = 'Data Ingestion stage'

class DataIngestionPipeline:
    def __init__(self):    
        pass

    def main(self):
        try:
            logging.info(f">>> Starting {STAGE_NAME} <<<")

            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)

            logging.info("Fetching data from API...")
            data_ingestion.fetching_data_from_api()

            logging.info("Converting JSON to CSV...")
            data_ingestion.convert_json_to_csv()

            logging.info(f">>> {STAGE_NAME} completed successfully <<<")
        
        except Exception as e:
            logging.error(f"Exception occurred in {STAGE_NAME}")
            raise CustomException(e, sys)

if __name__ == '__main__':
    try:
        logging.info("=== Pipeline execution started ===")
        obj = DataIngestionPipeline()
        obj.main()
        logging.info("=== Pipeline execution completed ===")

    except Exception as e:
        logging.error("Pipeline execution failed.")
        raise CustomException(e, sys)
