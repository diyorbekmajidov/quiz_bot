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

def start1(update:Update, context:CallbackContext):
    arr=[]
    query = update.callback_query
    url='http://127.0.0.1:8000/quiz/'
    data=requests.get(url).json()
    for i in data:
        inlinekeyboard = InlineKeyboardButton(f'{i["title"]}',callback_data="✋"+str(i['id']))
        arr.append(inlinekeyboard)
    reply_markup = InlineKeyboardMarkup([arr])
    query.edit_message_text(text='quiz', reply_markup=reply_markup)

def topic(update:Update, context:CallbackContext):
    list1=[]
    query = update.callback_query
    id = query.data[1:]
    url=f'http://127.0.0.1:8000/topic/{id}/'
    data = requests.get(url).json()
    for i in data["topic"]:
        inlinekeyboard = InlineKeyboardButton(f'{i["t_name"]}', callback_data="👍"+str(i["id"]))
        list1.append(inlinekeyboard)
    inlinekeyboard1=InlineKeyboardButton("◀️", callback_data="◀back")
    reply_markup = InlineKeyboardMarkup([list1,[inlinekeyboard1]],)
    query.edit_message_text(text="Python", reply_markup=reply_markup)

def quetion(update:Update, context:CallbackContext):
    
    bot = context.bot
    query=update.callback_query
    chat_id = query.message.chat.id 
    id = query.data[1:]
    url=f'http://127.0.0.1:8000/question/{id}/'
    data = requests.get(url).json()
    for i in data:
        list2=[]
        for j in i["options"]:
            inlinekeyboard = InlineKeyboardButton(f'{j["option"]}', callback_data="👎"+str(j["id"]))
            list2.append([inlinekeyboard])
        reply_markup = InlineKeyboardMarkup(list2)
        bot.sendMessage(chat_id,text=i["quetion_name"], reply_markup = reply_markup)
    query.edit_message_text( text = "Test savolari omad!", reply_markup=None)

updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CallbackQueryHandler(topic, pattern="✋"))
updater.dispatcher.add_handler(CallbackQueryHandler(start1, pattern="◀back"))
updater.dispatcher.add_handler(CallbackQueryHandler(quetion, pattern="👍"))

updater.start_polling()
updater.idle()