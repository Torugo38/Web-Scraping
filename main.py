from bs4 import BeautifulSoup
import pandas
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


DRIVER_PATH = 'C:/Users/Victor Hugo/PycharmProjects/projetobluetape/venv/Scripts/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")


driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

excel = pandas.read_excel('Parâmetros.xlsx')

headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

palavras = excel['palavras_chave'].tolist()
urls = excel['urls'].tolist()
result_list = []
datatoexcel = pandas.ExcelWriter('Parâmetros.xlsx')


for url in urls:
  palavra_result = []
  if not pandas.isna(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    for palavra in palavras:
        result_lower = soup.find_all(string=re.compile(palavra))
        result_title = soup.find_all(string=re.compile(palavra.capitalize()))
        result_upper = soup.find_all(string=re.compile(palavra.upper()))
        result = result_upper + result_title + result_lower
        if len(result) != 0:
             palavra_result.append(palavra)
    result_list.append(' ,'.join(palavra_result))

driver.quit()
excel['Result'] = pandas.Series(result_list)
excel.to_excel(datatoexcel)
datatoexcel.save()