# -*- coding: utf-8 -*-
"""
Web scraping test
Ed Hayter 20/5/20
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as ureq

url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20cards'

#open connection, grab page and save to variable, close.
uClient = ureq(url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html,'html.parser')

#grabs each product
containers = page_soup.findAll('div',{'class':'item-container'})
#open csv to write products to
filename = 'products.csv'
f = open(filename,'w')
headers= 'brand, name, price\n'
f.write(headers)
#loop over each product
for container in containers:
    #scrape brand name
    brand_cont = container.findAll('a',{'class':'item-brand'})
    brand = brand_cont[0].img['title']
    #scrape product name
    title_cont = container.findAll('a',{'class':'item-title'})
    title = title_cont[0].text
    #grab price, convert to float 
    price_cont = container.findAll('li',{'class':'price-current'})
    price = price_cont[0].strong.text+price_cont[0].sup.text
    price = price.replace(',','')
    
    f.write(brand + ',' + title.replace(',','') + ',' + price + '\n')
    # print(brand,'\n',title,'\n',price)
    
f.close()
    