import functools
import logging
import os

from dotenv import load_dotenv


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class Logger:
    """
    Singleton logger class that is initialized the first time we get it.
    """

    def __init__(self):
        load_dotenv()
        log_format = f"%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(format=log_format,
                            level=os.environ.get('LOGLEVEL', 'INFO'))

        self.log = logging.getLogger()


logger = Logger().log


def log_and_except(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Started function {func.__name__}.")
            result = func(*args, **kwargs)
            logger.info(f"Finished function {func.__name__}.")
            return result
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e

    return wrapper


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Started function {func.__name__}.")
        result = func(*args, **kwargs)
        logger.info(f"Finished function {func.__name__}.")
        return result

    return wrapper
