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
from bs4 import BeautifulSoup
import re


import pandas as pd


opts = Options()
opts.add_argument(
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36.")
driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()),options=opts)


def get_title(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    '''Titulo'''
    
    try:
        titulo = soup.find_all('h1',attrs={'class':'sc-b73cd867-0 eKrKux'})[0].text
        titulo = titulo.replace('\n','').replace('Original title:','').strip()
        return titulo
    except:
        return str(url)


def extraer_id_imdb(link):
    return re.findall('/title/(tt\d+)/',link)[0].strip()

'''Haciendo las búsqueda en google'''
for i in range(1960, 1961):
    try:
        driver.get('https://www.imdb.com/event/ev0000003/{año}/1/'.format(año=str(i)))


        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="center-3-react"]/div/div/div[1]/h3/div[1]'))

        )

        premios = driver.find_elements(By.XPATH,"//*[@class='event-widgets__award-category']")
        nominados_categoria = {}
        años_=[]
        premios_ = []
        nominados_nombre = []
        ganador = []
        for premio in premios:
            nominados_ = [nominado.get_attribute('href') 
                for nominado in premio.find_elements(By.XPATH,".//a[contains(@href, '/title/tt')]")]
            
            #eliminado links repetidos de la lista
            nominados_ = list(dict.fromkeys(nominados_))

            años_.extend([str(i) for j in range(len(nominados_))])
            premios_.extend([premio.text.upper() for j in range(len(nominados_))])
            nominados_nombre.extend([nominados_[j] for j in range(len(nominados_))])
            ganador.extend([1 if c == 0 else 0 for c in range(len(nominados_))])

            nominados_categoria['Año'] = años_
            nominados_categoria['Premio'] = premios_
            nominados_categoria['Nominado'] = nominados_nombre
            nominados_categoria['Ganador'] = ganador
        
        df = pd.DataFrame(nominados_categoria,columns=['Año','Premio','Nominado','Ganador'])
        
        print(df)
            
        print('=====================')
        #extrayendo el id del link
        df_Nominado_id = df['Nominado'].map(lambda x: extraer_id_imdb(x))
        df['Nominado'] = df['Nominado'].map(lambda x: get_title(x))
        df = pd.concat([df,df_Nominado_id],axis=1)
        #df = df.iloc[:,['Año','Premio','Nominado','Nominado','Ganador']]
        df.to_csv('files/oscares/oscar_{año}.csv'.format(año=str(i)), index=False)
    except:
        continue 
driver.quit()






    #info_peli['title'] = movie
    



