import requests
from bs4 import BeautifulSoup as bs
import requests
import openpyxl as ox
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Doctors_Name = []
# Doctors_Spec = []
# Doctors_Categoria  = []
# Doctors_Experience = []
# Doctors_Clinic = []
# Doctors_Address = []  


pharm_name = []
pharm_price = []

url = 'https://lekopttorg.ru/catalog/'
availability_of_the_next_page = True

catalog_name = ['lekarstva_i_profilakticheskie_sredstva/']
page_num = 1

new_url = f"{url}/{catalog_name[0]}/?by=1000%2Fpage%3D5&PAGEN_3={page_num}"

driver = webdriver.Chrome()

while(availability_of_the_next_page):
    driver.get(new_url)

    # Получаем HTML-код страницы
    page = driver.page_source

    soup = bs(page, "html.parser")

    tmp_pharm_name = soup.find_all("a", class_="product__title mb-8 title title_block")  # извлекаем название 
    tmp_pharm_price = soup.find_all("span", class_="price__regular")  # извлекаем цену

    # tmp_Doctors_Spec       = soup.find_all("div", class_="b-doctor-card__spec")  # извлекаем Специфику
    # tmp_Doctors_Categoria  = soup.find_all("div", class_="b-doctor-card__category")  # извлекаем Опыт
    # tmp_Doctors_Experience = soup.find_all("div", class_="b-doctor-card__experience-years")  # извлекаем Стаж
    # tmp_Doctors_Clinic     = soup.find_all("span", class_="b-select__trigger-main-text")  # извлекаем Больницу
    # tmp_Doctors_Address    = soup.find_all("span", class_="b-select__trigger-adit-text")  # извлекаем адрес больницы

    # for data in tmp_Doctors_Name:
    #     Doctors_Name.append(data.text)

    # for data in tmp_Doctors_Spec:
    #     data = data.text.replace('\n', '')
    #     tmp = ' '.join(data.split())
    #     Doctors_Spec.append(tmp)

    # for data in tmp_Doctors_Categoria:
    #     Doctors_Categoria.append(data.text)

    # for data in tmp_Doctors_Experience:
    #     data = data.text.replace('\n', '')
    #     tmp = ' '.join(data.split())
    #     tmp = tmp[5::]
    #     Doctors_Experience.append(tmp)

    # for data in tmp_Doctors_Clinic:
    #     data = data.text.replace('\n', '')
    #     tmp = ' '.join(data.split())
    #     Doctors_Clinic.append(tmp)
    # for data in tmp_Doctors_Address:
    #     data = data.text.replace('\n', '')
    #     tmp = ' '.join(data.split())
    #     Doctors_Address.append(tmp)

    for data in tmp_pharm_name:
         pharm_name.append(data.text)
         
    for data in tmp_pharm_price:
         pharm_price.append(data.text)

    ##status = soup.find("span", class_="b-pagination-vuetify-imitation__item b-pagination-vuetify-imitation__item_next b-pagination-vuetify-imitation__item_disabled")
    status = soup.find("div", class_="arrow__right")
    if status != None:
        page_num += 1
        new_url = f"{url}/{catalog_name[0]}/?by=1000%2Fpage%3D5&PAGEN_3={page_num}"
    else:
        availability_of_the_next_page = False

driver.quit()

wb = ox.load_workbook('F:\Education\Python parser\SiteParser\parsing.xlsx')
ws = wb.worksheets[0]
ws.cell(row=1, column=9).value = "Название" 
for i, statN in enumerate(pharm_name): 
    ws.cell(row=i+2, column=9).value = statN 
wb.save('parsing.xlsx')