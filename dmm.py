#! python3
# dmm.py - Download Meeting Media
# Downloads all meeting media from jw.org

# imports
import requests, bs4, webbrowser, pprint, os

# language, month, year, dates (Example: 7-13)
def inputs():
    print('Month: ', end='')
    month = input()
    print('Year: ', end='')
    year = input()
    print('Dates: ', end='')
    dates = input()
    return month, year, dates

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
directory = 'C:\\Users\\Mack W\\Documents\\Python\\personalProjects\\Meeting Media Downloader'
os.chdir(directory)
# week = inputs() # returns a tuple with the month, year, and dates (Example 7-13)
# saveWebsite()
# saveImages()
