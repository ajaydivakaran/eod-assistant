from logging.handlers import SysLogHandler

import logging
from logging import StreamHandler


def get_logger():
    logging.basicConfig(format='%(asctime)s: %(module)s.%(funcName)s: %(message)s', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.addHandler(SysLogHandler(address='/dev/log'))
    logger.addHandler(StreamHandler())
    return logger
