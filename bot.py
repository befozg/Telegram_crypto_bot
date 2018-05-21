from telegram.ext import Updater, CommandHandler
import parser
import logging
from dateutil import parser as date_parser
import time
import os

with open('readme.txt', 'r') as input_file:
    start_text = input_file.read()

with open('help.txt', 'r') as input_file:
    support_text = input_file.read()


def start(bot, update):
    """
    Отвечает за команду /start и отправляет в chat_id приветствие.
    """
    bot.send_message(chat_id=update.message.chat_id, text=start_text)


def help(bot, update):
    """
    Отвечает за команду /help и отправляет в chat_id инструкцию по командам.
    """
    bot.send_message(chat_id=update.message.chat_id, text=support_text)


def bot_crate(bot, update):
    """
    Отвечает за команду /crate и отправляет в chat_id значение, возвращаемое
    parser_crate./home/karen
    """
    bot.send_message(
        chat_id=update.message.chat_id,
        text=parser.crate(*update.message.text.split()[1:]))


def bot_history(bot, update):
    """
    Отвечает за команду /hystory и отправляет в chat_id фото графика,
    показывающаге историю изменения курса.
    """
    try:
        message_text = update.message.text.split()
        del message_text[0]
        begin_time = time.mktime(date_parser.parse(message_text[1]).timetuple())
        end_time = time.mktime(date_parser.parse(message_text[2]).timetuple())
        parser.history(message_text[0], int(begin_time), int(end_time), *message_text[3:])
        if(date_parser.parse(message_text[1]).timetuple()[0] < 2010):
            bot.send_message(chat_id=update.message.chat_id, text='Вводить надо в промежутке 2010 - 2018гг. :)')
        else:
            bot.send_photo(chat_id=update.message.chat_id, photo=open('tmp_fig.png', 'rb'))
            os.remove('./tmp_fig.png')
    except KeyError,IndexError:
        bot.send_message(chat_id=update.message.chat_id, text='Вводить надо в формате /history и аргументы :)')

def run_bot(token):
    """
    Запускает бот по token,
    :param token: token моего бота, который надо запустить
    """
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    updater = Updater(token=token)
    """
    Создаем диспетчер, чтобы для каждой комманды создать handler
    """
    dispatcher = updater.dispatcher
    """
    Создаем handler для всех комманд и добавляем в диспетчер
    """
    start_handler = CommandHandler('start', start)
    crate_handler = CommandHandler('crate', bot_crate)
    history_handler = CommandHandler('history', bot_history)
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(crate_handler)
    dispatcher.add_handler(history_handler)
    dispatcher.add_handler(help_handler)
    updater.start_polling()
