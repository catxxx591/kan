
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import requests
import json
from bs4 import BeautifulSoup


# In[2]:





def ship_dict(n1,n2 = 0):
    data = pd.DataFrame()
    if n2 < n1:
        n2 = n1
    ship = n1
    shipdic={}
    while ship <= n2:
        url = ('https://db.kcwiki.org/construction/ship/'+str(ship)+'.json')
        try:
            j_in = pd.read_json(url)
        except ValueError:
            continue
        else:

            j_in = pd.read_json(url)
            df1 = pd.DataFrame(j_in)
            df2 = df1['data']
            #type(df2)  pandas.core.series.Series
            #type(df2[1]) dict


            ##############################################################################
            url= requests.get('https://db.kcwiki.org/construction/ship/'+str(ship)+'.html')
            soup = BeautifulSoup(url.text, 'html.parser')
            title= soup.title
            #type(title) bs4.element.Tag
            title=title.text
            name = title.split('-')[2][1:]
#建立艦娘清單
            if name != None:
                shipdic[name] = ship
        finally:
            ship += 1
    
    return shipdic





def recipe_num(n1,n2 = 0,group = 'off'):
    data = pd.DataFrame()
    if n2 < n1:
        n2 = n1
    ship = n1
    shipdic={}
    while ship <= n2:
        url = ('https://db.kcwiki.org/construction/ship/'+str(ship)+'.json')
        try:
            j_in = pd.read_json(url)
        except ValueError:
            continue
        else:

            j_in = pd.read_json(url)
            df1 = pd.DataFrame(j_in)
            df2 = df1['data']
            #type(df2)  pandas.core.series.Series
            #type(df2[1]) dict


            ##############################################################################
            url= requests.get('https://db.kcwiki.org/construction/ship/'+str(ship)+'.html')
            soup = BeautifulSoup(url.text, 'html.parser')
            title= soup.title
            #type(title) bs4.element.Tag
            title=title.text
            name = title.split('-')[2][1:]
#建立艦娘清單
            if name != None:
                shipdic[ship] = name
                (NAME,SHIP)=(1,'a')
                print(name,end = "")
            n = 0
            while n <= len(df2)-1:
                record = df2[n]  #每一筆建造紀錄
                df0 = pd.DataFrame(columns=['oil','bullet','steel','Al','materials','rate'])
                recipe = record['recipe']
                rate = record['rate']
#                print(rate)
#篩選大造配方
                if rate < 20 and int(recipe[0])>1000:
#                    if NAME != name :
#                        print(name)
                    df = pd.DataFrame([[name,recipe[0],recipe[1],recipe[2],recipe[3],recipe[4],record['usedCount'],rate]])#,columns=['name','oil','bullet','steel','Al','materials','rate'])
                    data = pd.concat([data,df])
                    (NAME,SHIP)=(name,ship)
#打開群組
                    count = 1
                    if group == 'on':
                        while count <= int(record['usedCount']):
                            data = pd.concat([data,df])
#                            print(data)
                            count += 1
#                    data['usedCount'] = record['usedCount']
                n += 1
            if (NAME,SHIP)==(name,ship):
                print((NAME,SHIP),end = "")
        finally:
            ship += 1

        #data = pd.concat([df0,df])
        #data.insert(0,'name',name)
        #print(df)
    if group == 'on':
        df0 = pd.DataFrame(columns=['name','oil','bullet','steel','Al','materials','rate'])
    df0 = pd.DataFrame(columns=['name','oil','bullet','steel','Al','materials','uesdCount','rate'])
    
    try:
        data.columns = df0.columns 
        return data
    except ValueError:
        print(shipdic)
        print('無大造艦娘資料')





def recipe_name(*names,group = 'off'):
    
    shipdic={}
    data = pd.DataFrame()
    
    for name in names:
        ship = ship_all[str(name)]
        while ship != None:
            url = ('https://db.kcwiki.org/construction/ship/'+str(ship)+'.json')
            try:
                j_in = pd.read_json(url)
            except ValueError:
                continue
            else:

                j_in = pd.read_json(url)
                df1 = pd.DataFrame(j_in)
                df2 = df1['data']
                #type(df2)  pandas.core.series.Series
                #type(df2[1]) dict


                ##############################################################################
                url= requests.get('https://db.kcwiki.org/construction/ship/'+str(ship)+'.html')
                soup = BeautifulSoup(url.text, 'html.parser')
                title= soup.title
                #type(title) bs4.element.Tag
                title=title.text
                name = title.split('-')[2][1:]

    #建立艦娘清單
                if name != None:
                    shipdic[ship] = name
    #                print(name)
                n = 0
                while n <= len(df2)-1:
                    record = df2[n]  #每一筆建造紀錄
                    df0 = pd.DataFrame(columns=['oil','bullet','steel','Al','materials','rate'])
                    recipe = record['recipe']
                    rate = record['rate']
    #                print(rate)
    #篩選大造配方
                    if rate < 20 and int(recipe[0])>1000:
                        df = pd.DataFrame([[name,recipe[0],recipe[1],recipe[2],recipe[3],recipe[4],record['usedCount'],rate]])#,columns=['name','oil','bullet','steel','Al','materials','rate'])
                        data = pd.concat([data,df])
                        count = 1
    #打開群組
                        if group == 'on':
                            while count <= int(record['usedCount']):
                                data = pd.concat([data,df])
    #                            print(data)
                                count += 1
    #                    data['usedCount'] = record['usedCount']
                    n += 1
            finally:
    #            ship += 1
                break

            #data = pd.concat([df0,df])
            #data.insert(0,'name',name)
            #print(df)
    if group == 'on':
        df0 = pd.DataFrame(columns=['name','oil','bullet','steel','Al','materials','rate'])
    df0 = pd.DataFrame(columns=['name','oil','bullet','steel','Al','materials','uesdCount','rate'])
    
    try:
        data.columns = df0.columns 
        return data
    except ValueError:
        print(shipdic)
        print('無大造艦娘資料')



