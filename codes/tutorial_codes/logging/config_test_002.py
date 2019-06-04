import logging
import logging.config

config_dict = {
    'version': 1,
    'formatters': {
        'c_format': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
        'f_format': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'c_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'c_format',
            'level': 'ERROR',
            'stream': 'ext://sys.stdout',
        },
        'f_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'f_format',
            'level': 'WARNING',
            'filename': 'cz_1.log'
        }
    },
    'loggers': {
        'dante': {
            'level': 'DEBUG',
            'handlers': ['c_handler', 'f_handler']
        },
    },
    # 'root': {
    #     'level': 'WARNING',
    #     'handlers': ['c_handler'],
    # },
}
logging.config.dictConfig(config_dict)
logger = logging.getLogger('dante')
logger.debug('this is a debug info')
logger.info('this is a info info')
logger.warning('this is a warning info')
logger.error('this is an error info')