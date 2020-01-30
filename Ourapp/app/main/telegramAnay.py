import logging, pprint
import requests, json, pickle
from model import predict

url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelUrls/'
# data = {'modelId': '353cea12-4dcc-47ee-b139-dd345157b17d', 'urls' : ['https://goo.gl/ICoiHc']}

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
token = '1028553795:AAEee86Tt40IHdGZe4JeooGRQfY_9UutE_w'
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
headers = {"content-type": "application/json"}
users_dict = {}
with open('models/tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

logger = logging.getLogger(__name__)

def process_text(text, maxlen=150):
    text = ' '.join(preprocess(text))
    # print(text)
    text = np.array([text])
    text = tokenizer.texts_to_sequences(text)
    text = sequence.pad_sequences(text, maxlen=maxlen)
    return text

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Updater, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update._effective_message.reply_text('Hi!')


def help(update: Updater, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update._effective_message.reply_text('Hey, my name is PewBot. Send more than 3 obscene messages, and youll get kicked. Enjoy!')


def echo(update: Updater, context: CallbackContext):
    """Echo the user message."""
    data = update._effective_message.text
    label, has_bullying, amount = predict(data)
    # logging.warning(update)
    send_data = ''.join(label)
    logging.warning(has_bullying)
    user_details = update['_effective_message']['from_user']
    username = user_details['username']
    users_dict[username] = 0 if username not in users_dict else users_dict[username]
    if has_bullying:
        logging.warning(username)
        users_dict[username] +=1
        if username:
            if users_dict[username] > 0:
                # logging.warning('Yayy')
                warn_data = "Issued warning number " + str(users_dict[username]) + " for you. Please refrain from any more such activities."
                update._effective_message.reply_text(warn_data)
            if users_dict[username] >=3:
                # update._effective_message.forward(user_details['id'])
                update['_effective_chat'].kick_member(update._effective_user.id)
                users_dict[username] = 0
                logging.warning('Greater than 3')
    logging.warning(user_details)
    # logging.warning(update['message'])
    # update._effective_message.reply_text(send_data)

def image_handle(update: Updater, context: CallbackContext):
    # logging.warning('For photos')
    # logging.warning(update.message['photo'][-1])
    user_details = update['_effective_user']
    username = user_details['username']
    users_dict[username] = 0 if username not in users_dict else users_dict[username]
    pic_list = update.message['photo']
    logging.warning(pic_list[-1].get_file().file_path)
    data = {'modelId': '4df5e7ba-e1e4-4e5b-9eb2-10ea96c465f3', 'urls' : [pic_list[-1].get_file().file_path]}
    headers = {
        'accept': 'application/x-www-form-urlencoded'
    }
    response = requests.request('POST', url, headers=headers, auth=requests.auth.HTTPBasicAuth('3lWlxT6SbjLIm-60Jxvb-tjPCICer6UM', ''), data=data)
    # logging.warning(response.text)
    probs = json.loads(response.text)
    logging.warning(probs)
    pred = probs['result'][0]['prediction']
    val = max(pred, key = lambda x:x['probability'])
    logging.warning(val)
    if val['label'] == 'nsfw':
        users_dict[username]+=1
        warn_data = "Issued warning number " + str(users_dict[username]) + " for you. Please refrain from any more such activities."
        update._effective_message.reply_text(warn_data)
    # print(response.text)

def error(update: Updater, context: CallbackContext):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, context.error)


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
    dp.add_handler(MessageHandler(Filters.all, image_handle))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logging
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()