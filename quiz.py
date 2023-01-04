from telegram.ext import Updater,MessageHandler,Filters,CallbackContext,CommandHandler,CallbackQueryHandler
from telegram import Update, ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup,InputMediaPhoto
import requests
import telegram
from tinydb import TinyDB

db=TinyDB('quetion.json', indent=4, separators=(',',':'))

TOKEN='5621731301:AAHRxF4B3r3rQMoNOz21zs-WdhR4FmD7-hM'


updater=Updater(TOKEN)

def start(update:Update, context:CallbackContext):
    arr=[]
    chat_id = update.message.chat.id 
    first_name = update.message.from_user.first_name
    url1=f'http://127.0.0.1:8000/api/student/'
    url='http://127.0.0.1:8000/api/quiz/'
    data_list={
        "telegram_id":chat_id,
        "list_question":[],
        "first_name":first_name,
    }
    r=requests.post(url1, json=data_list)
    data=requests.get(url).json()
    for i in data:
        inlinekeyboard = InlineKeyboardButton(f'{i["title"]}',callback_data="✋"+str(i['id']))
        arr.append(inlinekeyboard)
    reply_markup = InlineKeyboardMarkup([arr])
    update.message.reply_text(text='quiz', reply_markup=reply_markup)

def start1(update:Update, context:CallbackContext):
    arr=[]
    query = update.callback_query
    url='http://127.0.0.1:8000/api/quiz/'
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
    
    url=f'http://127.0.0.1:8000/api/topic/{id}/'

    data = requests.get(url).json()
    
 
    for i in data["topic"]:
        inlinekeyboard = InlineKeyboardButton(f'{i["title"]}', callback_data="👍"+str(i["id"]))
        list1.append(inlinekeyboard)
    inlinekeyboard1=InlineKeyboardButton("◀️", callback_data="◀back")
    reply_markup = InlineKeyboardMarkup([list1,[inlinekeyboard1]],)
    query.edit_message_text(text="Python", reply_markup=reply_markup)
    query.answer("topic", show_alert=True)


def quetion(update:Update, context:CallbackContext):
    
    bot = context.bot
    query=update.callback_query
    chat_id = query.message.chat.id 
    first_name = query.from_user.first_name

    id = query.data[1:]
    url= f'http://127.0.0.1:8000/api/quiz/{id}/'
    data = requests.get(url).json()
    # print(pk, pk_quistion)
    url3=f'http://127.0.0.1:8000/api/resultadd/'
    

    qeution_list=data["topic"]["quetion_index"]
    url1=f'http://127.0.0.1:8000/api/studentget/{chat_id}/'
    r = requests.get(url1).json()
    
    result_user = {
        "score":0,
        "student":r['id'],
        "topic":id,
    }
    request_data= requests.post(url3, json=result_user)

    url2=f'http://127.0.0.1:8000/api/updaterstudent/{r["id"]}/'
    if len(qeution_list)>0:
        pk = data['topic']['id']
        for i in data['topic']['question'][qeution_list[0]]['optons']:
            pk_quistion=i['id']

        data_question=data['topic']["quetion_index"][0]
        img=data['topic']['question'][data_question]['img']
        text=data['topic']['question'][data_question]['title']
        inlineKeyboard = InlineKeyboardButton('A',callback_data=f'⏭{id} {pk} A{pk_quistion}')
        inlineKeyboard1 = InlineKeyboardButton('B',callback_data=f'⏭{id} {pk} B{pk_quistion}')
        inlineKeyboard2 = InlineKeyboardButton('C',callback_data=f'⏭{id} {pk} C{pk_quistion}')
        inlineKeyboard3 = InlineKeyboardButton('D',callback_data=f'⏭{id} {pk} D{pk_quistion}')
        inlineKeyboard4 = InlineKeyboardButton('Test natija olish',callback_data='✅')
        reply_markup = InlineKeyboardMarkup([
            [inlineKeyboard,inlineKeyboard1,inlineKeyboard2,inlineKeyboard3],[inlineKeyboard4]
            ])
        updater.bot.sendPhoto(chat_id, img, text, reply_markup=reply_markup)
        if len(qeution_list) > 0:
                qeution_list.pop(0)
                data_list = {
                    "list_question":qeution_list,
                    }
                r=requests.post(url2, json = data_list)
                
        else :
            updater.bot.sendMessage(chat_id, 'Bu mavzu bo\'yicha savollarimiz tugadi.')
    return r.status_code

def next_quetion(update:Update, context:CallbackContext):
    query=update.callback_query
    chat_id = query.message.chat.id 
    id = query.data.split()[1]
    url1=f'http://127.0.0.1:8000/api/studentget/{chat_id}/'
    url=f'http://127.0.0.1:8000/api/quiz/{id}/'
    
    data = requests.get(url).json()
    r = requests.get(url1).json()
    qeution_list=r['list_question']
    url2=f'http://127.0.0.1:8000/api/updaterstudent/{r["id"]}/'

    if len(qeution_list)>0:
        list2=[]
        data_question=r['list_question'][0]
        pk = data['topic']['id']
        for i in data['topic']['question'][qeution_list[0]]['optons']:
            print(i)
            pk_quistion=i['id']
        
        img=data['topic']['question'][data_question]['img']
        text=data['topic']['question'][data_question]['title']
        inlineKeyboard = InlineKeyboardButton('A',callback_data=f'⏭{id} {pk} A{pk_quistion}')
        inlineKeyboard1 = InlineKeyboardButton('B',callback_data=f'⏭{id} {pk} B{pk_quistion}')
        inlineKeyboard2 = InlineKeyboardButton('C',callback_data=f'⏭{id} {pk} C{pk_quistion}')
        inlineKeyboard3 = InlineKeyboardButton('D',callback_data=f'⏭{id} {pk} D{pk_quistion}')
        inlineKeyboard4 = InlineKeyboardButton('Test natija olish',callback_data='✅')
        reply_markup = InlineKeyboardMarkup([
            [inlineKeyboard,inlineKeyboard1,inlineKeyboard2,inlineKeyboard3],[inlineKeyboard4]
            ])
        updater.bot.sendPhoto(chat_id, img, text, reply_markup=reply_markup)
        if len(r['list_question']) > 0:
            r['list_question'].pop(0)
            data_list = {
                "list_question":r['list_question'],
                    }
            r=requests.post(url2, json = data_list)
        else :
            updater.bot.sendMessage(chat_id, 'Bu mavzu bo\'yicha savollarimiz tugadi.') 

def resultdetail(update:Update, context:CallbackContext):
    pass


updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CallbackQueryHandler(topic, pattern="✋"))
updater.dispatcher.add_handler(CallbackQueryHandler(start1, pattern="◀back"))
updater.dispatcher.add_handler(CallbackQueryHandler(quetion, pattern="👍"))
updater.dispatcher.add_handler(CallbackQueryHandler(next_quetion, pattern='⏭'))

updater.start_polling()
updater.idle()