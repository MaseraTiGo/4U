import logging
from logging_test_002 import test
logger = logging.getLogger(__name__)
# f_handler = logging.FileHandler(r'.\cz.log')
# f_handler.setLevel(logging.DEBUG)
# f_format = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
# f_handler.setFormatter(f_format)
# logger.addHandler(f_handler)
logger.error('logging_test_001 error occurred!')
print('test_001-------->', id(logger), logger)
test()
