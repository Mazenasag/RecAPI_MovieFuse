import logging
import os    
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.log"
LOG_PATH ="logs"
os.makedirs(LOG_PATH,exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] File Name: %(filename)s - Line No:  %(lineno)d - %(levelname)s - %(message)s',
    level=logging.INFO,
)


logging.info("This is an info message.")
