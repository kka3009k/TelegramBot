from django.shortcuts import render
import json
import requests
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from rest_framework.response import * 
from rest_framework.decorators import api_view
from rest_framework import status
import telebot
from TeleBot.core.bot import *


bot = telebot.TeleBot('1212419724:AAHgTJvXsv5njwJxv4-S_myvZOy95LxBFVg')


@bot.message_handler(commands=['start'])
def start_message(message):
    res = 'Привет {0}, я Бот Банк Азии:\nВот что я умею:\nПоказать курс валют - /rate \nПоказать погоду за день - /weath'.format(message.chat.first_name)
    bot.send_message(message.chat.id, res)


@bot.message_handler(commands=['rate'])
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


bot.polling()

   


