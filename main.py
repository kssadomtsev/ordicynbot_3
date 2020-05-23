import os


from telegram.ext import Updater
from controller.controller import Controller
from utils.utils import get_logger

logger = get_logger()

# Getting mode, so we could define run function for local and Heroku setup

TOKEN = os.getenv("TOKEN")
REQUEST_KWARGS = {
    'proxy_url': 'socks5://195.181.215.234:8080',
    'urllib3_proxy_kwargs': {
        'username': 'anon',
        'password': 'Durf2OqgQ=',
    }
}

# mode = mode
mode = os.getenv("MODE")

if __name__ == '__main__':
    logger.info("Starting bot")
    if mode == "dev":
        updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    elif mode == "prod":
        updater = Updater(TOKEN, use_context=True)
    controller = Controller(updater=updater)

