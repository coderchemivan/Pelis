import os

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader




class VistasEn (CrawlSpider):
    
    name = "Imdb titles"
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'CLOSESPIDER_PAGECOUNT': 30000,    
    'FEEDS' :  {
    'files/vistas_en.json' : {
        'format': 'json'
            }
        } ,
    }           
    

    allowed_domains = ['letterboxd.com']
    start_urls = [f'https://letterboxd.com/chemivan/films/diary/']
    


    rules = (
        Rule(#Paginación de peliculas
            LinkExtractor(
                allow=r'page'
            ), follow=True),

        
        Rule(#Detalle de películas
            LinkExtractor(
                restrict_xpaths=["//td[@class='td-film-details']//h3/a"]
            ), follow=True,callback='parse_titles'),
        )
    
    def parse_titles(self, response):
        sel  = Selector(response)
        titulo = sel.xpath("//span[@class='film-title-wrapper']/a/text()").get()
        fecha_vista = sel.xpath('//*[@id="content"]//meta/@content').get()
        film_page = sel.xpath("//span[@class='film-title-wrapper']/a/@href").get()


        yield {
                'titulo': titulo,
                'fecha_vista': fecha_vista,
                'film_page': film_page,
        }

if os.path.exists('files/vistas_en.json'):
    os.remove('files/vistas_en.json')   
def get_user_movies():
    process = CrawlerProcess()
    process.crawl(VistasEn)
    process.start()

get_user_movies()

