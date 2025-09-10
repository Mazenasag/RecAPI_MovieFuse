from src.RECAPI_MOVIEFUSE.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from exception import CustomException
import sys
from logger import logging


STAGE_NAME='Date Ingestion stage'
if __name__ == '__main__':
    try:
        logging.info("=== Pipeline execution started ===")
        obj = DataIngestionPipeline()
        obj.main()
        logging.info("=== Pipeline execution completed ===")

    except Exception as e:
        logging.error("Pipeline execution failed.")
        raise CustomException(e, sys)