import scrapy
from scrapy.selector import Selector
import re

class Peliculas_direccion(scrapy.Spider):
    name = 'movies_direccion'
    start_urls = ['https://www.imdb.com/title/tt2562232/fullcredits/?ref_=tt_cl_sm']

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
    start_urls = ['https://www.imdb.com/title/tt2562232/plotsummary?ref_=tt_stry_pl']

    def parse(self, response):
        sel  = Selector(response)
        link_movie = sel.xpath("//*[@class='subpage_title_block__right-column']//a/@href").extract()
        id_imdb = re.findall('/title/(tt\d{7,11})/',link_movie[0])[0]
        yield {
            'id_imdb': id_imdb,
            'plot': ''.join(sel.xpath("//*[@class='ipl-zebra-list']/li[2]/p/text()").getall())
        }


