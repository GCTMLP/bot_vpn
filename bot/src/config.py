from environs import Env
from pathlib import Path

ADMINS = [297822605]

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

PAYMENTS_TOKEN = env.str("PAYMENTS_TOKEN")

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / 'logs'


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "info": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "standard",
            "filename": LOG_DIR / "info.log",
            "when": "D",
            "backupCount": 5,
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "standard",
            "filename": LOG_DIR / "error.log",
            "when": "D",
            "backupCount": 5,
        },
    },
    "loggers": {
        "info": {
            "handlers": ["info", "default"],
            "level": "INFO",
            "propagate": False,
        },
        "error": {
            "handlers": ["error", "default"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
