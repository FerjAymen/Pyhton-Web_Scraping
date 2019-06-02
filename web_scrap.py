from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient
class offre():
    def __init__(self):
        self.name=""
        self.link=""
        self.offre_description=""
        self.expiration_date=""

def get_offre_list(offre,url):
    offre_list=[]
    driver = webdriver.Chrome(executable_path= r'/usr/local/bin/chromedriver')
    driver.get(url)
    doc = driver.page_source
    soup = BeautifulSoup(doc, 'html.parser')
    div1 = soup.find('div', class_='search-results col-xs-12 col-sm-9')
    #print(div)
    for article in div1.find_all('article'):
        for div2 in article.find_all('div', class_='media-body'):
            for div3 in div2.find_all('div', class_='media-heading listing-item__title'):
                for a in div3.find_all('a'):
                    #print(a.text)
                    #print(a['href'])
                    new_offre= offre()
                    new_offre.name=a.text
                    new_offre.link=a['href']
                    offre_list.append(new_offre)
   # for offre in offre_list:
    #    print(offre.name)
     #   print(offre.link) '''
                

    #driver.quit()
    return offre_list
#get_offre_list(offre)
def get_detail_of_all_offer(offre_list):
    driver = webdriver.Chrome(executable_path= r'/usr/local/bin/chromedriver')
    for o in offre_list[0:2]:
        url=o.link
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        description_de_lemploi=""
        div1 = soup.find('div', class_='details-body__content content-text')
        p=div1.find('p')
        description_de_lemploi=p.text + '\n'
        for pp in p.find_next_siblings():
            description_de_lemploi=description_de_lemploi + pp.text + '\n'
        date_dexpiration=""
        date_dexpiration=soup.find('h3', string="Date d'expiration").find_next().text
        o.offre_description=description_de_lemploi
        o.expiration_date=date_dexpiration

    #driver.quit()
    return offre_list
def get_all():
    driver = webdriver.Chrome(executable_path= r'/usr/local/bin/chromedriver')
    url = 'https://www.tanitjobs.com/jobs/?searchId=1554304169.1879&action=search'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    div_page=soup.find('div', class_='pagination-top')
    page_num = int(div_page.find_all('span')[len(div_page.find_all('span')) - 1].text)
    #print(page_num)
    page_url=[]
    for page in range(1,page_num + 1):
        new_url = url + '&page{0}'.format(page)
        #print(new_url)
        page_url.append(new_url)
    return(page_url)
    

client = MongoClient('mongodb://127.0.0.1:27017/')
db=client.scrapdb
#print(db)
col=db.Offre
x= get_all()
l=[[]]
for a in x[0:3]:
    offre_list= get_detail_of_all_offer(get_offre_list(offre,a))
    for p in offre_list[0:2]:
        doc={"name": str(p.name), "link": str(p.link), "offre_description": str(p.offre_description), "expiration_date": str(p.expiration_date)}
        insert=col.insert_one(doc)
        print('\n')
        print(p.name)
        print(p.link)
        print(p.offre_description)
        print(p.expiration_date)
        print('\n')
        
            

        
        
        
  
