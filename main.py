import datetime
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from bs4 import BeautifulSoup
import requests
import os
import re

bot = telegram.Bot(token=os.environ['TOKEN'])

def eenadu(request):
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(request),bot)
        if update.callback_query:
            query = update.callback_query
            chat_id = query.message.chat_id
            message_id = query.message_id
            if re.match(r'^[a-z]',query.data):
                if query.data == 't':
                    res_text = gettithi()
                    bot.send_message(chat_id=chat_id,text=res_text)
                elif query.data == 's':
                    img_url = getimg()
                    if img_url == 'empty':
                        bot.send_message(chat_id=chat_id,text='No image found')
                    else:
                        bot.send_photo(chat_id=chat_id,photo=img_url)
                elif query.data == 'r':
                    keyboard = [[InlineKeyboardButton("Aries/Mesham", callback_data='1-Aries/Mesham'),InlineKeyboardButton("Taurus/Vrishabham", callback_data='2-Taurus/Vrishabham')],
                        [InlineKeyboardButton("Gemini/Midhunam", callback_data='3-Gemini/Midhunam'),InlineKeyboardButton("Cancer/Karkatakam", callback_data='4-Cancer/Karkatakam')],
                        [InlineKeyboardButton("Leo/Simham", callback_data='5-Leo/Simham'),InlineKeyboardButton("Virgo/Kanya", callback_data='6-Virgo/Kanya')],
                        [InlineKeyboardButton("Libra/Tula", callback_data='7-Libra/Tula'),InlineKeyboardButton("Scorpio/Vrischikam", callback_data='8-Scorpio/Vrischikam')],
                        [InlineKeyboardButton("Saggitarius/Dhanassu", callback_data='9-Saggitarius/Dhanassu'),InlineKeyboardButton("Capricon/Makaram", callback_data='10-Capricon/Makaram')],
                        [InlineKeyboardButton("Aquarius/Kumbham", callback_data='11-Aquarius/Kumbham'),InlineKeyboardButton("Pisces/Meenam", callback_data='12-Pisces/Meenam')]
                    ]                 
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    query.message.reply_text('Please choose ',reply_markup=reply_markup)
                else:
                    bot.send_message(chat_id=chat_id,text='Invalid input')
            elif re.match(r'^[1-9]',query.data):
                parse_message = query.data.split('-')
                url = 'https://www.eenadu.net/graham/inner_page/' + parse_message[0]
                reqpage = requests.get(url)
                soup = BeautifulSoup(reqpage.content,'html.parser')
                hscope = soup.find('section',class_='two-col-left-block box-shadow telugu_uni_body fullstory offset-bt1')
                res_text = '\n' + parse_message[1] + '\n' + hscope.get_text()
                bot.edit_message_text(chat_id=query.message.chat_id,message_id=message_id,text=res_text)
            else:
                bot.send_message(chat_id=chat_id,text='Unknown error')
        else:            
            chat_id = update.message.chat_id
            rec_msg = update.message.text.split(' ')
            if rec_msg[0] == '/start':
                keyboard = [[InlineKeyboardButton('Tithi',callback_data='t'),InlineKeyboardButton('Sangathi',callback_data='s'),InlineKeyboardButton('Rasi',callback_data='r')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Select Operation',reply_markup=reply_markup)
            elif rec_msg[0] == '/help':
                res_text = '\nTo use this bot, give /start\n'
                bot.send_message(chat_id=chat_id,text=res_text)
            else:
                res_text = 'Invalid command, please use /help for more details'
                bot.send_message(chat_id=chat_id,text=res_text)
    return f'ok'

def gettithi():
    url = 'https://www.eenadu.net'
    reqpage = requests.get(url)
    soup = BeautifulSoup(reqpage.content,'html.parser')
    # cont = soup.find('section',class_='two-col-left-block box-shadow telugu_uni_body fullstory offset-bt1')
    cont = soup.find('p',class_='push-fixed1')
    return cont.get_text()

def getimg():
    cur_date = f"{datetime.datetime.now():%d%m%Y}"
    url = 'https://www.eenadu.net/cartoons/apcartoon/'
    reqpage = requests.get(url)
    soup = BeautifulSoup(reqpage.content,'html.parser')
    img_url = ''
    for imgs in soup.find_all('img',class_='lazy'):
        if imgs["data-src"].find(cur_date) > 0:
            img_url = imgs["data-src"]
            break
    if img_url == '':
        return f'empty'
    else:
        return img_url