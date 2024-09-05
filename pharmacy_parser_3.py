import string
import requests
from bs4 import BeautifulSoup as bs
import requests
import openpyxl as ox
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

pharm_name = []
pharm_price = []

url = 'https://www.acmespb.ru/pharma/oz17'
availability_of_the_next_page = True

catalog_name = ['a']

catalog_name_cnt = 0
page_num = 1
last_page = -1

new_url = f"{url}?page_code={catalog_name[catalog_name_cnt]}"

service = Service(executable_path='./geckodriver.exe')
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

while(availability_of_the_next_page):
    driver.get(new_url)

    # Получаем HTML-код страницы
    page = driver.page_source

    soup = bs(page, "html.parser")

    tmp_pharm_name = soup.find_all("div", class_="cell name")  # извлекаем название 
    tmp_pharm_price = soup.find_all("div", class_="cell pricefull")  # извлекаем цену

    for data in tmp_pharm_name:
        data = data.text.replace('\n', '')
        tmp = ' '.join(data.split())
        pharm_name.append(tmp)
         
    for data in tmp_pharm_price:
        data = data.text.replace('\n', '')
        tmp = ' '.join(data.split())
        pharm_price.append(tmp)

    if page_num < last_page:
        page_num += 1
        new_url = f"{url}"
    elif catalog_name_cnt <= len(catalog_name):
        catalog_name_cnt += 1
        page_num = 1
        last_page = -1
        new_url = f"{url}"
    else:
        availability_of_the_next_page = False
driver.quit()

wb = ox.load_workbook('parsing_acm.xlsx')
ws = wb.worksheets[0]
#ws.delete_cols(9)
ws.cell(row=1, column=9).value = "Название" 
for i, statN in enumerate(pharm_name): 
    ws.cell(row=i+2, column=9).value = statN
ws.cell(row=1, column=10).value = "Цена" 
for i, statN in enumerate(pharm_price): 
    ws.cell(row=i+2, column=10).value = statN 
wb.save('parsing_acm.xlsx')
