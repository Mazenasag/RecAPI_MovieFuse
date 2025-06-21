from RECAPI_MOVIEFUSE.config.configuration import ConfigurationManager
from RECAPI_MOVIEFUSE.components.data_preprocessing import MoviePreprocessing
from exception import CustomException
from logger import logging
import sys

STAGE_NAME = 'Data Preprocessing Stage'


class DataPreprocessingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logging.info(f">>> Starting {STAGE_NAME} <<<")

            config = ConfigurationManager()
            data_preprocessing_config = config.get_data_preprocessing_config()

            movie_preprocessor = MoviePreprocessing(config=data_preprocessing_config)
            movie_preprocessor.preprocess()

            logging.info(f">>> {STAGE_NAME} completed successfully <<<")

        except Exception as e:
            logging.error(f"Exception occurred in {STAGE_NAME}")
            raise CustomException(e, sys)


if __name__ == '__main__':
    try:
        logging.info("=== Pipeline execution started ===")
        pipeline = DataPreprocessingPipeline()
        pipeline.main()
        logging.info("=== Pipeline execution completed ===")

    except Exception as e:
        logging.error("Pipeline execution failed.")
        raise CustomException(e, sys)
