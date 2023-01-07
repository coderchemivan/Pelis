from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd
import json

class ExtraccionLinksPeliculas():
    def __init__ (self,archivo_links_generos):
        self.archivo_links_generos = archivo_links_generos
        self.links_generos = self.leer_links_generos()
          
    def leer_links_generos(self):
        with open(self.archivo_links_generos, 'r') as archivo:
            links_generos = archivo.readlines()
        return links_generos[23:24]
    
    def extraer_links_peliculas(self):
        links_peliculas = []
        m = 1   
        for link in self.links_generos:
            print('Género '+ str(m))
            links_peliculas.append(self.extraer_links_peliculas_por_genero(link))
            m += 1
        return links_peliculas
        
    def extraer_links_peliculas_por_genero(self,link):
        links_peliculas = []
        pelicula_genero = {}
        genero_ =[]
        pagina = requests.get(link)
        soup = BeautifulSoup(pagina.text, 'lxml')
        links = soup.find_all('h3', class_='lister-item-header')
        #genero = re.findall('https://www.imdb.com//search/title?genres=(.+)&title_type=feature&explore=genres',link)
        #links = soup.find_all('a', href=re.compile('/title/tt\d+'))
        for link in links:
            #genero_.append(genero)
            links_peliculas.append(link.find('a').get('href').replace('title','').replace('/',''))
        #print(links_peliculas)
        link_pag_seiguiente = soup.find_all('div', class_='desc')
        link_pag_seiguiente = link_pag_seiguiente[0].find('a').get('href')

        c = 0
        while c<=40 or link_pag_seiguiente == None:
            r = requests.get('https://www.imdb.com'+link_pag_seiguiente)
            soup = BeautifulSoup(r.text, 'lxml')
            links = soup.find_all('h3', class_='lister-item-header')
            for link in links:
                #genero_.append(genero)
                links_peliculas.append(link.find('a').get('href').replace('title','').replace('/',''))
                #with open(r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\Pelis\extraccion_links_peliculas\titles.json', "r") as file:
            c += 1
            link_pag_seiguiente = soup.find_all('div', class_='desc')
            
            link_pag_seiguiente = link_pag_seiguiente[0].find_all('a')
            if len(link_pag_seiguiente) > 1:
                link_pag_seiguiente = link_pag_seiguiente[1].get('href')
                print(c,link_pag_seiguiente)
            else:
                break
        #pelicula_genero['genero'] = genero_
        pelicula_genero['link'] = links_peliculas
        #registrando pelicula_genero en un json que va a se usado para la extraccion de datos
        #agregando el diccionario al archivo json
        # 1. Read file contents

        return links_peliculas

        

c = ExtraccionLinksPeliculas(r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\Pelis\files\generos_imdb.txt')
lista_link_total =  c.extraer_links_peliculas()

lista_link_total = [item for sublist in lista_link_total for item in sublist]

"list n 0 con mumpy"

lista_ceros = list(np.zeros(len(lista_link_total)))

#crear un datafrmae con los links y los ceros
df = pd.DataFrame({'links':lista_link_total, 'Scraped':lista_ceros})

df.to_csv(r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\Pelis\files\links_peliculas3.csv', index = False)
