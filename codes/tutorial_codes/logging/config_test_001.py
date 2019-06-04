import logging
import logging.config

logging.config.fileConfig(fname=r'.\config.conf', disable_existing_loggers=True)

logger = logging.getLogger('dante')
logger.debug('this is a debug info')
logger.info('this is a info info')
logger.warning('this is a warning info')
logger.error('this is an error info')
