# coding=UTF-8

import sys
import os
import logging
import logging.config

_logger_dir = os.path.dirname(os.path.abspath(__file__))
_logger_file = os.path.join(_logger_dir, "logger.conf")
logging.config.fileConfig(_logger_file)
logger = logging.getLogger("root")
