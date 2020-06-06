from django.shortcuts import render
import json
import requests
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from rest_framework.response import * 
from rest_framework.decorators import api_view
from rest_framework import status
from bs4 import BeautifulSoup
import telebot
from datetime import datetime 


bot = telebot.TeleBot('1212419724:AAHgTJvXsv5njwJxv4-S_myvZOy95LxBFVg')


@bot.message_handler(commands=['start'])
def start_message(message):
    res = 'Привет, я Бот Банк Азии:\n Вот что я умею:\n Показать курс валют - /rate \nПоказать погоду за день - /weath'
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

#Получение курс валют с сайта www.bankasia.kg
def get_and_parse():
    res = ''
    url='https://www.bankasia.kg/ru/'
    site = requests.get(url)
    site.encoding = 'utf8' 
    with open('test.txt', 'w') as output_file:
        output_file.write(site.text)
    soup = BeautifulSoup(site.text, 'lxml')
    head = soup.find('div', {'id': 'home'})
    head = head.find('tbody')
    heads = []
    heads.append('Валюта: Покупка: Продажа: НБКР:')
    k = 0
    for i in head:
       k=k+1
       heads.append(str(i).replace('<tr>','').replace('</tr>','').replace('<td>','').replace('</td>','').replace('\n','   '))
       print(k)
    for i in heads:
        res = res + i + '\n'
        print(i)
    return res

#Получение прогноза погоды за день
def get_weather():
    month = str(datetime.now().month)
    day = str(datetime.now().day)
    result= 'Погода за ' +  day  + '.' +  month + ':' +'\n'
    try:
        appid = '95ebcec99f4eacbd6d61238bbe51304b'
        city_id = '1528675'
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        k=0
        for i in data['list']:
            k=k+1
            temp = ''
            if i['main']['temp'] < 0:
                temp = '-'+str(i['main']['temp'])
            else:
                 temp = '+'+str(i['main']['temp'])
            result = result + i['dt_txt'] + ' ' + temp + ' ' + i['weather'][0]['description'] + '\n\n'
            print(result)
            if k == 6:
                break
    except Exception as e:
        print("Exception (forecast):", e)
    return str(result)

bot.polling()

   


