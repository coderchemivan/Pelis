from attr import attrs
import requests
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import pandas as pd

from bs4 import BeautifulSoup
import re

# df = pd.read_json('files/titulos1.json').astype(str)
# df = df.iloc[:, 0]
# df = df.apply(lambda x: x[2:len(x)-2])
# print(df)



class Opinion(Item):
    id_imdb = Field()
    title = Field()
    genre = Field()
    director = Field()
    guionista = Field()
    plot = Field()
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

        try:
            titulo = sel.xpath('//*[@hero-title-block__original-title="hero-title-block__original-title"]/text()')[0].get()
            
        except:
            titulo = sel.xpath('//*[@data-testid="hero-title-block__title"]/text()')[0].get()
            
        '''ID'''
        links = sel.xpath("//*[@class='ipc-metadata-list-item__icon-link']/@href").getall()
        id_imdb = re.findall('/title/(tt\d{7,11})/',''.join(links))[0]
        item.add_value('id_imdb', id_imdb)      
        

        '''Titulo'''
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


        '''director'''
        link = 'https://www.imdb.com/title/{id_imdb}/fullcredits/?ref_=tt_cl_sm'.format(id_imdb=id_imdb)
        response = requests.get(link)
        sel = Selector(response)
        try:
            directores = [x.strip() for x in sel.xpath("//*[@id='fullcredits_content']//table[1]//td/a/text()").getall()]
            directores_=[]
            [directores_.append(director) for director in directores if director not in directores_]
            item.add_value('director', directores_)
        except:
            item.add_value('director', 'ND')

        try:
            guionistas = [x.strip() for x in sel.xpath("//*[@id='fullcredits_content']//table[2]//td/a/text()").getall()]
            papel_guionista = [x.strip() for x in sel.xpath("//*[@id='fullcredits_content']//table[2]//td[@class='credit']/text()").getall()]
            guionistas_=[]
            [guionistas_.append(guionista) for guionista in guionistas if guionista not in guionistas_]
            papel_guionista_ = []
            [papel_guionista_.append(papel) for papel in papel_guionista if papel not in papel_guionista_]
            guionista = {papel_guionista_[i]:guionistas_[i] for i in range(len(guionistas_))}
            item.add_value('guionista', guionista)
        except:
            item.add_value('guionista', 'ND')


       
        '''plot'''
        link = 'https://www.imdb.com/title/{id_imdb}/plotsummary?ref_=tt_stry_pl'.format(id_imdb=id_imdb)
        response = requests.get(link)
        sel = Selector(response)
        try:
            plot = ''.join(sel.xpath("//*[@id='plot-summaries-content']/li[2]/p/text()").getall())
            if plot == '':
                plot = ''.join(sel.xpath("//*[@id='plot-summaries-content']/li[1]/p/text()").getall())
            item.add_value('plot', plot)
            item.add_value('director', directores)
        except:
            item.add_value('director', 'ND')

     
        yield item.load_item() 


    def parse_cast(self, response):pass


#scrapy runspider extraccion_peliculas.py -o files/titulos1.json -t json

