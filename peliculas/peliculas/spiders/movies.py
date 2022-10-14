from turtle import delay
import scrapy
from scrapy.selector import Selector
import re
import pandas as pd



class AbrirJsonFiles():
    def __init__(self, filename):
        self.filename = filename
    
    def read_json(self):
        with open(r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\Pelis\files/{file}.json'.format(file = self.filename), 
        encoding='utf-8') as file:
            df = pd.read_json(file).astype(str)

        df = df.iloc[:, 0]
        ids = df.tolist()
        return ids

class lista_links():
    def __init__(self, filename):
        self.filename = filename
    
    def read_json(self):
        df = pd.read_csv(r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\Pelis\files/{file}.csv'.format(file = self.filename))
        df = df.iloc[:, 0]
        df = df.apply(lambda x: x[2:len(x)-2])
        ids = df.tolist()
        return ids


# class Peliculas_direccion(scrapy.Spider):
#     name = 'movies_direccion'
    
#     file = input('Nombre del archivo: ')
#     ids = AbrirJsonFiles(file).read_json()
    
#     start_urls = ['https://www.imdb.com/title/{id}/fullcredits/?ref_=tt_cl_sm'.format(id=id) for id in ids]

#     def parse(self, response):
#         sel  = Selector(response)
#         link_movie = sel.xpath("//*[@class='subpage_title_block__right-column']//a/@href").extract()
#         id_imdb = re.findall('/title/(tt\d{7,11})/',link_movie[0])[0]
#         yield {
#             'id_imdb': id_imdb,
#             'escritores': [x.strip() for x in sel.xpath("//table[2][@class='simpleTable simpleCreditsTable']//a/text()").getall()],
#             'directores': [x.strip() for x in sel.xpath("//table[1][@class='simpleTable simpleCreditsTable']//a/text()").getall()]
#         }

# class Peliculas_plot(scrapy.Spider):
#     custom_settings = {
#     'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
#     'CLOSESPIDER_PAGECOUNT': 30000         
#     }

#     allowed_domains = ['imdb.com']
#     name = 'movies_plot'
#     file = input('file: ')
#     ids = AbrirJsonFiles(file).read_json()
#     start_urls = ['https://www.imdb.com/title/{id}/plotsummary?ref_=tt_stry_pl'.format(id=id) for id in ids]
#     download_delay = 1

#     def parse(self, response):
#         sel  = Selector(response)
#         link_movie = sel.xpath("//*[@class='subpage_title_block__right-column']//a/@href").extract()
#         id_imdb = re.findall('/title/(tt\d{7,11})/',link_movie[0])[0]
#         yield {
#             'id_imdb': id_imdb,
#             'plot': ''.join(sel.xpath("//*[@class='ipl-zebra-list']/li[2]/p/text()").getall())
#         }



class extraccion_info(scrapy.Spider):
    name = 'movies_info'
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'CLOSESPIDER_PAGECOUNT': 30000         
    }

    allowed_domains = ['imdb.com']

    allowed_domains = ['imdb.com']
    ids = lista_links('links_peliculas').read_json()
    start_urls = ['https://www.imdb.com/title/{id}/plotsummary?ref_=tt_stry_pl'.format(id=id) for id in ids]
    download_delay = 1

    def parse(self, response):
        sel  = Selector(response)
        link_movie = sel.xpath("//*[@class='subpage_title_block__right-column']//a/@href").extract()
        id_imdb = re.findall('/title/(tt\d{7,11})/',link_movie[0])[0]
        yield {
            'id_imdb': id_imdb,
            'plot': ''.join(sel.xpath("//*[@class='ipl-zebra-list']/li[2]/p/text()").getall())
        }

