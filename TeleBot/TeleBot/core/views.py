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


bot = telebot.TeleBot('1212419724:AAHgTJvXsv5njwJxv4-S_myvZOy95LxBFVg')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

bot.polling()


@api_view(['GET', 'POST'])
def send_bot_message(request):
    if request.method == 'GET':
        get_and_parse()
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


def get_and_parse():
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
        print(i)

   


