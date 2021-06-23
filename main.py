import requests
from bs4 import BeautifulSoup
from shutil import copyfileobj
from os import mkdir


def getAllCapitulos():
    capitulos_req = requests.get('https://mangayabu.top/manga/one-punch-man/')
    capitulos_soup = BeautifulSoup(capitulos_req.text, 'html.parser')
    capitulos_divs = capitulos_soup.findAll('div', class_='single-chapter')
    capitulos_urls = []
    for div in capitulos_divs:
        capitulos_urls.append(div.a['href'])
    capitulos_urls.reverse()
    return [capitulos_urls[0], capitulos_urls[1], capitulos_urls[3]]

def getAllImagesLinks(capitulos_urls):
    capitulo_images = []
    for capitulo_url in capitulos_urls:
        capitulo_req = requests.get(capitulo_url)
        capitulo_soup = BeautifulSoup(capitulo_req.text, 'html.parser')
        images_div = capitulo_soup.findAll('div', class_='image-navigator')
        images_urls = []
        for image in images_div[0].find_all('img'):
            images_urls.append(image.attrs['src'])
        capitulo_images.append(images_urls)
    return capitulo_images

def downloadImages(path, images_urls):
    pg = 0
    for image_url in images_urls:
        with requests.get(image_url, stream=True) as req:
            with open(path + str(pg) + '.jpg', 'wb') as file:
                req.raw.decode_content = True
                copyfileobj(req.raw, file)
                pg += 1


capitulos = getAllCapitulos()
images_links = getAllImagesLinks(capitulos)
cap = 0
for link in images_links:
    path = 'capitulo-' + str(cap) + '/'
    mkdir(path)
    downloadImages(path, link)
    exit(0)