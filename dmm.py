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
def guia(info):
    month = info['month']
    year = info['year']
    dates = info['dates']    
    base = 'https://www.jw.org/es/publicaciones/guia-actividades-reunion-testigos-jehova/'
    ext = '%s-%s-mwb/programa-reunion-%sen/' % (month, year, dates)
    url = base + ext
    res = requests.get(url)
    res.raise_for_status()
    # workbook name
    workbook = ('%s %s workbook.txt' % (month, dates))
    file = open(workbook, 'wb')
    for chunk in res.iter_content(100000):
        file.write(chunk)
    file.close()

def media(info):
    month = info['month']
    dates = info['dates'] 
    # make soup
    file = open(('%s %s workbook.txt' % (month, dates)), 'rb')
    meetingSoup = bs4.BeautifulSoup(file, features="lxml")
    # find links
    # elems = meetingSoup.select('a[data-video]') # finds videos when it says 'el video'
    elems = meetingSoup.select('em')
    for i in range(len(elems)):       
        print(elems[i])

# Main

# get data
#info = inputs()
info = {'month': 'enero', 'year': '2019', 'dates': '7-13', 'path':
        'C:\\Users\\Mack W\\Documents\\Python\\personalProjects\\Meeting Media Downloader'}

# where to save the media
os.chdir(info['path'])

# Function calls
# guia(info)
media(info)

# TODO
'''
line 42 - find out what element leads to media content
'''



