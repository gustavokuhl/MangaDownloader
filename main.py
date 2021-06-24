from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

import requests
import shutil
import os
import argparse


class Manga:
    def __init__(self, url):
        self.url = url
        self.addRequest()
        self.addSoup()
        self.setNome()
        self.addCapitulos()

    def addRequest(self):
        self.request = requests.get(self.url)

    def addSoup(self):
        self.soup = BeautifulSoup(self.request.text, 'html.parser')

    def addCapitulos(self):
        capitulos_divs = self.soup.findAll('div', class_='single-chapter')
        capitulos_divs.reverse()
        self.capitulos = []
        for div in capitulos_divs:
            capitulo = Capitulo(div.a.text, div.a['href'])
            self.capitulos.append(capitulo)

    def setNome(self):
        self.nome = self.soup.h1.text
    
    def getNome(self):
        return self.nome

    def getCapitulos(self):
        return self.capitulos

class Capitulo:
    def __init__(self, nome, url):
        self.nome = nome
        self.url = url
        self.addRequest()
        self.addSoup()
        self.show()

    def addRequest(self):
        self.request = requests.get(self.url)

    def addSoup(self):
        self.soup = BeautifulSoup(self.request.text, 'html.parser')
    
    def addImagensUrls(self):
        images_div = self.soup.find('div', class_='image-navigator')
        self.images_urls = []
        for image in images_div.find_all('img'):
            self.images_urls.append(image.attrs['src'])

    def getImagensUrls(self):
        return self.images_urls

    def getNome(self):
        return self.nome

    def show(self):
        print("Adicionado: {capitulo}".format(capitulo=self.nome))
    

def downloadImagem(path, url):
    with requests.get(url, stream=True) as req:
        filename = path / url.rsplit('/', 1)[1]
        with open(filename, 'wb') as file:
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, file)


parser = argparse.ArgumentParser(description='Anime Downloader')
parser.add_argument('-u', '--url', type=str)
parser.add_argument('-p', '--path', type=str)
parser.add_argument('-t', '--threads', type=int, default=5)
args = parser.parse_args()

manga = Manga(args.url)
path = Path(args.path)
try:
    os.mkdir(path)
except FileExistsError:
    pass

with ThreadPoolExecutor(max_workers=args.threads) as executor:
    for Capitulo in manga.getCapitulos():
        Capitulo.addImagensUrls()
        new_path = path / Capitulo.getNome()
        os.mkdir(new_path)
        for url in Capitulo.getImagensUrls():
            executor.submit(downloadImagem, new_path, url)