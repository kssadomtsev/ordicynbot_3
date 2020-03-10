import logging
import os
import random
import sys

from telegram.ext import Updater, CommandHandler, CallbackContext
from telebot.credentials import bot_token, URL

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
# TOKEN = os.getenv("TOKEN")

TOKEN = bot_token
# mode = mode

if mode == "dev":
    def run(updater):
        logger.info("Dev mode select")
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        logger.info("Prod mode select")
        PORT = int(os.environ.get("PORT", "8443"))
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("{URL}{HOOK}".format(URL=URL, HOOK=TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def callback_minute(context: CallbackContext):
    #context.bot.send_message(chat_id='@test_channel_5',
    #                         text='One message every minute')
    context.bot.send_photo(chat_id='@test_channel_5',
                           photo='https://memepedia.ru/wp-content/uploads/2020/03/ty-chevo-nadelal-1.jpg',
                           caption='Кот Захар раз в полчаса')


def start_handler(update, context):
    # Creating a handler-function for /start command
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text("Hello from Python!\nPress /random to get random number")


def random_handler(update, context):
    # Creating a handler-function for /random command
    number = random.randint(0, 10)
    logger.info("User {} randomed number {}".format(update.effective_user["id"], number))
    update.message.reply_text("Random number: {}".format(number))


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    j = updater.job_queue
    j.run_repeating(callback_minute, interval=1800, first=0)

    dp.add_handler(CommandHandler("start", start_handler))
    dp.add_handler(CommandHandler("random", random_handler))

    run(updater)
