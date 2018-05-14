# To scrap Billboard Hot 100 songs of every week since 
# 1960 to current year

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import codecs
import csv

def parser(html):
    songs = []
    artists = []
    ranks = []
    weeks = []

    soup = BeautifulSoup(html, 'html.parser')

    artist_tags = soup.find_all(class_="chart-row__artist")
    if len(artist_tags) < 1:
        artist_tags = soup.find_all(class_="chart-row__artist")
    song_tags = soup.find_all(class_="chart-row__song")
    rank_tags = soup.find_all(class_="chart-row__current-week")
    week_tag = soup('time')
    for week in week_tag:
        weeks.append(week.get_text())
    for tag in artist_tags:
        tag = tag.get_text()
        tag = tag.strip()
        if len(tag) > 0:
            artists.append(tag)

    for tag in song_tags:
        tag = tag.get_text()
        if len(tag) > 0:
            songs.append(tag)

    for tag in rank_tags:
        tag = tag.get_text()
        ranks.append(tag)

    return songs, ranks, artists, weeks

# to avoid ssl certificate issue
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# starting year(replace with year you want)
initial = 1960
years = []
while True:
    if initial == 2018:
        break
    years.append(initial)
    initial += 1

# starting month(replace with month you want)
initial = 1
months = []
while True:
    if initial == 13:
        break
    months.append(initial)
    initial += 1

initial = 1
days = []
while True:
    if initial == 32:
        break
    days.append(initial)
    initial += 1

for year in years:
    for month in months:
        for day in days:
            year = str(year)
            month = str(month)
            day = str(day)
            day = day.zfill(2)
            month = month.zfill(2)
            url = 'http://www.billboard.com/charts/hot-100/'
            url = url + year + '-' + month + '-' + day
            print('trying for %s' % url)
            try:
                html = urllib.request.urlopen(url, context=ctx)
            except urllib.error.HTTPError:
                continue
            if html.getcode() == 200:
                html = html.read()
                song, rank, artist, week = parser(html)
                week =week[0]
                with codecs.open('%s.csv' % week, 'wb', encoding='utf-8') as output:
                    print('writing for %s %s' % (year, week))
                    fields = ['Rank', 'Song', 'Artist']
                    logger = csv.DictWriter(output, fieldnames=fields)
                    logger.writeheader()
                    for i in range(len(song)):
                        logger.writerow({'Rank': rank[i], 'Song': song[i], 'Artist': artist[i]})
print('Successfully wrote all data')


