import requests
from bs4 import BeautifulSoup
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config import URL


url = 'https://www.speedrent.ru/venue/2241775?eventtype=delovaja_vstrecha'
features = {
    "Кондиционер": "missing",
    "Микрофон": "missing",
    "Проектор": "missing",
    "Светомузыка": "missing",
    "Акустическая система": "missing",
    "WI-FI": "missing",
    "ТВ-панель": "missing",
    "Гардероб": "missing",
    "Сцена": "missing"
}


response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
main_info = soup.find('div', class_='table_options')
main_info = main_info.text

for key in features.keys():
    if key in main_info:
        features[key] = 'present'

print(features)
#print(main_info)



