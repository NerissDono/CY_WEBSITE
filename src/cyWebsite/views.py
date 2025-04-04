from django.shortcuts import render
from django.db.models import Q
from objConnecte.models import ObjConnecte, Type 
from news.models import Article, Category, Author
import json
import urllib.request
import requests

def fetch_weather():
    #api_key = "LhTqBxJAtocyRmui"
    api_key="fcedc13048dfa3741250c40742cb18cc"
    lat=49.0588
    lon=2.19113
    city_name = "Saint-Quentin"
    #url = "https://my.meteoblue.com/packages/basic-1h_basic-day?apikey=LhTqBxJAtocyRmui&lat=49.0588&lon=2.19113&asl=67&format=json"
    source =urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q=batman&appid=fcedc13048dfa3741250c40742cb18cc&units=metric').read()
    list_of_data= json.loads(source)   
    print(list_of_data)
    data = {
    "country_code": str(list_of_data['sys']['country']),
    "coordinate": str(list_of_data['coord']['lon']) + ' ' 
                  + str(list_of_data['coord']['lat']),
    "temp": str(list_of_data['main']['temp']),
    "pressure": str(list_of_data['main']['pressure']),
    "humidity": str(list_of_data['main']['humidity']),
    "description": str(list_of_data['weather'][0]['description']),
    "icon": list_of_data['weather'][0]['icon'],
    "city": "StarCity",
    }
    return data

def index(request):
    weather_data = fetch_weather()
    list=[1,2,3]
    return render(request, 'cyWebsite/index.html', {'list': list
                                                    , 'weather_data': weather_data})