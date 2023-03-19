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

#from get_user_movies import MongoDB_admin




class IMDB (CrawlSpider):
    name = "Imdb titles"
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'CLOSESPIDER_PAGECOUNT': 30000         
    }

    allowed_domains = ['imdb.com']

    #url from generos_imdb.txt'
    #generar una lista de urls con los titulos de las peliculas del archivo files/titulos.txt


    with open('files/titulos1.txt','r') as f:
        urls = f.readlines()
        start_urls = [f'https://www.google.com/search?q={url.strip()} imdb' for url in urls]
 
    download_delay = 1

    rules = (
        Rule(#Detalle de películas
            LinkExtractor(
                allow =r'/title/tt\d+',
                restrict_xpaths=["//div[1][@class='yuRUbf']//a[1][not(contains(@href, 'fullcredits')) and contains(@href,'title/tt') and string-length(@href) <= 40]"]
            ), follow=True,callback='parse_titles'),
        )
    
    
    

    def parse_titles(self, response):

    
        sel  = Selector(response)
        titulo = ''
        try:
            titulo = sel.xpath("//div[contains(@data-testid,'original-title')]/text()")[0].get()
            
        except:
            titulo = sel.xpath("//h1[contains(@data-testid,'title-block__title')]/text()")[0].get()
            
        
        print(titulo,"_________________________________________________________________________________________")
    #     #print(titulo)
    #     #if titulo not in df.values:

    #     '''Titulo'''
        
        

    #     '''genre'''
    #     try:
    #         genres = sel.xpath("//*[@class='ipc-chip__text']/text()")
    #         for genero in genres:
    #             pass
                
    #     except:
    #         genres = "ND"

    #     '''rating'''
    #     try:
    #         rating = sel.xpath("//*[@class='sc-7ab21ed2-1 jGRxWM']/text()")[1].get()
            
    #     except:
    #         rating = "ND"



    #     '''year'''
    #     try:
    #         year = sel.xpath("//*[@class='sc-8c396aa2-2 itZqyK']/text()")[0].get()
            
    #     except:
    #         year = "ND"


    #     '''durcion'''
    #     try:
            
    #         duracion = sel.xpath("//*[@class='sc-80d4314-2 iJtmbR']/ul/li[3]/text()").getall()
    #         if duracion == []:
    #             duracion = sel.xpath("//*[@class='sc-80d4314-2 iJtmbR']/ul/li[2]/text()").getall()
    #         duracion = ''.join(duracion)
    #     except:
    #         duracion = "ND"


    #     '''estrenada'''
    #     try:
    #         estreno = sel.xpath("//*[@data-testid='tm-box-up-date']/text()")[0].get()
    #     except:
    #        estreno = "ND"


    #     '''director'''
    #         #//*[@class='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base'][1] me va a dar el director o guión
    #     posibles_contenedores = sel.xpath("//*[@class='ipc-metadata-list__item']")
    #     director_count = 0
    #     for i in range(len(posibles_contenedores)):
    #         direccion = posibles_contenedores[i].xpath('.//span/text()').get()
    #         if direccion =="Director":
    #             director_count+=1
    #             if director_count ==3:
    #                 directores_contenedor = sel.xpath("//*[@class='ipc-metadata-list__item']")[i]
    #                 directores = directores_contenedor.xpath(".//div/ul/li/a/text()")
    #                 for director in directores:
    #                     pass
    #         continue

    #     '''plot'''
        
    #     plot_ = sel.xpath("//*[@class='sc-132205f7-0 bJEfgD']/div/div/div/text()")
    #     print(plot_,'_______________________________________________________________________')

    #     '''reparto'''
    #     try:
    #         reparto = sel.xpath("//*[@class='ipc-metadata-list-item__icon-link']/@href").getall()
    #         posibles_links_de_reparto = re.findall('(/title/tt\d{7,11}/fullcredits/\?ref_=tt_cl_sm)',''.join(reparto))
    #         link_reparto= 'https://www.imdb.com/'+posibles_links_de_reparto[0]
    #         r = requests.get(link_reparto)
    #         soup = BeautifulSoup(r.text, 'html.parser')
    #         writing = soup.find_all('table', attrs={'class':'simpleTable simpleCreditsTable'})
    #         writers = writing[1].find_all('a')
    #         credit_papel = writing[1].find_all('td',attrs={'class':'credit'})
    #         writing_credits = {}
    #         c =0	
    #         for writer in writers:
    #             writing_credits[credit_papel[c].text.strip().replace('(','').replace(')','').replace('&','')] = writer.text.strip()
    #             c+=1
    #         print(writing_credits)
    #     except:
    #         guide = "ND"
                
    #     '''budget'''
    #     try:
    #         budget = sel.xpath("//*[@class='ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB']/div/ul/li/span/text()")[0].get()
    #     except:
    #         budget = "ND"


    #     '''recaudacion'''
    #     try:
    #         recaudacion = sel.xpath("//*[@class='ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB']/div/ul/li/span/text()")[4].get()
    #     except:
    #         recaudacion = "ND"

    #     #
    #     '''cast'''
    #     try:
    #         cast = sel.xpath("//*[@data-testid='title-cast-item__actor']/text()")
    #         for actor in cast:
    #             pass
    #     except:
    #        acto = "ND"

    #     '''personajes'''
    #     try:
    #         chars = sel.xpath("//*[@data-testid='cast-item-characters-link']/span/text()")
    #         for char in chars:
    #             pass
    #     except:
    #         chars = "ND"

    # def parse_cast(self, response):pass


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
        
       
# with open('files/titulos.txt','r') as f:
#     urls = f.readlines()
#     for url in urls:
#         print(url)