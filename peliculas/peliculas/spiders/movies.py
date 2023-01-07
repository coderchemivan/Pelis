from isort import file
import scrapy
from scrapy.selector import Selector
import re
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule



class AbrirJsonFiles():
    def __init__(self, filename):
        self.filename = filename
    
    def read_json(self):
        with open(r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\Pelis\files/{file}.json'.format(file = self.filename), 
        encoding='utf-8') as file:
            df = pd.read_json(file).astype(str)

        df = df.iloc[:, 0]
        df = df.apply(lambda x: x[2:len(x)-2])
        ids = df.tolist()
        return ids

class lista_links():
    def __init__(self):pass
        
    
    def read_csv(self):
        df = pd.read_csv(r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\Pelis\files\titulos_faltantes.csv')
        df = df.iloc[:, 0]
        ids = df.tolist()
        return ids


# class Peliculas_direccion(scrapy.Spider):
#     name = 'movies_direccion'
#     custom_settings = {
#     'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
#     'CLOSESPIDER_PAGECOUNT': 5350, 
#     'FEEDS' :  {
#        'peliculas/plot/plot1.json' : {
#            'format': 'json'
#        }
#     }             
#     }
#     file = input('Nombre del archivo: ')
#     ids = AbrirJsonFiles(file).read_json()
    
#     start_urls = ['https://www.imdb.com/title/{id}/fullcredits/?ref_=tt_cl_sm'.format(id=id) for id in ids]

#     def parse(self, response):
#         sel  = Selector(response)
#         link_movie = sel.xpath("//*[@class='subpage_title_block__right-column']//a/@href").extract()
#         id_imdb = re.findall('/title/(tt\d{7,11})/',link_movie[0])[0]
#         escritores_link= sel.xpath("//table[2][@class='simpleTable simpleCreditsTable']//a/@href").getall()
#         escritores_link = [re.findall('/name/(nm\d{7,11})/',escritor_link)[0] for escritor_link in escritores_link]

#         directores_link = sel.xpath("//table[1][@class='simpleTable simpleCreditsTable']//a/@href").getall()
#         directores_link = [re.findall('/name/(nm\d{7,11})/',director_link)[0] for director_link in directores_link]

#         try:
#             actores_link = sel.xpath("//*[@class='cast_list']//tr//td[2]/a/@href")[0:20].getall()
#         except:
#             actores_link = sel.xpath("//*[@class='cast_list']//tr//td[2]/a/@href").getall()
#         actores_link = [re.findall('/name/(nm\d{7,11})/',actor_link)[0] for actor_link in actores_link]
 
#         yield {
#             'id_imdb': id_imdb,
#             'escritores': [x.strip() for x in sel.xpath("//table[2][@class='simpleTable simpleCreditsTable']//a/text()").getall()],
#             'escritores_link': escritores_link,
#             'directores': [x.strip() for x in sel.xpath("//table[1][@class='simpleTable simpleCreditsTable']//a/text()").getall()],
#             'directores_link': directores_link,
#             'actores_link': actores_link
#         }



#scrapy crawl movies_plot -O plot1/plot1.json
#scrapy crawl movies_direccion -O reparto/reparto1.json
# class Peliculas_plot(scrapy.Spider):
#     name = 'movies_plot'
#     custom_settings = {
#     'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
#     'CLOSESPIDER_PAGECOUNT': 5350, 
#     'FEEDS' :  {
#        'peliculas/plot/plot1.json' : {
#            'format': 'json'
#        }
#     }             
#     }

#     allowed_domains = ['imdb.com']
    
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


# def main():
#     process = CrawlerProcess()
#     process.crawl(Peliculas_plot)
#     process.start()

# if __name__ == '__movies__':
#     main()









class extraccion_info(scrapy.Spider):
    name = 'movies_info'
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'CLOSESPIDER_PAGECOUNT': 30000         
    }

    allowed_domains = ['imdb.com']

    allowed_domains = ['imdb.com']
    ids = lista_links().read_csv()
    start_urls = ['https://www.imdb.com/title/{id}/'.format(id=id) for id in ids]
    download_delay = 1

    def parse(self, response):
        sel  = Selector(response)
        '''ID'''
        links = sel.xpath("//*[@class='ipc-metadata-list-item__icon-link']/@href").getall()
        id_imdb = re.findall('/title/(tt\d{7,11})/',''.join(links))[0]
        print(id_imdb)
        yield {
            'id_imdb': id_imdb,
            'hola perros' : "hola"
        }