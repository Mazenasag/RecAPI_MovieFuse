from RECAPI_MOVIEFUSE.config.configuration import ConfigurationManager
from RECAPI_MOVIEFUSE.components.data_training import MovieRecommender
from exception import CustomException
from logger import logging
import sys


STAGE_NAME = 'Data Training Stage'


class DataPreprocessingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logging.info(f">>> Starting {STAGE_NAME} <<<")

            config=ConfigurationManager()
            data_training_config=config.get_model_training_config()
            movie_training = MovieRecommender(config=data_training_config)
            movie_training.preprocess_and_cache()
            recommendations=movie_training.recommend('life after fighting')
            print(recommendations)
        except Exception as e:
           raise CustomException(e,sys)


if __name__ == '__main__':
    try:
        logging.info("=== Pipeline execution started ===")
        pipeline = DataPreprocessingPipeline()
        pipeline.main()
        logging.info("=== Pipeline execution completed ===")

    except Exception as e:
        logging.error("Pipeline execution failed.")
        raise CustomException(e, sys)
