import logging
import os
import random
import sys

from telegram.ext import CommandHandler, CallbackContext
from telebot.credentials import URL
from utils.utils import get_logger

logger = get_logger()


mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

if mode == "dev":
    def run(updater):
        logger.info("Dev mode select")
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        logger.info("Prod mode select")
        PORT = int(os.environ.get("PORT", "8001"))
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("{URL}{HOOK}".format(URL=URL, HOOK=TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


class Controller:
    """
    Controller class:
        The main responsibility of this class is 'controlling states of bot with user inputs and handlers', etc.
        It depends on your bot scenario you can create a main controller class for starting bot and common states of
        your bot and then create some other controller classes and inherit from main controller class.
    """

    def __init__(self, updater):
        self.updater = updater
        self.dispatcher = updater.dispatcher
        self.__process_handlers()

    def callback_minute(self, context: CallbackContext):
        # context.bot.send_message(chat_id='@test_channel_5',
        #                         text='One message every minute')
        context.bot.send_photo(chat_id='@test_channel_5',
                               photo='https://memepedia.ru/wp-content/uploads/2020/03/ty-chevo-nadelal-1.jpg',
                               caption='Кот Захар раз в полчаса')

    def start_handler(self, update, context):
        # Creating a handler-function for /start command
        logger.info("User {} started bot".format(update.effective_user["id"]))
        update.message.reply_text("Hello from Python!\nPress /random to get random number")

    def random_handler(self, update, context):
        # Creating a handler-function for /random command
        number = random.randint(0, 10)
        logger.info("User {} randomed number {}".format(update.effective_user["id"], number))
        update.message.reply_text("Random number: {}".format(number))

    def __process_handlers(self):
        j = self.updater.job_queue
        j.run_repeating(self.callback_minute, interval=1800, first=0)

        self.dispatcher.add_handler(CommandHandler("start", self.start_handler))
        self.dispatcher.add_handler(CommandHandler("random", self.random_handler))

        run(self.updater)
