#! python3
# dmm.py - Download Meeting Media
# Downloads all meeting media from jw.org

# imports
import requests, bs4, webbrowser, pprint, os

# month, year, dates (Example: 7-13)
def inputs():
    info = {'month': '', 'year': '', 'dates': '', 'path': ''}
    keys = list(info.keys())
    for i in range(len(keys)):
        print('%s: ' % keys[i], end='')
        info[keys[i]] = input()
    return info

# download webpage
def saveWebsite():
    res = requests.get('https://www.jw.org/es/publicaciones/guia-actividades-reunion-testigos-jehova/enero-2019-mwb/programa-reunion-7-13en/efectuese-voluntad-de-jehova/')
    res.raise_for_status()
    tesoros = open('efectuese la voluntad de jehová.txt', 'wb')
    for chunk in res.iter_content(100000):
        tesoros.write(chunk)
    tesoros.close()

def saveImages():
    # make soup
    file = open('efectuese la voluntad de jehová.txt', 'rb')
    meetingSoup = bs4.BeautifulSoup(file, features="lxml")
    # find links
    imageElems = meetingSoup.select('aside li figure span[class]')
    for i in range(len(imageElems)):
        # open link
        url = imageElems[i].get('data-zoom')
        image = requests.get(url)
        image.raise_for_status()    
        # name and save file
        imageFile = open('%d.jpg' % i, 'wb')
        for chunk in image.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
    # close your files
    file.close()

# Main
info = inputs()
os.chdir(info['path'])
# saveWebsite()
# saveImages()
