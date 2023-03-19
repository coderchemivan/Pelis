from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep



driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
'''Haciendo las búsqueda en google'''
driver.get('https://www.imdb.com/event/ev0000003/2020/1/')


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="center-3-react"]/div/div/div[1]/h3/div[1]'))

)

premios = driver.find_elements(By.XPATH,"//*[@class='event-widgets__award-category']")[0:24]
nombre_premios = driver.find_elements(By.XPATH,"//*[@class='event-widgets__award-category-name']")
nominaos_categoria = {}

print(len(premios))
c = 0
for premio in premios:
    #categoria_name = premio.find_element(By.XPATH,".//div").text
    nominados = premio.find_elements(By.XPATH,".//div/div/div/div/div/div[1]")
    nominados_ = []
    for nominado in nominados:
        print(nominado.text)
        nominados_.append(nominado.text)
    nominaos_categoria[nombre_premios[c].text] = nominados_
    c+=1    
    print('=====================')
print(nominaos_categoria)
        



