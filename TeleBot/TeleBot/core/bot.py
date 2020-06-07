from bs4 import BeautifulSoup
from datetime import datetime 
import json
import requests


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
