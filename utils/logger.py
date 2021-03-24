import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_timed_rotating_log(path):
    handler = TimedRotatingFileHandler(path,
                                       when='midnight',
                                       backupCount=1)
    handler.suffix = "%Y-%m-%d"
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# how to use
# logger.debug('debug message')
# logger.info('informational message')
# logger.warning('warning')
# logger.error('error message')
# logger.critical('critical failure')
