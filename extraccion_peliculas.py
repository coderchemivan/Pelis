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


buscar_repetidos = False
archivo = input('Ingrese el nombre del archivo: ')
num_archivo = re.findall('(\d+)',archivo)
archivo = 'files/{archivo}.json'.format(archivo = archivo)
existencia_archivo = os.path.exists(archivo)
if existencia_archivo == True:
    df = pd.read_json(archivo).astype(str)
    df = df.iloc[:, 0]
    df = df.apply(lambda x: x[2:len(x)-2])
    buscar_repetidos = True
else:
    print('El archivo no existe')


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
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'CLOSESPIDER_PAGECOUNT': 30000         
    }

    allowed_domains = ['imdb.com']

    #url from generos_imdb.txt'
    urls = []
    with open('files/generos_imdb.txt','r') as f:
        urls = f.readlines()

    urls = [url.strip() for url in urls]

    start_urls = [urls[0]]

    download_delay = 1

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
        id_imdb = re.findall('/title/(tt\d+)/',''.join(links))[0]
        item.add_value('id_imdb', id_imdb)   

        if buscar_repetidos == True:
            if id_imdb in df.values:
                print('La pelicula ya existe')
                print('__________________________--','\n')
            else:
                '''Titulo'''
                try:
                    titulo = sel.xpath('//*[@hero-title-block__original-title="hero-title-block__original-title"]/text()')[0].get()
                    
                except:
                    titulo = sel.xpath('//*[@data-testid="hero-title-block__title"]/text()')[0].get()
                
                
                item.add_value('title', titulo)
                
                '''genre'''
                try:
                    genres = sel.xpath("//*[@class='ipc-chip__text']/text()")
                    for genero in genres:
                        item.add_value('genre',genero.get())
                except:
                    item.add_value('genre','ND')


                '''rating'''
                try:
                    rating = sel.xpath("//*[@class='sc-7ab21ed2-1 jGRxWM']/text()")[1].get()
                    item.add_value('rating',rating)
                except:
                    item.add_value('rating', 'ND')



                '''year'''
                try:
                    year = sel.xpath("//*[@class='sc-8c396aa2-2 itZqyK']/text()")[0].get()
                    item.add_value('year',year)
                except:
                    item.add_value('year','ND')


                '''durcion'''
                try:
                    
                    duracion = sel.xpath("//*[@class='sc-80d4314-2 iJtmbR']/ul/li[3]/text()").getall()
                    if duracion == []:
                        duracion = sel.xpath("//*[@class='sc-80d4314-2 iJtmbR']/ul/li[2]/text()").getall()
                    duracion = ''.join(duracion)
                    item.add_value('duracion',duracion)
                except:
                    item.add_value('duracion','ND')


                '''estrenada'''
                try:
                    estreno = sel.xpath("//*[@data-testid='tm-box-up-date']/text()")[0].get()
                    item.add_value('estreno',estreno)
                except:
                    item.add_value('estreno',0)
                        
                '''budget'''
                try:
                    budget = sel.xpath("//*[@class='ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB']/div/ul/li/span/text()")[0].get()
                    item.add_value('budget',budget)
                except:
                    item.add_value('budget', 'ND')


                '''recaudacion'''
                try:
                    recaudacion = sel.xpath("//*[@class='ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB']/div/ul/li/span/text()")[4].get()
                    item.add_value('boxOffice_collection',recaudacion)
                except:
                    item.add_value('boxOffice_collection', 'ND')

                #
                '''cast'''
                try:
                    cast = sel.xpath("//*[@data-testid='title-cast-item__actor']/text()")
                    for actor in cast:
                        item.add_value('cast', actor.get())
                except:
                    item.add_value('cast', 'ND')

                '''personajes'''
                try:
                    chars = sel.xpath("//*[@data-testid='cast-item-characters-link']/span/text()")
                    for char in chars:
                        item.add_value('personajes', char.get())
                except:
                    item.add_value('personajes', 'ND')
            
                yield item.load_item() 


            def parse_cast(self, response):pass





# if __name__ == '__main__':
#     process = CrawlerProcess()
#     process.crawl(Imdb)
#     process.start()

#scrapy runspider extraccion_peliculas.py -o files/titulos1.json -t json

