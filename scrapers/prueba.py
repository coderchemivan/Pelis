



with open('files/titulos.txt','r') as f:
    urls = f.readlines()
    urls = [f'https://www.google.com/search?q={url.strip()} imdb' for url in urls]
