import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DBM')))


from bs4 import BeautifulSoup
import requests
from lxml import etree
from tqdm import tqdm
import numpy as np
from DBM import MongoDB_admin
import os
import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import scrapy.crawler as crawler
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.log import configure_logging
from multiprocessing import Process, Queue
from twisted.internet import reactor
import winsound
import json
import re

from get_user_movies import MongoDB_admin




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


def get_user_movies_watch_date():
    process = CrawlerProcess()
    process.crawl(VistasEn)
    process.start()








class Letterboxd_user_scraper():
    def __init__(self,username,ejecutar=False):
        self.username = username
        self.ejecutar = ejecutar
        
        
    def scrape_list(self):
        if self.ejecutar == True:
            
            """
            Takes in a Letterboxd link and outputs a list of film title, release year, 
            director, cast, average rating and letterboxd url
            """
            _domain = 'https://letterboxd.com/'
            film_rows = []
            list_link = f'{_domain}/{self.username}/films/'
            while True:
                list_page = requests.get(list_link)
                
                # check to see page was downloaded correctly
                if list_page.status_code != 200:
                    pass

                soup = BeautifulSoup(list_page.content, 'html.parser')
            #imprimir el árbol html completo
                # browser.get(following_url)
                
                # grab the main film grid
                table = soup.find('ul', class_='poster-list')
                
                if table is None:
                    return None
                
                films = table.find_all('li')
                
                # iterate through films
                for film in tqdm(films):
                    film_info = {}
                
                    #attributes of the film
                    info_movie = film.find('div').attrs

                    # finding the film name
                    panel = film.find('div').find('img')
                    film_name = panel['alt']

                    # movie id
                    movie_id = info_movie['data-film-id']
                    
                    # try to find the rating of a film if possible and converting to float
                    try:
                        stars = film.find('span', class_='rating').get_text().strip()
                        rating = self.transform_stars(stars)
                    except:
                        rating = 0
                    
                    #Like button
                    like = True if len(film.find_all('span', class_='like has-icon icon-liked icon-16')) > 0 else False                

                    # Obtaining release year, director, cast and average rating of the movie
                    film_card = film.find('div').get('data-target-link')
                    film_page = _domain + film_card
                    #filmget = requests.get(film_page)
                    #film_soup = BeautifulSoup(filmget.content, 'html.parser')
                    
                    # release_year = film_soup.find('meta', attrs={'property':'og:title'}).attrs['content'][-5:-1]
                    #director = film_soup.find('meta', attrs={'name':'twitter:data1'}).attrs['content']
                    
                    # # try to find the cast, if not found insert a nan
                    # try:
                    #     cast = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-cast'}).find_all('a')]
                        
                    #     # remove all the 'Show All...' tags if they are present
                    #     cast = [i for i in cast if i != 'Show All…']
                    
                    # except:
                    #     cast = np.nan
                    
                    # # try to find average rating, if not insert a nan
                    # try:
                    #     average_rating = float(film_soup.find('meta', attrs={'name':'twitter:data2'}).attrs['content'][:4])
                    # except:
                    #     average_rating = np.nan

                    #film_rows.append([film_name, release_year, director, cast, rating, average_rating, _domain+film_card])
                    film_info['film_name'] = film_name
                    #film_info['release_year'] = release_year
                    #film_info['director'] = director
                    #film_info['cast'] = cast
                    film_info['rating'] = rating
                    #film_info['average_rating'] = average_rating
                    film_info['film_page'] = _domain+film_card
                    film_info['liked'] = like
                    #film_info['año'] = 0
                    film_rows.append(film_info)


                    
                # check if there is another page of ratings
                next_button = soup.find('a', class_='next')
                if next_button is None:
                    break
                else:
                    list_link = _domain + next_button['href']
            #escribir el dicc en un archivo txt
            if os.path.exists('files/data.txt'):
               os.remove('files/data.txt')   
            with open('files/data.txt', 'a') as outfile:
                json.dump(film_rows, outfile)
            return film_rows

    def transform_stars(self,starstring):
        """
        Transforms star rating into float value
        """
        stars = {
            "★": 1,
            "★★": 2,
            "★★★": 3,
            "★★★★": 4,
            "★★★★★": 5,
            "½": 0.5,
            "★½": 1.5,
            "★★½": 2.5,
            "★★★½": 3.5,
            "★★★★½": 4.5
        }
        try:
            return stars[starstring]
        except:
            return np.nan
    

    
class Peliculas (CrawlSpider):
    def __init__(self,usuario):
        self.usuario = usuario

    name = "Imdb titles"
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'CLOSESPIDER_PAGECOUNT': 1000,
    'FEEDS' :  {
    'files/mis_pelis.json' : {
        'format': 'json'
            }
        }
    }

    allowed_domains = ['letterboxd.com']
    #download_delay = 1

    films = Letterboxd_user_scraper(username='chemivan',ejecutar=True).scrape_list()
    peliculas_existentes = MongoDB_admin(password='bleistift16',db='movies',collection='watched').verificar_peliculas_existentes()
    peliculas_nuevas = []
    for k,v in enumerate(films):
        if v['film_page'] not in peliculas_existentes:
            peliculas_nuevas.append(v['film_page'])
    start_urls = [film['film_page'] for film in films]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            
    def parse(self, response):
        sel  = Selector(response)
        info = {}
        titulo = sel.xpath("//*[@id='featured-film-header']/h1/text()")[0].get()
        if titulo == 'It':
            print('hola')
        try:
            año = sel.xpath("//*[@id='featured-film-header']//a[contains(@href, 'year')]/text()")[0].get()
        except:
            año = 'ND'

        try:
            directores = sel.xpath("//*[@id='featured-film-header']/p/a/span/text()").getall()
        except:
            directores = 'ND'

        try:
            imdb_id = sel.xpath("//p[@class='text-link text-footer']/a[contains(@href, 'imdb')]/@href").get()
            imdb_id = re.findall(r'tt\d+', imdb_id)[0]
        except:
            imdb_id = 'ND'
        
        try:
            tmdb_id = sel.xpath("//p[@class='text-link text-footer']/a[contains(@href, 'themoviedb')]/@href").get()
            tmdb_id = re.findall(r'movie/(\d+)', tmdb_id)[0]
        except:
            tmdb_id = 'ND'

        try:
            film_page = sel.xpath("//div[@id='tabbed-content']//li/a/@href")[1].get()
            film_page = re.findall(r'(film/.+)/(details|crew|releases|genres)', film_page)[0][0]
        except:
            film_page = 'ND'
        #image_url = sel.xpath("//div[@id='poster-large']//img/@src").getall()
        with open('files/data.txt') as json_file:
            data = json.load(json_file)
            for p in data:
                print(f'https://letterboxd.com//{film_page}'  ,   p['film_page'])
                if p['film_page'] == f'https://letterboxd.com//{film_page}/':
                    rating = p['rating']
                    liked = p['liked']
                    pagina = p['film_page']
                    break

        with open('files/vistas_en.json') as json_file:
            data = json.load(json_file) 
            for p in data:
                print(f'/{film_page}/'  ,   p['film_page'])
                if p['film_page'] == f'/{film_page}/':
                    vista_en = p['fecha_vista']
                    break


        yield {
                'titulo': titulo,
                'año': año,
                'directores': directores,
                'rating': rating,
                'usuario': self.usuario,
                'imdb_id': imdb_id,
                'tmdb_id': tmdb_id,
                'liked': liked,
                'vista_en': vista_en,
                'film_page': f'/{film_page}/',
                

        }
        
def get_user_movies():
    #eliminar data.txt si existe

    process = CrawlerProcess()
    process.crawl(Peliculas,usuario='chemivan')
    process.start()
    duration = 1000  # milliseconds
    freq = 440  # Hz
    #abrir el doc mis_pelis.json y pasar la info a una lista de diccionarios
    with open('files/mis_pelis.json') as json_file:
        data = json.load(json_file)
        film_rows = []
        for p in data:
            film_rows.append(p)
    #MongoDB_admin(password='bleistift16',db='movies',collection='watched').insert_documents(film_rows) 
    winsound.Beep(freq, duration)











if os.path.exists('files/vistas_en.json'):
    os.remove('files/vistas_en.json')   

if os.path.exists('files/mis_pelis.json'):
    os.remove('files/mis_pelis.json')   
get_user_movies_watch_date()  
get_user_movies()



        
       

