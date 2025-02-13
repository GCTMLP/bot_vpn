import logging
import logging.config
from environs import Env
from pathlib import Path

import os
from os.path import join, dirname
from pathlib import Path
from string import Template

BASE_DIR = Path(__file__).resolve().parent.parent


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_NAME = env.str("DB_NAME")
DB_ISOLATION_LEVEL = env.str("DB_ISOLATION_LEVEL")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

NEW_KEY_DIR = str(BASE_DIR / env.str("NEW_KEY_DIR"))+'/'
USED_KEY_DIR = str(BASE_DIR / env.str("USED_KEY_DIR"))+'/'
INSTRUCTION_DIR = str(BASE_DIR / env.str("INSTRUCTION_DIR"))+'/'

PRICE = {
    '1': 100,
    '2': 190,
    '3': 250,
    '6': 490
}

PAYMENTS_TOKEN='381764678:TEST:109740'
ADMINS = [297822605]


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / 'logs'

error_file_log_lvl = 'ERROR'
info_file_log_lvl = 'INFO'

LOGGER_NAME_ERROR = f'{error_file_log_lvl}_LOGS'
LOGGER_NAME_INFO = f'{info_file_log_lvl}_LOGS'

LOGGER_NAME = 'LOGS'

error_log_file = LOG_DIR / f'{LOGGER_NAME_ERROR}.log'

info_log_file = LOG_DIR / f'{LOGGER_NAME_INFO}.log'


file_format = '%(asctime)-15s %(levelname)-8s %(module)s ' \
              '%(pathname)s:%(lineno)d %(message)s'

LOGGER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file_format': {
            'format': '%(asctime)-15s | %(levelname)-8s | %(pathname)s %(funcName)s():%(lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'console_format': {
            'format': '%(asctime)-15s | %(levelname)-8s | %(module)s %(funcName)s():%(lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    }
}


LOG = logging.getLogger(LOGGER_NAME)
log_formatter = logging.Formatter(file_format)


ERROR_LOG = logging.handlers.TimedRotatingFileHandler(error_log_file, when='D')
ERROR_LOG.setFormatter(log_formatter)
ERROR_LOG.setLevel(logging.ERROR)
LOG.addHandler(ERROR_LOG)

INFO_LOG = logging.handlers.TimedRotatingFileHandler(info_log_file, when='D')
INFO_LOG.setFormatter(log_formatter)
INFO_LOG.setLevel(logging.INFO)
LOG.addHandler(INFO_LOG)


LOG.setLevel(logging.INFO)