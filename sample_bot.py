from telegram.ext import Updater, CommandHandler
import logging
import os
import json
import sys
import signal
import subprocess


def manage_process_id():
    '''
    Process ID Management: This part of the code helps out when you want to run
    your program in background using '&'. This will save the process id of the
    program going in background in a file named 'pid'. Now, when you run you
    program again, the last one will be terminated with the help of pid. If in
    case the no process exist with given process id, simply the `pid` file will
    be deleted and a new one with current pid will be created.
    '''
    currentPID = os.getpid()
    if 'pid' not in os.listdir():
        with open('pid', mode='w') as file:
            file.write(str(currentPID))
    else:
        with open('pid', mode='r') as f:
            try:
                os.kill(int(f.read()), signal.SIGTERM)
                logging.info("Terminating previous instance of %s" % os.path.realpath(__file__))
            except ProcessLookupError:
                subprocess.run(['rm', 'pid'])
        with open('pid', mode='w') as file:
            file.write(str(currentPID))


def get_telegram_token():
    '''
    Token Management Starts: This part will check for the config.txt file which
    holds the Telegram Token/Key and will also give a user friendly message if
    they are invalid. New file is created if not present in the project directory.
    '''
    configError = "Please open config.txt file located in the project directory and relace the value '0' of Telegram-Bot-Token with the Token you recieved from botfather"
    if 'config.json' not in os.listdir():
        with open('config.json', mode='w') as f:
            json.dump({'Telegram-Bot-Token': '<Replace this with token>'}, f)
            logging.error(configError)
            sys.exit(0)
    else:
        with open('config.json', mode='r') as f:
            config = json.loads(f.read())
            if config["Telegram-Bot-Token"]:
                logging.info("Token Present, I am on!...")
                return config["Telegram-Bot-Token"]
            else:
                logging.error(configError)
                sys.exit(0)


def start(bot, update):
    '''handles all the /start command and sends message back'''
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi! I'm bot!")


if __name__ == '__main__':
    # Configurint Logging Module
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Managing program process id
    manage_process_id()

    # Setting up updater class
    updater = Updater(token=get_telegram_token())

    # Setting up dispatcher class
    dispatcher = updater.dispatcher

    # Adding command handler
    dispatcher.add_handler(CommandHandler('start', start))

    # Application is run using polling method
    updater.start_polling()
