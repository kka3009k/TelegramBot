from django.shortcuts import render
import json
import requests
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from rest_framework.response import * 
from rest_framework.decorators import api_view
from rest_framework import status
from telebot import *
from TeleBot.core.bot import *
from .models import * 


bot = TeleBot('1212419724:AAHgTJvXsv5njwJxv4-S_myvZOy95LxBFVg')

#Проверка авторизации
def auth(func):
    def wrapper(message):
        user = UsersBot.objects.get(user_id=message.from_user.id)
        if user == None or user.is_active == False:
            return bot.send_message(message.chat.id, 'Нажмите /start или попросите доступ у администратора!')
        else:
            return func(message)
    return wrapper

@bot.message_handler(commands=['start'])
def start_message(message):
    res = 'Привет {0}, я Бот Банк Азии:\nВот что я умею:\nПоказать курс валют - /rate \nПоказать погоду за день - /weath'.format(message.chat.first_name)
    row = []
    row.append('Конвертер валют')
    bot.send_message(message.chat.id, res,reply_markup=get_mark_keyboard(row,True))
    try:
        create_user(message.from_user)
    except ex:
        start = ['/start']
        print(str(ex))
        bot.send_message(message.chat.id, 'Пожалуйста нажми на кнопку',reply_markup=get_mark_keyboard(row,True))



@bot.message_handler(commands=['rate'])
@auth
def get_valute_message(message):
    bot.send_message(message.chat.id, 'Загружаю....')
    res = get_and_parse()
    bot.send_message(message.chat.id, 'Вот держи:')
    bot.send_message(message.chat.id, res)


@bot.message_handler(commands=['weath'])
def get_weather_message(message): 
    bot.send_message(message.chat.id, 'Загружаю....')
    weath = get_weather()
    
    bot.send_message(message.chat.id, weath)


@bot.message_handler(regexp="Конвертер")
def handle_message(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Сомы в ->  💲", callback_data="dollars")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, 'Выбери конвертацию:',reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_message(call):      
    if call.data == "dollars":
        bot.send_message(call.message.chat.id, 'Введите сумму начиная с $:')

   

@bot.message_handler(content_types=["text"])
def handle_message(message):
    convert_valute = message.text.find("$")
    print(convert_valute)
    if convert_valute == 0:
        bot.send_message(message.chat.id, str(float(message.text.replace("$","").strip())*2))
    print("dsd")


        
    
    



@api_view(['GET', 'POST'])
def send_bot_message(request):
    if request.method == 'GET':
        
        return Response(data="tests",status=status.HTTP_201_CREATED)
    elif request.method == 'POST':
        data = request.data
        print(data)
        try :
            id_odb = create_contract_in_odb(data)
            client = CreditRequestInfo.objects.get(id=data['id'])
            client.credit_contract_id_odb = id_odb
            client.save()
            return Response(data="OK", status=status.HTTP_201_CREATED)
        except Exception as ex:
           return Response(data=str(ex), status=status.HTTP_400_BAD_REQUEST)



def bot_polling():
    bot.polling(none_stop=True, interval=0)

x = threading.Thread(target=bot_polling)
x.start()
   


