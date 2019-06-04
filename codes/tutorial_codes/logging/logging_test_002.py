import logging
def test():
    logger = logging.getLogger(__name__)
    print('test_002-------->', id(logger), logger)
    logger.error('logging_test_002 error occurred!')