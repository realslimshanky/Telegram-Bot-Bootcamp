from telegram.ext import Updater, CommandHandler


# Replace this with your Telegram Bot Token
TOKEN = 'Telegram Bot Token'


def start(bot, update):
    '''handles all the /start command and sends message back'''
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi! I'm bot!")


# Setting up updater class
updater = Updater(token=TOKEN)

# Setting up dispatcher class
dispatcher = updater.dispatcher

# Adding command handler
dispatcher.add_handler(CommandHandler('start', start))

# Application is run using polling method
updater.start_polling()
