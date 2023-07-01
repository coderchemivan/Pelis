from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.imdb.com/feature/genre')
soup = BeautifulSoup(r.content, 'html.parser')

generos = soup.find_all('section', class_='ipc-page-section ipc-page-section--base')
generos = generos.find_all('div',attrs={'class':'ipc-chip ipc-chip--on-base-accent2'})
generos = ['https://www.imdb.com/' + genero.find('a').get('href') for genero in generos]



#guardando los generos en un archivo
with open('files/generos_imdb.txt','w') as f:
    for genero in generos:
        f.write(genero + ' \n')






