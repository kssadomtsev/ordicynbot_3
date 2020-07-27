import os


from telegram.ext import Updater
from controller.controller import Controller
from utils.utils import get_logger

logger = get_logger()

# Getting mode, so we could define run function for local and Heroku setup

TOKEN = os.getenv("TOKEN")

if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)
    controller = Controller(updater=updater)

