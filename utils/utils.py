import logging

def get_logger():
    logger = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    return logger