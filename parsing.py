import requests
from bs4 import BeautifulSoup
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config import URL
import re 

#Получение всехх страниц сайта 
def all_urls(url):
    urls = []
    for i in range (1, 2):
        urls.append(url+str(i))
    return urls

#Получение всех ссылок на все площадки, представленные на сайте 
def extract_links(url):
    sites_links = set()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") 
    links = soup.find_all('a', href=True)  
    for link in links: 
        href = link['href'] 
        if "/venue/" in href and "/booking?" not in href and "/add" not in href:
            sites_links.add('https://www.speedrent.ru' + href)   

    return sites_links  

#Получение адресов 
async def place(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    adr = soup.find('div', class_='address') 
    for address in adr:
        clean_address = address.text.strip().replace('\n', ' ')
        clean_address = re.sub(r'\s+', ' ', clean_address)
    return clean_address

#Получение вместитетьльности (максимальное кол-во человек) и метрожа 
async def capacity(link): #Вместительность 
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    capacity = soup.find_all('div', class_='option-label')
    square = soup.find_all('div', class_='option-label')
    for cap in capacity:
        if "человек" in cap.text.strip():
            clean_cap = cap.text.strip().replace('\n', ' ')
            clean_cap = re.sub(r'\s+', ' ', clean_cap)
    for sqr in square:
        if "м2" in sqr.text:
            squares = sqr.text.strip() 
            squares = squares.replace('/n', ' ').strip()
            squares = re.sub(r'\s+', ' ', squares)

    return clean_cap, squares
#Получение названия площадки 
async def names(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    name_d = soup.find('div', class_='content-main')
    if name_d:
        name = name_d.find('h1')
        name = name.text.strip().replace('Арендовать ', '')
        return name

async def services(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.txt, "html.parser")
    main_info = soup.find('div', class_='table_options')
    
#Запуск парсера 
async def parse_all_links(res):
    all_information=[]
    tasks=[]
    for link in res:
        tasks.append(place(link))
        tasks.append(capacity(link))
        tasks.append(names(link))
        
    
    results = await asyncio.gather(*tasks)
    
    for i in range(0, len(results), 3):
        address, (capacitys, square), name = results[i], results[i+1], results[i+2]
        all_information.append((address, capacitys, square, name))
    
    return all_information

all_address=[]
all_capacity=[]
all_square=[]
all_name=[]

if __name__ == "__main__":
    url = URL
    urls = all_urls(url)
    res = []
    for link in urls:
        link_to_the_sites = extract_links(link)
        for i in link_to_the_sites:
            res.append(i)

    results = asyncio.run(parse_all_links(res))

    for data in results:
        address, capacity, square, name = data
        all_address.append(address)
        all_capacity.append(capacity)
        all_square.append(square)
        all_name.append(name)
    


    
    c=0
    for i in all_square:
        print(i)
        c+=1
    print(c)