import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DBM')))

import requests
import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from twisted.internet import reactor
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
import json
from get_user_movies import MongoDB_admin




class IMDB (CrawlSpider):
    name = "Imdb titles"
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'CLOSESPIDER_PAGECOUNT': 30000,    
    'FEEDS' :  {
    'files/mis_pelis_data_.json' : {
        'format': 'json'
            }
        } ,
    #'ITEM_PIPELINES': {"scrapy.pipelines.images.ImagesPipeline": 1},
    #'IMAGES_STORE' : "files/posters",
    # 'PROXY_POOL_ENABLED' : True,
    # 'DOWNLOADER_MIDDLEWARES' : {
    # # ...
    # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
    # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
    # # ...
    }           
    

    allowed_domains = ['imdb.com']

    #url from generos_imdb.txt'
    #generar una lista de urls con los titulos de las peliculas del archivo files/titulos.txt


    # with open('files/titulos.txt','r') as f:
    #     urls = f.readlines()
    #     #start_urls = [f'https://www.google.com/search?q={url.strip()} imdb' for url in urls]
 
    with open('files/mis_pelis.json') as f:
        data = json.load(f)
        peliculas_existentes = MongoDB_admin(password='bleistift16',db='movies',collection='movies').verificar_peliculas_existentes(campo='imdb_id',pagina='imdb')
        ids = [f'https://www.imdb.com/title/{movie["imdb_id"]}' for movie in data if movie['imdb_id']]
        peliculas_nuevas = []
        for id in ids:
            if id not in peliculas_existentes:
                peliculas_nuevas.append(id)
        start_urls = peliculas_nuevas
        #start_urls = [f'https://www.imdb.com/title/{movie["imdb_id"]}/' for movie in data]




        download_delay = 0.5

    # rules = (
    #     Rule(#Detalle de películas
    #         LinkExtractor(
    #             allow =r'/title/tt\d+',
    #             restrict_xpaths=["//div[1][@class='yuRUbf']//a[1][not(contains(@href, 'fullcredits')) and contains(@href,'title/tt') and string-length(@href) <= 40]"]
    #         ), follow=True,callback='parse_titles'),
    #     )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_titles, dont_filter=True)    


    def parse_titles(self, response):
        sel  = Selector(response)

        movie_description = sel.xpath('//*[@class="sc-b5e8e7ce-0 dZsEkQ"]')
        print(len(movie_description),'________________________________________________')

        try:
            video_type = sel.xpath("//meta[@property='og:type']/@content")[0].get()
            if 'movie' in video_type or 'other' in video_type:
                video_type = 'movie'
        except:
            video_type = 'ND'

        if video_type == 'movie':
            try:
                imdb_id = sel.xpath("//head/meta[@property='og:url']/@content")[0].get()
                imdb_id = re.findall(r'tt\d+', imdb_id)[0]
            except:
                imdb_id = 'ND'  


            titulo = ''
            try:
                titulo = sel.xpath("//meta[@property='og:title']/@content").get()
                try:
                    titulo, year = titulo.split(" (")
                    year = re.findall(r'(\d+)',year)[0] 
                except:
                    year = re.findall(r'(\d+)',titulo)[0]
                
            except:
                titulo = imdb_id
                year = "ND"
            titulo = titulo.replace('Original title: ','').strip()




            '''genre'''
            try:
                genres = sel.xpath("//*[@class='ipc-chip__text' and not(contains(text(),'Back to top'))]/text()")
                genres_list = [genre.get() for genre in genres]  
            except:
                genres = "ND"

            '''rating'''
            try:
                rating = sel.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span[1]/text()")[0].get()
                
            except:
                rating = "ND"

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

            '''poster'''
            poster_url = sel.xpath("//meta[@property='og:image']/@content").getall()[0]
            name = titulo
            try:
                with open(f'files/posters/{name}.jpg', 'wb') as f:
                    f.write(requests.get(poster_url).content) 
            except:
                pass         

            yield {
                    'titulo': titulo,
                    'imdb_id': imdb_id,
                    'generos': genres_list,
                    'rating': rating,
                    'year': year,
                    'duracion': duracion,
                    'budget': budget,
                    'recaudacion_mundial': recaudacion,
                    'cast': cast_list,
                    'director': director,
                    'escritor': writer,
                    'casas_productoras': production_companies,
                    'idiomas': languages,
                    'países_de_origen': country,
                    'fecha_de_estreno': release_date,
                    'pais_estreno': pais_estreno,
                    'image_urls': poster_url,
            }

#scrapy runspider extraccion_peliculas.py -o files/titulos1.json -t json



def get_user_movies():
    process = CrawlerProcess()
    process.crawl(IMDB)
    process.start()
    with open('files/mis_pelis_data_.json') as json_file:
        data = json.load(json_file)
        film_rows = []
        for p in data:
            film_rows.append(p)
        print(len(film_rows))
    MongoDB_admin(password='bleistift16',db='movies',collection='movies',movies_usuario=False).insert_documents(film_rows) 
            
get_user_movies()






