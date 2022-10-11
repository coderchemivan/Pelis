from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import pandas as pd



# df = pd.read_json('files/titulos1.json').astype(str)
# df = df.iloc[:, 0]
# df = df.apply(lambda x: x[2:len(x)-2])
# print(df)



class Opinion(Item):
    title = Field()
    genre = Field()
    director = Field()
    guionista = Field()
    year = Field()
    duracion = Field()
    rating = Field()
    budget = Field()
    boxOffice_collection = Field()
    plot = Field()
    cast = Field()
    personajes = Field()
    estreno = Field()
    


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
        # Rule( #Extracción de generos
        #     LinkExtractor(
        #         allow=r'genres=.+&title_type=feature&explore'
        #     ), follow=True),

        Rule(#Paginación de peliculas
            LinkExtractor(
                allow=r'adv_nxt'
            ), follow=True),

        
        Rule(#Detalle de películas
            LinkExtractor(
                allow =r'/title/tt\d+',
                restrict_xpaths=["//*[@class='lister-list']/div/div/h3/a"]
            ), follow=True,callback='parse_titles'),
        
        Rule(#Reparto
            LinkExtractor(
                allow =r'fullcredits',

        ),follow=True,callback='parse_cast')  
        )
    
    
    

    def parse_titles(self, response):

    
        sel  = Selector(response)
        item = ItemLoader(Opinion(),sel)

        try:
            titulo = sel.xpath('//*[@hero-title-block__original-title="hero-title-block__original-title"]/text()')[0].get()
            
        except:
            titulo = sel.xpath('//*[@data-testid="hero-title-block__title"]/text()')[0].get()
            
        
        
        #print(titulo)
        #if titulo not in df.values:

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
            estreno = sel.xpath("//*[@data-testid='tm-box-up-date']/text()").get()
            item.add_value('estreno',estreno)
        except:
            item.add_value('estreno','0')


        '''director'''
            #//*[@class='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base'][1] me va a dar el director o guión
        posibles_contenedores = sel.xpath("//*[@class='ipc-metadata-list__item']")
        director_count = 0
        for i in range(len(posibles_contenedores)):
            direccion = posibles_contenedores[i].xpath('.//span/text()').get()
            print(direccion,i)
            if direccion =="Director":
                director_count+=1
                if director_count ==3:
                    directores_contenedor = sel.xpath("//*[@class='ipc-metadata-list__item']")[i]
                    directores = directores_contenedor.xpath(".//div/ul/li/a/text()")
                    for director in directores:
                        item.add_value('director',director.get())
            continue
        
        #    item.add_value('director','ND')
        
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


        '''plot'''
        try:
            plot_ = sel.xpath("//*[@class='sc-132205f7-0 bJEfgD']/div/div/div/text()").get()
            item.add_value('plot',plot_)
        except:
            item.add_value('plot', 'ND')
        yield item.load_item() 

    def parse_cast(self, response):
        sel  = Selector(response)
        item = ItemLoader(Opinion(),sel)
        print('___________________')
        print('___________________')

#scrapy runspider prueba.py -o files/titulos1.json -t json

