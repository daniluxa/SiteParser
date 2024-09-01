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

url = 'https://ozerki.ru/sankt-peterburg/catalog'
availability_of_the_next_page = True

catalog_name = ['lekarstva-ot-prostudy-i-grippa', 'preparaty-dlya-pishchevaritelnogo-trakta','preparaty-dlya-serdechno-sosudistoj-sistemy', 
                'preparaty-pri-boleznyah-nervnoj-sistemy','planirovanie_semi', 'fitopreparaty','mama_i_malysh','zdorovoe_pitanie','vitaminy-i-obmen-veshchestv',
                'preparaty-dlya-lecheniya-zabolevanij-kozhi', 'sredstva-ot-boli-vospaleniya-temperatury','ginekologicheskie-preparaty', 
                'preparaty-dlya-kostno-myshechnoj-sistemy','preparaty-dlya-mochepolovoj-sistemy','preparaty-dlya-zreniya-i-sluha','preparaty-pri-allergii',
                'preparaty-dlya-lecheniya-ehndokrinnoj-sistemy','preparaty-pri-zabolevaniyah-krovi', 'preparaty-dlya-lecheniya-infekcij',
                'onkologiya-i-immunologiya','sredstva-ot-varikoza','preparaty-pri-zabolevaniyah-legkih','preparaty-dlya-borby-s-vrednymi-privychkami','preparaty-ot-parazitov',
                'bazovaya-fitoterapiya','gomeopaticheskie-sredstva','vakciny-i-syvorotki', 'mass-market','lechebnaya-i-selektivnaya-kosmetika', 'predmety-detskoj-gigieny','predmety-uhoda-dlya-detej',
                'tovary-dlya-beremennyh-i-kormyashchih','detskoe-pitanie','detskie-igrushki', 'produkty-pitaniya-obshchego-naznacheniya','funkcionalnoe-pitanie','sportivnoe-pitanie', 
                'medicinskaya-tehnika','perevyazochnye-sredstva','diagnosticheskie-test-sistemy','sredstva-uhoda-za-bolnymi',
                'izdeliya-medicinskie','funkcionalnoe-bele','ortopedicheskie-predmety','aptechki',
                'sredstva-dlya-uhoda-za-linzami-i-ochkami','linzy-kontaktnye','okklyudery','lupy','opravy','aksessuary-dlya-optiki','ochki',
                'dermakosmetika-uhod-za-volosami','chuvstvitelnaya-kozha-i-allergiya','dermakosmetika-antivozrastnoj-uhod',
                'dermakosmetika-zashchita-ot-solnca','dermakosmetika-problemnaya-kozha','vypadenie-i-perhot',
                'dermakosmetika-uvlazhnenie-i-pitanie', 'dermakosmetika-atopiya','dermakosmetika-uhod-za-telom','dermakosmetika-ochishchenie',
                'dermakosmetika-uhod-za-licom','dermakosmetika-dlya-detej','dermakosmetika-dlya-muzhchin','solnce']

catalog_name_cnt = 0 
page_num = 1 

new_url = f"{url}/{catalog_name[catalog_name_cnt]}/?page={page_num}"

driver = webdriver.Chrome()


while(availability_of_the_next_page):
    driver.get(new_url)

    # Получаем HTML-код страницы
    page = driver.page_source

    soup = bs(page, "html.parser")

    tmp_pharm_name = soup.find_all("a", class_="AppRouterLink_link__uudGk sc-128b053f-1 pvICS product-name")  # извлекаем название 
    tmp_pharm_price = soup.find_all("div", class_="product-price__base-price")  # извлекаем цену

    for data in tmp_pharm_name:
         pharm_name.append(data.text)
         
    for data in tmp_pharm_price:
         pharm_price.append(data.text)
    ##status = soup.find("span", class_="b-pagination-vuetify-imitation__item b-pagination-vuetify-imitation__item_next b-pagination-vuetify-imitation__item_disabled")
    status = soup.find("svg", class_="sc-adb9b8f4-0 hKNQCg undefined app-icon-sprite__chevron_right-icon")
    if status != None:
        page_num += 1
        catalog_name_cnt += 1
        new_url = f"{url}/{catalog_name[catalog_name_cnt]}/?page={page_num}"
    else:
        availability_of_the_next_page = False

driver.quit()

wb = ox.load_workbook('C:\python\parsing\parsing_ozerki.xlsx')
ws = wb.worksheets[0]
ws.cell(row=1, column=9).value = "Название" 
for i, statN in enumerate(pharm_name): 
    ws.cell(row=i+2, column=9).value = statN 
ws.cell(row=1, column=10).value = "Цена" 
for i, statN in enumerate(pharm_price): 
    ws.cell(row=i+2, column=10).value = statN 
wb.save('parsing_ozerki.xlsx')