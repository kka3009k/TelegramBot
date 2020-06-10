from bs4 import BeautifulSoup
from datetime import datetime 
import json
import requests
from telebot.types import *
from .models import * 
from datetime import datetime
import schedule
import time
import threading
#Получение курс валют с сайта www.bankasia.kg
def get_and_parse():
    res = ''
    url='https://www.bankasia.kg/ru/'
    site = requests.get(url)
    site.encoding = 'utf8' 
    soup = BeautifulSoup(site.text, 'lxml')
    head = soup.find('div', {'id': 'home'})
    head = head.find('tbody')
    heads = []
    heads.append('Валюта: Покупка: Продажа: НБКР:')
    for i in head:
       heads.append(str(i).replace('<tr>','').replace('</tr>','').replace('<td>','').replace('</td>','').replace('\n','   '))
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


#Возращает keyboard
def get_mark_keyboard(rows: str, vis: bool):
    keyboard = ReplyKeyboardMarkup(True,vis)
    for i in rows:
        keyboard.add(i)
    return keyboard

#Создание пользователя
def create_user(data: dict):
    print(data)
    user = UsersBot.objects.get(user_id=data.id)
    if user == None:
        print("create")
        user = UsersBot.objects.create(user_id=data.id,full_name = str(data.first_name) + ' ' + str(data.last_name),date_create=datetime.now())
        user.save()
    else:
        print("update")
        user.full_name = str(data.first_name) + ' ' + str(data.last_name)
        user.save()



##Удаление файлов
#def job():
#    print("Удаляю файлы")

#schedule.every(1).minutes.do(job)
##schedule.every().day.at("10:30").do(job)
#def polling():
#    while 1:
#        schedule.run_pending()
#        time.sleep(1)

#x = threading.Thread(target=polling)
#x.start()

###################################################
