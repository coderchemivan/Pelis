from attr import attrs
import requests
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
import pandas as pd

from bs4 import BeautifulSoup
import re
import os
import json
import numpy as np




# archivo = input('Ingrese el nombre del archivo: ')
# archivo = 'files/{archivo}.json'.format(archivo = archivo)
# contador_descargas = 0
verificar_existencia_archivo = input("¿Desea verificar la existencia de un archivo? (s/n): ")
# if verificar_existencia_archivo == "s":
#     df = pd.read_json(archivo).astype(str)
#     df = df.iloc[:, 0]
#     df = df.apply(lambda x: x[2:len(x)-2])
    #print(df)



class Opinion(Item):
    id_imdb = Field()
    title = Field()
    genre = Field()
    year = Field()
    estreno = Field()
    duracion = Field()
    rating = Field()
    budget = Field()
    boxOffice_collection = Field()
    cast = Field()
    personajes = Field()
    
    


class Imdb (CrawlSpider):
    name = "Imdb titles"
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'CLOSESPIDER_PAGECOUNT': 30000         
    }

    allowed_domains = ['imdb.com']

    #url from generos_imdb.txt'
    urls = []
    with open('files/generos_imdb.txt','r') as f:
        urls = f.readlines()

    urls = [url.strip() for url in urls]

    start_urls = [urls[1]]

    def truncate(n, decimals = 0): 
        multiplier = 10 ** decimals 
        return int(n * multiplier) / multiplier
    download_delay = truncate(np.random.uniform(0.5,1),1)

    rules = (
        Rule(#Paginación de peliculas
            LinkExtractor(
                allow=r'adv_nxt'
            ), follow=True),

        
        Rule(#Detalle de películas
            LinkExtractor(
                allow =r'/title/tt\d+',
                restrict_xpaths=["//*[@class='lister-list']/div/div/h3/a"]
            ), follow=True,callback='parse_titles'),
        )
    
    
    

    def parse_titles(self, response):
        sel  = Selector(response)
        item = ItemLoader(Opinion(),sel)
 
        '''ID'''
        links = sel.xpath("//*[@class='ipc-metadata-list-item__icon-link']/@href").getall()
        id_imdb = re.findall('/title/(tt\d{7,11})/',''.join(links))[0]
        item.add_value('id_imdb', id_imdb)      
        
        if verificar_existencia_archivo == "s" and id_imdb in df.values:
            print('La película ya se encuentra en el archivo')        
        else:
            
            try:
                titulo = sel.xpath('//*[@hero-title-block__original-title="hero-title-block__original-title"]/text()')[0].get()
                
            except:
                titulo = sel.xpath('//*[@data-testid="hero-title-block__title"]/text()')[0].get()


            '''Titulo'''
            item.add_value('title', titulo)
            
            

            '''genre'''
            try:
                genres = sel.xpath("//*[@class='ipc-chip__text']/text()")
                generos = [genero.get() for genero in genres]
                for genero in genres:
                    item.add_value('genre',genero.get())
            except:
                generos = 'ND'
                item.add_value('genre','ND')


            '''rating'''
            try:
                rating = sel.xpath("//*[@class='sc-7ab21ed2-1 jGRxWM']/text()")[1].get()
                item.add_value('rating',rating)
            except:
                rating = 'ND'
                item.add_value('rating', 'ND')



            '''year'''
            try:
                year = sel.xpath("//*[@class='sc-8c396aa2-2 itZqyK']/text()")[0].get()
                item.add_value('year',year)
            except:
                year = 'ND'
                item.add_value('year','ND')


            '''durcion'''
            try:
                
                duracion = sel.xpath("//*[@class='sc-80d4314-2 iJtmbR']/ul/li[3]/text()").getall()
                if duracion == []:
                    duracion = sel.xpath("//*[@class='sc-80d4314-2 iJtmbR']/ul/li[2]/text()").getall()
                duracion = ''.join(duracion)
                item.add_value('duracion',duracion)
            except:
                duracion = 'ND'
                item.add_value('duracion','ND')


            '''estrenada'''
            try:
                estreno = sel.xpath("//*[@data-testid='tm-box-up-date']/text()")[0].get()
                item.add_value('estreno',estreno)
            except:
                estreno = 'ND'
                item.add_value('estreno',0)
                    
            '''budget'''
            try:
                budget = sel.xpath("//*[@class='ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB']/div/ul/li/span/text()")[0].get()
                item.add_value('budget',budget)
            except:
                budget = 'ND'
                item.add_value('budget', 'ND')


            '''recaudacion'''
            try:
                recaudacion = sel.xpath("//*[@class='ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB']/div/ul/li/span/text()")[4].get()
                item.add_value('boxOffice_collection',recaudacion)
            except:
                recaudacion = 'ND'
                item.add_value('boxOffice_collection', 'ND')

            '''cast'''
            try:
                cast = sel.xpath("//*[@data-testid='title-cast-item__actor']/text()")
                casts = [actor.get() for actor in cast]
                for actor in cast:
                    item.add_value('cast', actor.get())
            except:
                casts = 'ND'
                item.add_value('cast', 'ND')

            '''personajes'''
            try:
                chars = sel.xpath("//*[@data-testid='cast-item-characters-link']/span/text()")
                characters = [char.get() for char in chars]
                for char in chars:
                    item.add_value('personajes', char.get())
            except:
                characters = 'ND'
                item.add_value('personajes', 'ND')
            yield item.load_item() 



#scrapy runspider extraccion_peliculas1.0.py -o files/titulos2.json -t json








'''Esta version se puede correr directamente con el botón de correr y no requiere de la linea de comando'''
# from attr import attrs
# import requests
# from scrapy.item import Field
# from scrapy.item import Item
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.selector import Selector
# from scrapy.linkextractors import LinkExtractor
# from scrapy.loader import ItemLoader
# from scrapy.crawler import CrawlerProcess
# import pandas as pd

# from bs4 import BeautifulSoup
# import re
# import os
# import json


# archivo = input('Ingrese el nombre del archivo: ')
# archivo = 'files/{archivo}.json'.format(archivo = archivo)
# contador_descargas = 0
# verificar_existencia_archivo = input("¿Desea verificar la existencia de un archivo? (s/n): ")
# if verificar_existencia_archivo == "s":
#     df = pd.read_json(archivo).astype(str)
#     df = df.iloc[:, 0]
#     df = df.apply(lambda x: x[2:len(x)-2])
#     #print(df)

# class Opinion(Item):
#     id_imdb = Field()
#     title = Field()
#     genre = Field()
#     year = Field()
#     estreno = Field()
#     duracion = Field()
#     rating = Field()
#     budget = Field()
#     boxOffice_collection = Field()
#     cast = Field()
#     personajes = Field()
    
    


# class Imdb (CrawlSpider):
#     name = "Imdb titles"
#     custom_settings = {
#     'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
#     'CLOSESPIDER_PAGECOUNT': 30000         
#     }

#     allowed_domains = ['imdb.com']

#     #url from generos_imdb.txt'
#     urls = []
#     with open('files/generos_imdb.txt','r') as f:
#         urls = f.readlines()

#     urls = [url.strip() for url in urls]

#     start_urls = [urls[2]]

#     download_delay = 1

#     rules = (
#         Rule(#Paginación de peliculas
#             LinkExtractor(
#                 allow=r'adv_nxt'
#             ), follow=True),

        
#         Rule(#Detalle de películas
#             LinkExtractor(
#                 allow =r'/title/tt\d+',
#                 restrict_xpaths=["//*[@class='lister-list']/div/div/h3/a"]
#             ), follow=True,callback='parse_titles'),
#         )
    
    
    

#     def parse_titles(self, response):
#         sel  = Selector(response)
#         item = ItemLoader(Opinion(),sel)
 
#         '''ID'''
#         links = sel.xpath("//*[@class='ipc-metadata-list-item__icon-link']/@href").getall()
#         id_imdb = re.findall('/title/(tt\d{7,11})/',''.join(links))[0]
#         item.add_value('id_imdb', id_imdb)      
        
#         if verificar_existencia_archivo == "s" and id_imdb in df.values:
#             print('La película ya se encuentra en el archivo')        
#         else:
            
#             try:
#                 titulo = sel.xpath('//*[@hero-title-block__original-title="hero-title-block__original-title"]/text()')[0].get()
                
#             except:
#                 titulo = sel.xpath('//*[@data-testid="hero-title-block__title"]/text()')[0].get()


#             '''Titulo'''
#             #item.add_value('title', titulo)
            
            

#             '''genre'''
#             try:
#                 genres = sel.xpath("//*[@class='ipc-chip__text']/text()")
#                 generos = [genero.get() for genero in genres]
#             #    for genero in genres:
#             #        item.add_value('genre',genero.get())
#             except:
#                 generos = 'ND'
#                 item.add_value('genre','ND')


#             '''rating'''
#             try:
#                 rating = sel.xpath("//*[@class='sc-7ab21ed2-1 jGRxWM']/text()")[1].get()
#             #    item.add_value('rating',rating)
#             except:
#                 rating = 'ND'
#             #    item.add_value('rating', 'ND')



#             '''year'''
#             try:
#                 year = sel.xpath("//*[@class='sc-8c396aa2-2 itZqyK']/text()")[0].get()
#             #    item.add_value('year',year)
#             except:
#                 year = 'ND'
#             #    item.add_value('year','ND')


#             '''durcion'''
#             try:
                
#                 duracion = sel.xpath("//*[@class='sc-80d4314-2 iJtmbR']/ul/li[3]/text()").getall()
#                 if duracion == []:
#                     duracion = sel.xpath("//*[@class='sc-80d4314-2 iJtmbR']/ul/li[2]/text()").getall()
#                 duracion = ''.join(duracion)
#             #    item.add_value('duracion',duracion)
#             except:
#                 duracion = 'ND'
#             #    item.add_value('duracion','ND')


#             '''estrenada'''
#             try:
#                 estreno = sel.xpath("//*[@data-testid='tm-box-up-date']/text()")[0].get()
#             #    item.add_value('estreno',estreno)
#             except:
#                 estreno = 'ND'
#             #    item.add_value('estreno',0)
                    
#             '''budget'''
#             try:
#                 budget = sel.xpath("//*[@class='ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB']/div/ul/li/span/text()")[0].get()
#             #    item.add_value('budget',budget)
#             except:
#                 budget = 'ND'
#             #    item.add_value('budget', 'ND')


#             '''recaudacion'''
#             try:
#                 recaudacion = sel.xpath("//*[@class='ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB']/div/ul/li/span/text()")[4].get()
#             #    item.add_value('boxOffice_collection',recaudacion)
#             except:
#                 recaudacion = 'ND'
#             #    item.add_value('boxOffice_collection', 'ND')

#             #
#             '''cast'''
#             try:
#                 cast = sel.xpath("//*[@data-testid='title-cast-item__actor']/text()")
#                 casts = [actor.get() for actor in cast]
#             #    for actor in cast:
#             #        item.add_value('cast', actor.get())
#             except:
#                 casts = 'ND'
#             #    item.add_value('cast', 'ND')

#             '''personajes'''
#             try:
#                 chars = sel.xpath("//*[@data-testid='cast-item-characters-link']/span/text()")
#                 characters = [char.get() for char in chars]
#             #    for char in chars:
#             #        item.add_value('personajes', char.get())
#             except:
#                 characters = 'ND'
#             #    item.add_value('personajes', 'ND')

#             items = {
#                 'id_imdb':id_imdb,
#                 'title':titulo,
#                 'genre':generos,
#                 'rating':rating,
#                 'year':year,
#                 'duracion':duracion,
#                 'estreno':estreno,
#                 'budget':budget,
#                 'boxOffice_collection':recaudacion,
#                 'cast':casts,
#                 'personajes':characters
#             }
#             #agregando el diccionario al archivo json
#             # 1. Read file contents
#             with open(archivo, "r") as file:
#                 data = json.load(file)
#             # 2. Update json object
#             data.append(items)
#             # 3. Write json file
#             with open(archivo, "w") as file:
#                 json.dump(data, file)

            
#             #print('Descargando película: ',contador_descargas)
#             #contador_descargas += 1
#             #yield item.load_item() 

# if __name__ == '__main__':
#     process = CrawlerProcess()
#     process.crawl(Imdb)
#     process.start()

# #scrapy runspider extraccion_peliculas.py -o files/titulos2.json -t json

