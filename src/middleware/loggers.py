import logging
import os

def get_logger(name: str):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        if not os.path.exists('src/logs'):
            os.makedirs('src/logs')

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler("src/logs/app.log")
        file_handler.setFormatter(formatter)

        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger