import scrapy
from scrapy.selector import Selector

class Peliculas_direccion(scrapy.Spider):
    name = 'movies_direccion'
    start_urls = ['https://www.imdb.com/title/tt2562232/fullcredits/?ref_=tt_cl_sm']

    def parse(self, response):
        sel  = Selector(response)
        yield {
            'escritores': [x.strip() for x in sel.xpath("//table[2][@class='simpleTable simpleCreditsTable']//a/text()").getall()],
            'directores': [x.strip() for x in sel.xpath("//table[1][@class='simpleTable simpleCreditsTable']//a/text()").getall()]
        }

class Peliculas_plot(scrapy.Spider):
    name = 'movies_plot'
    start_urls = ['https://www.imdb.com/title/tt2562232/plotsummary?ref_=tt_stry_pl']

    def parse(self, response):
        sel  = Selector(response)
        yield {
            'escritores': ''.join(sel.xpath("//*[@class='ipl-zebra-list']/li[2]/p/text()").getall(),)
        }


