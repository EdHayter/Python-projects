"""
Pubmed scraper
Search in pubmed and copy the url to the url variable below. make sure &page=1 is added to the end
Name the csv file you want in 'output_file' and set the number of pages you want to scrape
Collects: abstract, article type (review, clinical trial), authors, doi, first author
last author, journal (shorthand), pubmed ID, title, year of publication
Ed Hayter 21/05/20

Edit: I realise there is an pubmed option to display abstract on main page, this would 
speed things up, when i get round to it! 
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as ureq
import pandas as pd

#url. check '&page=1' is on the end.
url = 'https://pubmed.ncbi.nlm.nih.gov/?term=circadian+and+cardi*+and+electrophysiology&format=abstract&size=200&page=1'
#name file to output
output_file = 'test.csv'
#how many pages of papers do you want? 
number_pages_to_scrape = 1

#loop over pages
for page in range(number_pages_to_scrape):
    #set new url
    nurl = url.replace('page=1','page='+str(page+1))
    
    #grab page html
    uClient = ureq(nurl)
    page_html = uClient.read()
    uClient.close()
    #soup it
    page_soup = soup(page_html,'html.parser')
    #initialise data as dataFrame
    data = pd.DataFrame()
    #find all articles on page
    articles = page_soup.findAll('article',{'class':'labs-full-docsum'})
    #loop over articles on page 
    for i, article in enumerate(articles):
        #paper title
        title = article.findAll('a',{'class':'labs-docsum-title'})[0].text.strip()
        
        #list of authors
        authors = article.findAll('span',{'class':'labs-docsum-authors full-authors'})[0].text
        
        #take first and last, strip space from last author
        first_author = authors.split(',')[0].strip('.')
        last_author = authors.split(',')[-1].strip().strip('.')
        
        #doi [could use regex?] 
        doi_txt = article.findAll('span',{'class':'labs-docsum-journal-citation full-journal-citation'})[0].text 
        if 'doi' in doi_txt:
            doi = doi_txt.split('doi:')[-1].split('Epub')[0].strip().strip('.')
        else:
            doi = '' 
            
        #journal shorthand
        journal = article.findAll('span',{'class':'labs-docsum-journal-citation short-journal-citation'})[0].text.split('.')[0]
        
        #publication year
        year = article.findAll('span',{'class':'labs-docsum-journal-citation short-journal-citation'})[0].text.split('.')[-2].strip()
        
        #PMID
        pmid = article.findAll('span',{'class':'docsum-pmid'})[0].text
        
        #article type (only papers with 'review' or 'clinical trial' tags on pubmed)
        try:
            article_type = article.findAll('span',{'class':'publication-type spaced-citation-item citation-part'})[0].text.strip('.')
        except:
            article_type = ''
            
        #getting abstract, have to get new URL using PMID
        url_abstract = 'https://pubmed.ncbi.nlm.nih.gov/'+pmid
        uClient = ureq(url_abstract)
        abstract_html = uClient.read()
        uClient.close()
        abstract_soup = soup(abstract_html,'html.parser')
       
        #include try/catch in case no abstract
        try:
            abstract = abstract_soup.findAll('div',{'id':'en-abstract'})[0].text.strip().replace(',','_').replace('\n','')
        except:
            abstract=''
            
        #write to dataFrame 
        data = data.append({'Title':title,
                     'Authors':authors,
                     'First_author':first_author,
                     'Last_author':last_author,
                     'Doi':doi,
                     'Journal':journal,
                     'Year':year,
                     'PMID':pmid,
                     'Article_type':article_type,
                     'Abstract':abstract},ignore_index=True)
        #keep user informed...
        print('Page ' + str(page+1) + ' paper ' + str(i+1) + ' scraped.')
    
print('Finished! Writing to csv...')
#write CSV
data.to_csv(output_file)    
    
    