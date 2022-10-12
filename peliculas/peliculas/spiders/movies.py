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
        df = df.apply(lambda x: x[2:len(x)-2])
        ids = df.tolist()
        return ids




class Peliculas_direccion(scrapy.Spider):
    name = 'movies_direccion'
    
    file = input()
    ids = AbrirJsonFiles(file).read_json()
    
    start_urls = ['https://www.imdb.com/title/{id}/fullcredits/?ref_=tt_cl_sm'.format(id=id) for id in ids]

    def parse(self, response):
        sel  = Selector(response)
        link_movie = sel.xpath("//*[@class='subpage_title_block__right-column']//a/@href").extract()
        id_imdb = re.findall('/title/(tt\d{7,11})/',link_movie[0])[0]
        yield {
            'id_imdb': id_imdb,
            'escritores': [x.strip() for x in sel.xpath("//table[2][@class='simpleTable simpleCreditsTable']//a/text()").getall()],
            'directores': [x.strip() for x in sel.xpath("//table[1][@class='simpleTable simpleCreditsTable']//a/text()").getall()]
        }

class Peliculas_plot(scrapy.Spider):
    name = 'movies_plot'
    file = input()
    ids = AbrirJsonFiles(file).read_json()
    start_urls = ['https://www.imdb.com/title/{id}/plotsummary?ref_=tt_stry_pl'.format(id=id) for id in ids]

    def parse(self, response):
        sel  = Selector(response)
        link_movie = sel.xpath("//*[@class='subpage_title_block__right-column']//a/@href").extract()
        id_imdb = re.findall('/title/(tt\d{7,11})/',link_movie[0])[0]
        yield {
            'id_imdb': id_imdb,
            'plot': ''.join(sel.xpath("//*[@class='ipl-zebra-list']/li[2]/p/text()").getall())
        }


