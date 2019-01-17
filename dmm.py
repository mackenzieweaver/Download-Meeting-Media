#! python3
# dmm.py - Download Meeting Media
# Downloads all meeting media from jw.org

# imports
import requests, bs4, webbrowser, pprint, os

# Dummy dictionary for testing
info = {'month': 'enero', 'year': '2019', 'dates': '28en-3febr', 'path':
        'C:\\Users\\Mack W\\Documents\\Python\\personalProjects\\Meeting Media Downloader'}

# where to save the media
os.chdir(info['path'])

# month, year, dates (Example: 7-13)
def inputs():
    info = {'month': '', 'year': '', 'dates': '', 'path': ''}
    keys = list(info.keys())
    for i in range(len(keys)):
        print('%s: ' % keys[i], end='')
        info[keys[i]] = input()
    return info

# download webpage
def guia(info):
    month = info['month']
    year = info['year']
    dates = info['dates']    
    ext = '/%s-%s-mwb/programa-reunion-%s/' % (month, year, dates)
    base = 'https://www.jw.org/es/publicaciones/guia-actividades-reunion-testigos-jehova'
    url = base + ext
    res = requests.get(url)
    res.raise_for_status()
    # workbook name
    workbook = ('%s %s workbook.txt' % (month, dates))
    file = open(workbook, 'wb')
    for chunk in res.iter_content(100000):
        file.write(chunk)
    file.close()

def mediaUrls(info):
    month = info['month']
    dates = info['dates']
    
    # make soup
    file = open(('%s %s workbook.txt' % (month, dates)), 'rb')
    meetingSoup = bs4.BeautifulSoup(file, features="lxml")
    
    # find elements
    elems = []
    elems += meetingSoup.select('a[class="pubSym-nwtsv"]') # introduction to bible books videos
    elems += meetingSoup.select('a[class="pubSym-mwb19"]') # tesoros y nuestra vida cristiana
    elems += meetingSoup.select('a[data-video]')           # videos when it says 'el video'
    elems += meetingSoup.select('a[class="pubSym-thv"]')   # seamos mejores maestros
    elems += meetingSoup.select('a[class="pubSym-jy"]')    # Jesus-The Way jy book
    
    # find links
    urls = []
    for i in range(len(elems)):        
        base = 'https://www.jw.org'
        ext = elems[i].get('href')
        if ext.startswith('/'):
            url = base + ext
        else:
            url = ext
        urls.append(url)
    return urls

# Main
# info = inputs()
# guia(info)
urls = mediaUrls(info)
print(urls)

# TODO
'''

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



