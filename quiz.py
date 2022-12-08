from telegram.ext import Updater,MessageHandler,Filters,CallbackContext,CommandHandler,CallbackQueryHandler
from telegram import Update, ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup,InputMediaPhoto
import requests
import telegram

TOKEN='5621731301:AAHRxF4B3r3rQMoNOz21zs-WdhR4FmD7-hM'


updater=Updater(TOKEN)

def start(update:Update, context:CallbackContext):
    arr=[]
    url='http://127.0.0.1:8000/quiz/'
    data=requests.get(url).json()
    for i in data:
        inlinekeyboard = InlineKeyboardButton(f'{i["title"]}',callback_data="✋"+str(i['id']))
        arr.append(inlinekeyboard)
    reply_markup = InlineKeyboardMarkup([arr])
    update.message.reply_text(text='quiz', reply_markup=reply_markup)

def topic(update:Update, context:CallbackContext):
    list1=[]
    query = update.callback_query
    id = query.data[1:]
    url=f'http://127.0.0.1:8000/topic/{id}/'
    data = requests.get(url).json()
    for i in data["topic"]:
        inlinekeyboard = InlineKeyboardButton(f'{i["t_name"]}', callback_data="👍"+str(i["id"]))
        list1.append(inlinekeyboard)
    inlinekeyboard1=InlineKeyboardButton("◀️", callback_data="back")
    reply_markup = InlineKeyboardMarkup([list1,[inlinekeyboard1]],)
    query.edit_message_text(text="Python", reply_markup=reply_markup)


updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CallbackQueryHandler(topic, pattern="✋"))

updater.start_polling()
updater.idle()