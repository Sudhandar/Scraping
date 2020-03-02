import pandas as pd
import requests 
from bs4 import BeautifulSoup

def data_clean(series):
    return series.str.strip().str.lower().replace('\W','',regex=True)

data=pd.read_csv('drugs_a.csv')
drugs=[]
final=pd.DataFrame()
for val in data['terms']:
    url = "https://www.drugs.com/international-%s.html"%(val)
    r = requests.get(url) 
    print(val)
    soup = BeautifulSoup(r.content, 'html5lib')
    dc=soup.select(".sitemap-list a")
    for val in dc:
        drugs.append(val.text)

final=pd.DataFrame(drugs)
final=final.drop_duplicates()
final.columns=['name']
final.to_csv('drugsdotcom_international_drugs.csv',index=False)
