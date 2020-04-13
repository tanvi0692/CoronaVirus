import urllib.request, json 

with urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json") as url:
    data = json.loads(url.read().decode())
    
import json 
import csv
import copy
import pandas as pd
import argparse
import matplotlib.pyplot as plt


def getValue(keys,value):
    key = keys.split('.')
    num,n = len(key)-1, 0
    while n<=num:
        try:
            value = value[key[n]]
            n+=1
        except KeyError:
            value = None
            break
    return value

def getKeys(data):  
    if not isinstance(data,dict):
        return ['']
    res_ = []
    for key in data.keys():
            temp = copy.deepcopy(getKeys(data[key]))
            for i, element in enumerate(temp):
                if element == '':
                    temp[i]= key
                else:
                    temp[i]= key+"."+ element
                res_.append(temp[i])
    return res_
    
if __name__=='__main__':

    with urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json") as url:
        data = json.loads(url.read().decode())
    
    countries = list(data.keys())
    keyList = getKeys(data[countries[0]][0])
    frame = []
    for country in countries:
        CountryData = {key: [] for key in keyList} 
        for value in data[country]:
            for item in keyList:
                CountryData[item].append(getValue(item,value))

        df = pd.DataFrame(CountryData)
        df['Country'] = df.apply(lambda x: country, axis=1)
        frame.append(df)
        result = pd.concat(frame)
    print(type(result))
    result.to_csv('{}.csv'.format('corona'), sep='\t')
    #result.plot(x ='date',y = keyList[1:])
    


    
                     
            
    