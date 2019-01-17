#! python3
# dmm.py - Download Meeting Media
# Downloads all meeting media from jw.org

# imports
import requests, bs4, webbrowser, pprint, os

# Dummy dictionary for testing
info = {'month': 'enero', 'year': '2019', 'dates': '7-13', 'path':
        'C:\\Users\\Mack W\\Documents\\Python\\personalProjects\\Meeting Media Downloader'}

# month, year, dates (Example: 7-13)
def inputs():
    info = {'month': '', 'year': '', 'dates': '', 'path': ''}
    keys = list(info.keys())
    for i in range(len(keys)):
        print('%s: ' % keys[i], end='')
        info[keys[i]] = input()
    return info    

# save workbook html
def guia(info):
    # all spanish workbooks start with this url
    base = 'https://www.jw.org/es/publicaciones/guia-actividades-reunion-testigos-jehova'
    # craft url using user input data
    month = info['month']
    year = info['year']
    dates = info['dates']    
    ext = '/%s-%s-mwb/programa-reunion-%sen/' % (month, year, dates)
    # download the url
    url = base + ext
    res = requests.get(url)
    res.raise_for_status()
    # workbook name
    workbook = ('%s %s workbook.txt' % (month, dates))
    # save to file
    file = open(workbook, 'wb')
    for chunk in res.iter_content(100000):
        file.write(chunk)
    file.close()

# return urls of the meeting parts
def mediaUrls(info):
    month = info['month']
    dates = info['dates']
    
    # make soup object to parse the html
    file = open(('%s %s workbook.txt' % (month, dates)), 'rb')
    meetingSoup = bs4.BeautifulSoup(file, features="lxml")
    
    # find elements (where the magic happens)
    elems = []
    elems += meetingSoup.select('a[class="pubSym-nwtsv"]') # introduction to bible books videos
    elems += meetingSoup.select('a[class="pubSym-mwb19"]') # tesoros y nuestra vida cristiana
    elems += meetingSoup.select('a[data-video]')           # videos when it says 'el video'
    elems += meetingSoup.select('a[class="pubSym-thv"]')   # seamos mejores maestros
    elems += meetingSoup.select('a[class="pubSym-jy"]')    # Jesus-The Way jy book
    
    # find links
    urls = []   
    base = 'https://www.jw.org'
    for i in range(len(elems)):
        ext = elems[i].get('href')
        if ext.startswith('/'):
            url = base + ext
        else:
            url = ext
        urls.append(url)
    return urls

def web2text(urls):
    names = []
    # download and name media files
    for i in range(len(urls)):
        res = requests.get(urls[i])
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features="lxml")
        elem = soup.select('h1')
        if elem:
            name = elem[0].getText() + '.txt'
            names.append(name)
            file = open(name, 'wb')
            for chunk in res.iter_content(100000):
                file.write(chunk)
            file.close()
    return names

# Main
# info = inputs()
os.chdir(info['path'])
# guia(info)
urls = mediaUrls(info)
fileNames = web2text(urls)
print(fileNames)

# TODO
'''
new funtion
downloads media from the urls
which are
provided by the mediaUrls function
'''

# Example: download video
'''
dwn_link = 'https://download-a.akamaihd.net/files/media_periodical/8f/mwbv_E_201901_01_r720P.mp4'
file_name = 'primera conversación.mp4' 
rsp = requests.get(dwn_link)
rsp.raise_for_status()
file = open(file_name, 'wb')
for chunk in rsp.iter_content(100000):
    file.write(chunk)
file.close()

# Video element
# <video
# class="vjs-tech" id="vjs_video_721_html5_api" tabindex="-1"
# preload="none" src="https://download-a.akamaihd.net/files/
# media_periodical/8f/mwbv_E_201901_01_r720P.mp4"
# poster="https://assetsnffrgf-a.akamaihd.net/assets/m/mwbv/univ/201901/art/mwbv_univ_201901_wsr_01_lg.jpg">
# </video>
'''



