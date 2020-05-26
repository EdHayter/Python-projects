"""
Pubmed scraper
Search in pubmed and copy the url to the url variable below. make sure &page=1 is added to the end
Name the csv file you want in 'output_file' and set the number of pages you want to scrape
Collects: abstract, article type (review, clinical trial), authors, doi, first author
last author, journal (shorthand), pubmed ID, title, year of publication, number of citations
Ed Hayter 21/05/20
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as ureq
import pandas as pd

#url. check '&page=1' is on the end.
url = 'https://pubmed.ncbi.nlm.nih.gov/?term=circadian&filter=years.2015-2020&size=200&page=1'
#name file to output
output_file = 'test.csv'
#how many pages of papers do you want? [make so: if 0 do all pages]
number_pages_to_scrape = 85

#initialise data as dataFrame
data = pd.DataFrame()
#init error count
error_count=0

#loop over pages
for page in range(29,number_pages_to_scrape):
    #set new url
    nurl = url.replace('page=1','page='+str(page+1))
    
    #grab page html
    uClient = ureq(nurl)
    page_html = uClient.read()
    uClient.close()
    #soup it
    page_soup = soup(page_html,'html.parser')
    #find all articles on page
    articles = page_soup.findAll('article',{'class':'labs-full-docsum'})
    #loop over articles on page 
    for i, article in enumerate(articles):
        #having ureq issues.. 
        try:
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
                abstract = abstract_soup.findAll('div',{'id':'en-abstract'})[0].text.strip().replace('\n','')
            except:
                abstract=''
                
            #number of citations (to date), errors if 0
            try:
                cite = abstract_soup.findAll('em',{'class':'amount'})[0].text
            except: 
                cite = '0'
                
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
                         'Abstract':abstract,
                         'no_citations':cite},ignore_index=True)
            #keep user informed...
            print('Page ' + str(page+1) + ' paper ' + str(i+1) + ' scraped.')
        except:
            print('Error, skipping paper')
            error_count = error_count+1
            
print('Finished! Writing to csv...')
#write CSV
data.to_csv(output_file)    
    
    
