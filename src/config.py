import logging
from environs import Env
from pathlib import Path

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

NEW_KEY_DIR = BASE_DIR / env.str("NEW_KEY_DIR")
USED_KEY_DIR = BASE_DIR / env.str("USED_KEY_DIR")

PRICE = {
    '1': 100,
    '2': 190,
    '3': 250,
    '6': 490
}

PAYMENTS_TOKEN='2051251535:TEST:OTk5MDA4ODgxLTAwNQ'
ADMINS = [297822605]

logging.basicConfig(level=logging.INFO)
