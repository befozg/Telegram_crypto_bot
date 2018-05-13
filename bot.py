from telegram.ext import Updater, CommandHandler
import CryptoParser
import logging
from dateutil import parser as date_parser
import time
import os

with open('help.txt', 'r') as input_file:
    support_text = input_file.read()


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=support_text)


def bot_crate(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=CryptoParser.crate(*update.message.text.split()[1:]))


def bot_history(bot, update):
    message_text = update.message.text.split()
    del message_text[0]
    begin_time = time.mktime(date_parser.parse(message_text[1]).timetuple())
    end_time = time.mktime(date_parser.parse(message_text[2]).timetuple())
    CryptoParser.history(message_text[0], int(begin_time), int(end_time), *message_text[3:])
    bot.send_photo(chat_id=update.message.chat_id, photo=open('tmp_fig.png', 'rb'))
    os.remove('./tmp_fig.png')


def run_bot(token):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    crate_handler = CommandHandler('crate', bot_crate)
    history_handler = CommandHandler('history', bot_history)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(crate_handler)
    dispatcher.add_handler(history_handler)
    updater.start_polling()
