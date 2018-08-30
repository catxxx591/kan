
# coding: utf-8

# In[85]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json
import re
from lxml import html




#做出 href清單dict   { name : href } = { 'Aquila' : '/kancolle/Aquila' }

def getshipdict():
    url = 'https://wikiwiki.jp/kancolle/%E8%89%A6%E5%A8%98%E5%90%8D%E4%B8%80%E8%A6%A7%EF%BC%88%E8%89%A6%E7%A8%AE%E5%88%A5%EF%BC%89'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    soup
    shipdict={}
    for p in soup.find_all('p')[11:47]:
        for a in p.find_all('a'):
            href = str(a).split('"')[1]
            name = str(a).split('"')[3]
#            print(name,end=',')
            shipdict[name] = href
    #    p += 1
    return shipdict


# In[90]:


"""shipdict =  getshipdict()
shipdict"""


# In[91]:


# 用 href清單 轉換URL 取得 soup

def getsoup(n):
    url = 'https://wikiwiki.jp'#/kancolle/%E9%87%91%E5%89%9B
    url = url + n#str(list(shipdict.values())[n])
#    print(str(list(shipdict.values())[n]))
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    return soup


# In[92]:


# 取得 船的類別資料 columns=[ no , name , type , class ]

def getwikiclass():
    shipdict =  getshipdict()
    df = pd.DataFrame()
    i = 0
    for n in list(shipdict.values()):
        soup = getsoup(n)
        no = soup.find_all('div',{'id':'body'})[0].find_all('tr')[0].text
        shiptype = soup.find_all('div',{'id':'body'})[0].find_all('tr')[1].find_all('td')[2].text.split(' ')[-1]
        shipclass = soup.find_all('div',{'id':'body'})[0].find_all('tr')[1].find_all('td')[2].text.split(' ')[0]
        shipname = list(shipdict.keys())[i]
        data = pd.DataFrame([[no,shipname,shiptype,shipclass]])
        df = pd.concat([df,data])
        if i % 20 == 0:
            print(i,end=",")
        i += 1
    df.columns = ['no','name','type','class']
    #df.set_index('no',inplace=True)
    df['no'] = df['no'].apply(lambda x:x.split('.')[-1])
    wikiclass = df
    
    wikiclass['type']= wikiclass['type'].apply(lambda x : x.replace("*1",""))
    replacedict={'護衛駆逐艦DE-413':'駆逐艦','神風型駆逐艦　5番艦':'駆逐艦','綾波型駆逐艦　5番艦':'駆逐艦','呂号潜水艦':'潜水艦','三式潜航輸送艇':'潜水艦'}
    n = 0
    while n < len(list(replacedict.keys())):
        wikiclass['type']= wikiclass['type'].apply(lambda x : x.replace(list(replacedict.keys())[n],list(replacedict.values())[n]))
        n += 1
    wikiclass['class']= wikiclass['class'].apply(lambda x : x.replace('神風型駆逐艦　5番艦','神風型'))
    wikiclass['class']= wikiclass['class'].apply(lambda x : x.replace('綾波型駆逐艦　5番艦','綾波型'))

    return wikiclass


# In[93]:


"""wikiclass = getwikiclass()
wikiclass"""


# In[94]:


# 檢查船的 type 欄位

'''types = wikiclass.groupby('type').count()
types.index'''


# In[95]:


# 修正 type欄位

'''wikiclass['type']= wikiclass['type'].apply(lambda x : x.replace("*1",""))
replacedict={'護衛駆逐艦DE-413':'駆逐艦','神風型駆逐艦　5番艦':'駆逐艦','綾波型駆逐艦　5番艦':'駆逐艦','呂号潜水艦':'潜水艦','三式潜航輸送艇':'潜水艦'}
n = 0
while n < len(list(replacedict.keys())):
    wikiclass['type']= wikiclass['type'].apply(lambda x : x.replace(list(replacedict.keys())[n],list(replacedict.values())[n]))
    n += 1
wikiclass.groupby('type').count()'''


# In[96]:


# 檢查船的 class 欄位

'''classes = wikiclass.groupby('class').count()
classes.index'''


# In[97]:


#修正 class欄位

'''wikiclass['class']= wikiclass['class'].apply(lambda x : x.replace('神風型駆逐艦　5番艦','神風型'))
wikiclass['class']= wikiclass['class'].apply(lambda x : x.replace('綾波型駆逐艦　5番艦','綾波型'))
wikiclass['class'].head()'''


# In[98]:


# 檢查 wikiclass

#wikiclass


# In[99]:


# 爬取ship 詳細資料 回傳 dict

"""def getd():
    url = 'https://github.com/KC3Kai/KC3Kai/blob/master/src/data/WhoCallsTheFleet_ships.nedb'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    soup
    soup = soup.find('table',{'class':'highlight tab-size js-file-line-container'})
    soup
    shipdict2 = soup.find_all('td',{'class':'blob-code blob-code-inner js-file-line'})[1].text
    d = json.loads(shipdict2)
    stat = d['stat']
    stat.values()
    return d"""


# In[100]:


#soup = soup.find('table',{'class':'highlight tab-size js-file-line-container'})
#soup


# In[101]:


'''
shipdict2 = soup.find_all('td',{'class':'blob-code blob-code-inner js-file-line'})[1].text
d = json.loads(shipdict2)
stat = d['stat']
stat.values()
d
'''


# In[102]:


'''
shipid = d['id']
shipname = no_dict[str(d['no'])]
shipclass = d['class']
shiptype = d['type']
df = pd.DataFrame([[shipid,shipname]],columns=['no','name'])
'''


# In[103]:


'''df= getwikiclass()
str('353') in list(df['no'])
#list(df['no'])
shipname = '伊13改'
df.loc[df['name']==shipname,'no'][0]'''


# In[104]:


#df = getwikiclass()


# In[105]:


#df.head()


# In[106]:


#df.loc[df['no']== '022' ]['name'][0]


# In[107]:


# 爬取 ship詳細資料 和 wikiclass 做出 dataframe

def getdata():
    
#    shipdict =  getshipdict()
    df = getwikiclass()    
    url = 'https://github.com/KC3Kai/KC3Kai/blob/master/src/data/WhoCallsTheFleet_ships.nedb'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
#    d = getd()
    data = pd.DataFrame()
    
    
    n=0
    while n < len(soup.find_all('td',{'class':'blob-code blob-code-inner js-file-line'})):
#        print(n,end=',')
        shipdict = soup.find_all('td',{'class':'blob-code blob-code-inner js-file-line'})[n].text
        d = json.loads(shipdict)
        stat = d['stat']
        shipnum = d['no']

        while len(str(shipnum)) < 3:
            shipnum = '0'+str(shipnum)
        shipnumstr = shipnum
#        print(shipnumstr)
#        print(n)
#        print(str(shipnumstr) in list(df['no']))

        if (str(shipnumstr) in list(df['no'])) == True:
#            print('T')
            name = df.loc[df['no']== str(shipnumstr) ]['name'][0]
            shipname = name
        else:
            if int(d['no']) > 999:
                shipname = str(d['name']['ja_jp']).replace("\n","")+'改'
                shipnumstr = df.loc[df['name']==shipname,'no'][0]
            else:
                n+=1
                continue
            
#        print(shipnumstr,shipname)    
        shipclass = df.loc[df['name']==shipname,'class'][0]
        shiptype = df.loc[df['name']==shipname,'type'][0]
        df1 = pd.DataFrame([[shipnumstr,shipname,shiptype,shipclass]],columns=['no','name','type','class'])
        df2 = pd.DataFrame([list(stat.values())],columns=list(stat.keys()))
        data0 = df1.join(df2)
        if n == 0:
            data = data0
#            print('go')
        while n > 0:
            #data.join(data0)
            m = pd.concat([data,data0],ignore_index=True)
            data = m
#            n += 1
            break
    
#        if n % 20 ==0:
#            print(n,end=",")
        n += 1
    poi = data
    poi[poi.columns[[0,2,3,19,20]]] = poi[poi.columns[[0,2,3,19,20]]].apply(lambda x: x.astype('str'))
    poi.sort_values('no',inplace=True)
    poi.set_index('no',inplace=True)
    poi.reset_index(inplace=True)
    return poi
        


# In[108]:


#poi = getdata()
#poi


# In[109]:


"""poi.dtypes"""


# In[110]:


"""poi[poi.columns[[0,2,3,19,20]]] = poi[poi.columns[[0,2,3,19,20]]].apply(lambda x: x.astype('str'))
poi.dtypes"""


# In[111]:


#poi.head()


# In[112]:


"""poi.sort_values('no',inplace=True)
poi.set_index('no',inplace=True)
"""


# In[113]:


"""poi.set_index('no',inplace=True)
poi.reset_index(inplace=True)
poi"""


from sqlalchemy import create_engine
import pymysql
engine = create_engine('mysql+pymysql://root@127.0.0.1:3306/datamining?charset=utf8')

# if_exists = 'append' -->發現重複table,增加在後面　# if_exists = 'replace'-->完整取代
#poi.to_sql(name='poi',con=engine,  if_exists = 'replace', index=False)

connect = pymysql.Connect(
#    host='localhost',
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='datamining',
    charset='utf8'
)

cursor = connect.cursor()
sql = ('SELECT * FROM datamining.poi;')
cursor.execute(sql)
def getsqldata():
    s_poi = pd.read_sql(sql=sql,con=connect)
    return s_poi

