import logging, pprint
import requests, json, pickle
from preprocess import preprocess

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
token = '1028553795:AAEee86Tt40IHdGZe4JeooGRQfY_9UutE_w'
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
headers = {"content-type": "application/json"}

with open('models/tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

logger = logging.getLogger(__name__)

def predict(text, maxlen=150):
    text = ' '.join(preprocess(text))
    # print(text)
    text = np.array([text])
    text = tokenizer.texts_to_sequences(text)
    text = sequence.pad_sequences(text, maxlen=maxlen)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Updater, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update._effective_message.reply_text('Hi!')


def help(update: Updater, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update._effective_message.reply_text('Help!')


def echo(update: Updater, context: CallbackContext):
    """Echo the user message."""
    # print(bool(update.get(_effective_message)))
    # logging.warning(update._effective_message)
    data = update._effective_message.text
    json_response = requests.post('http://13.127.65.157:3000/v1/models/cb:predict',
                                data=data, headers=headers)
    logging.warning(json.loads(json_response.text))
    # update._effective_message.reply_text(json_response)


def error(update: Updater, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()