# MangaDownloader

## Descrição

WebScraping multithread em python para baixar mangas do site [mangayabu](https://mangayabu.top)

## Como utilizar
```bash
git clone https://github.com/gustavokuhl/MangaDownloader.git
cd MangaDownloader
python3 main.py -u https://mangayabu.top/manga/boruto-naruto-next-generations/ -p /tmp/Boruto
```

## Argumentos
```
-u --url     -> URL do manga
-p --path    -> Pasta que serão colocados os arquivos
-t --threads -> Quantidade de threads (cuidar com números muito altos)
```
