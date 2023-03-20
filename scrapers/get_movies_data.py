import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DBM')))

import requests
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import re
from datetime import datetime
from datetime import timedelta
import random

#from get_user_movies import MongoDB_admin




class IMDB (CrawlSpider):
    name = "Imdb titles"
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'CLOSESPIDER_PAGECOUNT': 30000,    
    'FEEDS' :  {
    'files/mis_pelis_data.json' : {
        'format': 'json'
            }
        }        
    }

    allowed_domains = ['imdb.com']

    #url from generos_imdb.txt'
    #generar una lista de urls con los titulos de las peliculas del archivo files/titulos.txt


    with open('files/titulos.txt','r') as f:
        urls = f.readlines()
        start_urls = [f'https://www.google.com/search?q={url.strip()} imdb' for url in urls]
 
    
    download_delay = 3

    rules = (
        Rule(#Detalle de películas
            LinkExtractor(
                allow =r'/title/tt\d+',
                restrict_xpaths=["//div[1][@class='yuRUbf']//a[1][not(contains(@href, 'fullcredits')) and contains(@href,'title/tt') and string-length(@href) <= 40]"]
            ), follow=True,callback='parse_titles'),
        )
    
    def parse_titles(self, response):
        sel  = Selector(response)

        movie_description = sel.xpath('//*[@class="sc-b5e8e7ce-0 dZsEkQ"]')
        print(len(movie_description),'________________________________________________')
        

        titulo = ''
        try:
            titulo = sel.xpath('//*[@data-testid="hero-title-block__original-title"]/text()')[0].get()
            
        except:
            try:
                titulo = sel.xpath('//*[@data-testid="hero-title-block__title"]/text()')[0].get()
            except:
                "poner el titulo de la url"
                titulo = response.url.split('/')[-2]
        titulo = titulo.replace('Original title: ','').strip()
            
        '''genre'''
        try:
            genres = sel.xpath("//*[@class='ipc-chip__text' and not(contains(text(),'Back to top'))]/text()")
            genres_list = [genre.get() for genre in genres]  
        except:
            genres = "ND"

        '''rating'''
        try:
            rating = sel.xpath("//*[@class='sc-e457ee34-1 gvYTvP']/text()")[0].get()
            
        except:
            rating = "ND"

        '''year'''
        try:
            year = sel.xpath("//ul[@data-testid='hero-title-block__metadata']//span/text()")[0].get()
            
        except:
            year = "ND"


        '''durcion'''
        try:
            
            duracion = sel.xpath("//li[@data-testid='title-techspec_runtime']/div/text()").getall()
            duracion = ''.join(duracion)
            duracion = timedelta(hours=int(duracion.split()[0]), minutes=int(duracion.split()[2]))
            duracion = duracion.__str__().split(':')[:-1]
            duracion = ':'.join(duracion)
        except:
             duracion = "ND"


        '''budget'''
        try:
            budget = sel.xpath("//li[@data-testid='title-boxoffice-budget']/div//text()")[0].get()
        except:
            budget = "ND"


        '''recaudacion'''
        try:
            recaudacion = sel.xpath("//li[@data-testid='title-boxoffice-cumulativeworldwidegross']/div//text()")[0].get()
        except:
            recaudacion = "ND"


        '''cast'''
        try:
            cast = sel.xpath("//*[@data-testid='title-cast-item__actor']/text()")
            cast_list = [actor.get() for actor in cast]
        except:
            cast_list = "ND"

        '''director'''
        director = ''
        try:
            top_credits_container = sel.xpath("//*[@data-testid='title-pc-principal-credit']")
            for index, credit in enumerate(top_credits_container):
                texts = credit.xpath(".//text()").getall()
                if "Director" in texts or "Directors" in texts:
                    director = credit.xpath("div/ul/li/a/text()").getall()
                    break
        except Exception as e:
            director = "ND"

        '''escritores'''
        writer = ''
        try:
            top_credits_container = sel.xpath("//*[@data-testid='title-pc-principal-credit']")
            for index, credit in enumerate(top_credits_container):
                texts = credit.xpath(".//text()").getall()
                if "Writer" in texts or "Writers" in texts:
                    writer = credit.xpath("div/ul/li/a/text()").getall()
                    break
        except Exception as e:
            writer = "ND"

        '''production comopanies'''
        production_companies = ''
        try:
            production_companies = sel.xpath("//*[@data-testid='title-details-companies']//li/a/text()").getall()
        except:
            production_companies = "ND"

        '''languages'''
        languages = ''
        try:
            languages = sel.xpath("//*[@data-testid='title-details-languages']//li/a/text()").getall()
        except:
            languages = "ND"        

        '''country'''
        country = ''
        try:
            country = sel.xpath("//*[@data-testid='title-details-origin']//li/a/text()").getall()
        except:
            country = "ND"

        '''release date'''
        release_date = ''
        try:
            release_date_country_original = sel.xpath("//*[@data-testid='title-details-releasedate']//li/a/text()")[0].get()
            release_date_country = release_date_country_original.split(" ")
            release_date = release_date_country[1] + " " + release_date_country[0] + " " + release_date_country[2]
            release_date = datetime.strptime(release_date, "%d, %B %Y")
            release_date = release_date.strftime("%d-%m-%Y")         

            regex_pais = r"\((.*?)\)"
            match = re.search(regex_pais, release_date_country_original)
            pais_estreno = match.group(1)
            

        except Exception as e:
            release_date = "ND"
            pais_estreno = "ND"


        yield {
                'titulo': titulo,
                'generos': genres_list,
                'rating': rating,
                'año': year,
                'duracion': duracion,
                'budget': budget,
                'recaudacion_mundial': recaudacion,
                'cast': cast_list,
                'director': director,
                'escritor': writer,
                'casas_productoras': production_companies,
                'idiomas': languages,
                'países de origen': country,
                'fecha_de_estreno': release_date,
                'pais_estreno': pais_estreno
        }

#scrapy runspider extraccion_peliculas.py -o files/titulos1.json -t json



def get_user_movies():
    process = CrawlerProcess()
    process.crawl(IMDB)
    process.start()



get_user_movies()






# watched_movies = MongoDB_admin(password='bleistift16',db='movies',collection='watched',usuario ='chemivan').get_documents()
# for movie in watched_movies :
#     #añadir titulo. año y rating a un .txt
#     with open('files/titulos.txt','a') as f:
#         f.write(movie['titulo']+' '+movie['año']+'\n')
        
       