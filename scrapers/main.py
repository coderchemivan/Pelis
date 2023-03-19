from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np
from pymongo import MongoClient
import os
import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
import winsound
import json



class Letterboxd_user_scraper():
    def __init__(self,username):
        self.username = username
        
        
    def scrape_list(self):
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
                    rating = np.nan
                
                # Obtaining release year, director, cast and average rating of the movie
                film_card = film.find('div').get('data-target-link')
                film_page = _domain + film_card
                # filmget = requests.get(film_page)
                # film_soup = BeautifulSoup(filmget.content, 'html.parser')
                
                # release_year = film_soup.find('meta', attrs={'property':'og:title'}).attrs['content'][-5:-1]
                # director = film_soup.find('meta', attrs={'name':'twitter:data1'}).attrs['content']
                
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
                film_info['tmdb_id'] = movie_id
                #film_info['release_year'] = release_year
                #film_info['director'] = director
                #film_info['cast'] = cast
                film_info['rating'] = rating
                #film_info['average_rating'] = average_rating
                film_info['film_page'] = _domain+film_card
                #film_info['año'] = 0
                film_rows.append(film_info)


                
            # check if there is another page of ratings
            next_button = soup.find('a', class_='next')
            if next_button is None:
                break
            else:
                list_link = _domain + next_button['href']
        #escribir el dicc en un archivo txt
        with open('files/data.txt', 'w') as outfile:
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
    

    
class MongoDB_admin():
    def __init__(self,password,db,collection):
        self.password =  password
        self.db = db
        self.collection = collection
        
    def db_connect(self,documents):
        connection_string = f"mongodb+srv://coderchemivan:{self.password}@cluster0.mp5mmin.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection_string)
        db = client[self.db]
        
        #creat collection if not exists
        if self.collection not in db.list_collection_names():
            db.create_collection(self.collection)
            col = self.collection
            #create index con los campos de nombre y año
            db[col].create_index([('titulo',1),('año',1)],unique=True)
        self.collection = db[self.collection]
        self.collection.insert_many(documents,ordered=False)

class Peliculas (CrawlSpider):
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

    films = Letterboxd_user_scraper(username='chemivan').scrape_list()
    start_urls = [film['film_page'] for film in films]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            
    def parse(self, response):
        sel  = Selector(response)
        info = {}
        titulo = sel.xpath("//*[@id='featured-film-header']/h1/text()")[0].get()
        año = sel.xpath("//*[@id='featured-film-header']//a[contains(@href, 'year')]/text()")[0].get()
        with open('files/data.txt') as json_file:
            data = json.load(json_file)
            for p in data:
                if p['film_name'] == titulo:
                    rating = p['rating']
                    break
        yield {
                'titulo': titulo,
                'año': año,
                'rating': rating
        }
        
def main():
    process = CrawlerProcess()
    process.crawl(Peliculas)
    process.start()
    duration = 1000  # milliseconds
    freq = 440  # Hz
    #abrir el doc mis_pelis.json y pasar la info a una lista de diccionarios
    with open('files/mis_pelis.json') as json_file:
        data = json.load(json_file)
        film_rows = []
        for p in data:
            film_rows.append(p)
    print(film_rows)
    MongoDB_admin(password='bleistift16',db='movies',collection='watched').db_connect(film_rows) 
    winsound.Beep(freq, duration)
    os.remove('files/mis_pelis.json')


if __name__ == '__main__':
    main()


#mis_pelis = Letterboxd_user_scraper(username='chemivan').scrape_list()

#MongoDB_admin(password='bleistift16',db='movies',collection='watched').db_connect([{'film_name': 'All the Places', 'año':2023, 'rating': 2.5}])




