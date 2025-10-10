import requests
from bs4 import BeautifulSoup as bs
import requests
import openpyxl
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

def GetDetailNumber(index, file_path='zzap/zzap.xlsx'):
    """
    Возвращает номер детали по индексу из Excel файла
    """
    try:
        # Загружаем workbook и активный лист
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
        
        # Проверяем, что индекс в пределах данных
        if index < 0 or index >= ws.max_row:
            return f"Ошибка: индекс {index} вне диапазона данных (0-{ws.max_row-1})"
        
        # Возвращаем номер детали из второго столбца (столбец B)
        return ws.cell(row=index+1, column=2).value
    
    except FileNotFoundError:
        return f"Ошибка: файл {file_path} не найден"
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"


def FindMissingCompanies(part_number, file_path, available_companies):
    try:
        # Загружаем workbook и активный лист
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
        
        # Столбцы: A - номер детали (1), B - название компании (2)
        part_numbers_col = 1  # столбец A
        companies_col = 2     # столбец B
        
        companies_in_table = []
        found_part = False
        start_row = None
        
        # Проходим по всем строкам
        for row in range(1, ws.max_row + 1):
            current_part = ws.cell(row=row, column=part_numbers_col).value
            
            # Если нашли нужный номер детали
            if current_part == part_number and not found_part:
                found_part = True
                start_row = row
                # Добавляем компанию из этой строки
                company = ws.cell(row=row, column=companies_col).value
                if company and str(company).strip():
                    companies_in_table.append(str(company))
            
            # Если уже нашли деталь и продолжаем сбор компаний
            elif found_part:
                # Если текущая строка пустая в столбце с номерами деталей
                if current_part is None or str(current_part).strip() == "":
                    company = ws.cell(row=row, column=companies_col).value
                    if company and str(company).strip():
                        companies_in_table.append(str(company))
                else:
                    # Нашли следующую деталь - заканчиваем поиск
                    break
        
        if not found_part:
            return f"Номер детали '{part_number}' не найден"
        
        # Находим компании, которых нет в available_companies
        missing_companies = []
        for company in companies_in_table:
            if company not in available_companies:
                missing_companies.append(company)
        
        return missing_companies
        
    except FileNotFoundError:
        return f"Ошибка: файл {file_path} не найден"
    except Exception as e:
        return f"Ошибка: {e}"

#   https://www.zzap.ru/public/search.aspx#rawdata=4343060071&codes_addr=1.-1&delivery_days=0
url = 'https://www.zzap.ru/'

detail_number = GetDetailNumber(0)
details_name = []
prices = []
phone_number = []

detail_params_list = [details_name, prices, phone_number]

availability_of_the_next_page = True

#new_url = f"{url}/{catalog_name[catalog_name_cnt]}/?page={page_num}"
new_url = f"{url}/public/search.aspx#rawdata={detail_number}&codes_man=-2&codes_addr=1.-1&delivery_days=0;0.5;1"

service = Service(executable_path='./geckodriver.exe')
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

driver.get(new_url)
while(availability_of_the_next_page):

    # Получаем HTML-код страницы
    page = driver.page_source

    soup = bs(page, "html.parser")

    details_names_tmp = soup.find_all("a", class_="f14b alink")  # извлекаем название 
    for element in details_names_tmp:
        details_name.append(element.text)

    prices_tmp = soup.find_all("span", class_="dxeBase_ZZapAqua f14b dx-nowrap")  # извлекаем цену 
    for element in prices_tmp:
        prices.append(element.text)

    phone_number_tmp = soup.find_all("span", class_="f11b")  # извлекаем телефон 
    for element in phone_number_tmp:
        phone_number.append(element.text)
    

    aaa = FindMissingCompanies(detail_number, 'zzap/details.xlsx', details_name)






driver.quit()