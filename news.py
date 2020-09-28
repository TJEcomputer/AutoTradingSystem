import random
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import csv


header = {'User-Agent': 'Mozilla/5.0'}
pageNum = 1
saveTocsv = []
tmp = []

while pageNum:
    url = f'https://kr.investing.com/news/stock-market-news/{pageNum}'

    request = urllib.request.Request(url, headers=header)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find_all(class_="js-external-link title")

    for i in title:
        print(i.attrs['href'])
        print(i.attrs['title'])

        tmp = [[i.attrs['href']],[i.attrs['title']]]
        saveTocsv.append(tmp)



    with open('saved.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['link', 'title'])
        writer.writerow(saveTocsv)

    pageNum += 1
    print(str(pageNum)+'페이지 완료')
    time.sleep(random.uniform(1,10))