# Python爬蟲入門範例實戰在Yahoo電影這個網頁上，來爬出目前排行榜底下台北票房的電影排名與其他資訊。

# import libs
import requests
import pandas as pd
from bs4 import BeautifulSoup
# define url for crawling
url = 'https://movies.yahoo.com.tw/chart.html'

# GET request from url and parse via BeautifulSoup
resp = requests.get(url)
resp.encoding = 'utf-8' # encoded with format utf-8 for chinese character
soup = BeautifulSoup(resp.text, 'lxml')

# parse colname 
rows = soup.find_all('div', class_='tr')
# get strings and convert into list
colname = list(rows.pop(0).stripped_strings) 
print(colname)

# rows
# parse rest content info
contents = []
for row in rows:
    thisweek_rank = row.find_next('div', attrs={'class':'td'})
    updown = thisweek_rank.find_next('div')
    lastweek_rank = updown.find_next('div')
    
    # for the data form of first row in this web page is different from other rows
    if thisweek_rank.string == str(1):
        movie_title = lastweek_rank.find_next('h2')
    else:
        movie_title = lastweek_rank.find_next('div', attrs={'class':'rank_txt'})
    
    release_date = movie_title.find_next('div', attrs={'class':'td'})
    trailer = release_date.find_next('div', attrs={'class':'td'})
    trailer_address = trailer.find('a')['href']
    stars = row.find('h6', attrs={'class':'count'})
    
    # replace None with empty string ''
    lastweek_rank = lastweek_rank.string if lastweek_rank.string else ''
    
    c = [thisweek_rank.string, lastweek_rank, movie_title.string, release_date.string, trailer_address, stars.string]
    print(c)
    contents.append(c)
print(contents)

# convert to data frame format

df = pd.DataFrame(contents, columns=colname)
df.head()

import os
import datetime

cwd = os.getcwd()
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime('%Y%m%d')

filename = os.path.join(cwd, 'yahoo_movie_rank_{}.csv'.format(timestamp))
df.to_csv(filename, index=False)
print('Save csv to {}'.format(filename))