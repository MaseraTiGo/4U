import logging
import logging.config
logging.config.dictConfigClass
logger = logging.getLogger(__name__)

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(r'.\cz_1.log')

c_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.WARNING)

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.debug('this is a debug info')
logger.info('this is a info info')
logger.warning('this is a warning info')
logger.error('this is an error info')