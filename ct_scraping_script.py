import pandas as pd
import requests 
from bs4 import BeautifulSoup
import re

def data_clean(series):
    return series.str.strip().str.lower().replace('\W','',regex=True)

data=pd.DataFrame()
terms=pd.read_csv('input_data.csv')
terms['term']=terms['term'].str.strip()
i=0   

for val in terms['term']:
    try:
        url = "https://clinicaltrials.gov/ct2/results/details?cond=&term=%s&cntry=&state=&city=&dist=&Search=Search"%(val)
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'lxml')
        dc=soup.findAll("table")[0]
        print(val)
        i=i+1
        print(i)
    
        heading=dc.find_all("tr",{"style":"border-top:1px solid #ccc;"})
        print(len(heading))                          
        if len(heading)>1:      
                    
            breaker=heading[1].text
            test=re.sub(r'\W','',breaker)
            test=test.lower()
            table=pd.read_html(str(dc))
            check=pd.concat(table)
            check.columns=['synonyms','search_results','db_results']
            check['combined']=check.apply(lambda x: ' '.join(x.dropna().astype(str)),  axis=1)
            check['combined']=data_clean(check['combined'])
            if len(check.index[check['combined']==test].tolist())==0:
                final=check.iloc[:-1,:-1]
                search_term=check.iloc[0,0]
                final['search_term']=search_term
                final['is_root']=final['synonyms']==final['search_term']
                data=data.append(final)
            else:   
                ind=check.index[check['combined']==test].tolist()[0]
                final=check.iloc[:ind,:-1]
                search_term=check.iloc[0,0]
                final['search_term']=search_term
                final['is_root']=final['synonyms']==final['search_term']
                data=data.append(final)
        else:
            table=pd.read_html(str(dc))
            check=pd.concat(table)
            check.columns=['synonyms','search_results','db_results']
            check['combined']=check.apply(lambda x: ' '.join(x.dropna().astype(str)),  axis=1)
            check['combined']=data_clean(check['combined'])
            final=check.iloc[:,:]
            search_term=check.iloc[0,0]
            final['search_term']=search_term
            final['is_root']=final['synonyms']==final['search_term']    
            data=data.append(final)
    except:
        print("error")
        
data.to_csv('ct_scraping_results.csv',index=False)

