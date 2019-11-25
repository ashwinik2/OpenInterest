import requests
import api_key
import json
from collections import OrderedDict
from pandas.io.json import json_normalize
import csv
import pandas as pd
from pandas import DataFrame
from datetime import date
from datetime import datetime
import time
import os
import os.path
import datetime
from os import path

endpoint = r"https://api.tdameritrade.com/v1/marketdata/chains"
stockSymbol = []
stockExpDate =[]
stockOptionExpDate = []
stockStrikeprice = []
stockOptionType = []
stockCsvFiles = []
todayDate = []
expDate = []
loadopenInterest =[] 
stockStrikepricesList = []
stockOptionSymbolList = []
stockOptionExpDateList = []
global totalStocks
global totalStrikePrices_Alldates
global CSVOptionSymbolList
global totalCols
global optionPrice
global optionVolume
global num
global StockPrice
global StockVolume
import sys


csv.field_size_limit(sys.maxsize)

contractType =['CALL','PUT']
strikeCount = 20

date_format = '%m/%d/%y'

ofilepath = './output/'

ifilepath = './input/'
ifilestocklist = ifilepath+'StockList.csv'
     
def validateDtae(date_text):
    try:
        if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        date_text = datetime.datetime.strptime(date_text, date_format).date()
        return date_text
        
def generateTotalStockList():
    global totalStocks
    with open(ifilestocklist) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        fields = next(readCSV)
        for row in readCSV:
            stocksymbol = row[0]
            stockoptionExpDate = row[1]

            stockSymbol.append(stocksymbol)
            
            print("stockexpdate is before validating:",stockoptionExpDate)    
            formatedDate = validateDtae(stockoptionExpDate)
            print("result is :",formatedDate)

            if(formatedDate == True):
                print("result is :",formatedDate)
                stockOptionExpDate.append(stockoptionExpDate)
            else:
                stockOptionExpDate.append(str(formatedDate))
            
        print(stockSymbol)
        print(stockOptionExpDate)
        totalStocks = len(stockSymbol)
        print("Number of Stocks in OptionChainList is  : % 2d" %(totalStocks))
##def generateTotalStockList():
##    global totalStocks
##    with open('StockList.csv') as csvfile:
##        readCSV = csv.reader(csvfile, delimiter=',')
##        fields = next(readCSV)
##        for row in readCSV:
##            stocksymbol = row[0]
##            stockoptionExpDate = row[1]
##            stockSymbol.append(stocksymbol)
##            stockOptionExpDate.append(stockoptionExpDate)
##        print(stockSymbol)
##        print(stockOptionExpDate)
##        totalStocks = len(stockSymbol)
##        print("Number of Stocks in OptionChainList is  : % 2d" %(totalStocks))

def generateStockCSVFiles(index,stockIndex):       
    stockCsvfilename = ofilepath + stockSymbol[stockIndex]+'_'+stockOptionExpDate[stockIndex]+'_'+contractType[index]+'.csv'
    print(stockSymbol)
    print(stockOptionExpDate)
    print(stockCsvfilename)
    return stockCsvfilename

def getStockCSVFiles(index,stockIndex):       
    stockCsvfilename = ofilepath + stockSymbol[stockIndex]+'_'+stockOptionExpDate[stockIndex]+'_'+contractType[index]+'.csv'
    return stockCsvfilename

def getStockOptionExpDates(symbol,expDate,index):
        global stockOptionExpDateList
        payload = {'apikey':api_key.API_KEY,
               'symbol':symbol,
               'contractType':contractType[index],
                'strikeCount':strikeCount,
               'includeQuotes':'TRUE',
               'strategy':'SINGLE',   
               'toDate':expDate,
               'optionType':'S'
               }
        content = requests.get(url = endpoint, params = payload)
        data = content.json()
        with open('OptionsDataBase.json', 'w') as outfile:
            json.dump(data, outfile)
        with open('OptionsDataBase.json', 'r') as f:
           optionsData_dict = json.load(f)
       
        def firstkey(key,dictionary):
            for k, value in data.items():
                if k == key:
                    yield value

        def findSymbolKey(key, dictionary):
            for k, v in dictionary.items():
                if k == key:
                    if v != getStockOptionSymbol[0]:
                        yield v               
                elif isinstance(v, dict):
                    for result in findSymbolKey(key, v):
                        if v != getStockOptionSymbol[0]:
                            yield result
                elif isinstance(v, list):
                    if v != getStockOptionSymbol[0]:
                        for d in v:
                            for result in findSymbolKey(key, d):
                                yield result

        def findexpirationDateKey(key, dictionary):
            tt =0
            for k, v in dictionary.items():
                if k == key:
                    if v != getStockOptionSymbol[0]:
                        yield v               
                elif isinstance(v, dict):
                    for result in findSymbolKey(key, v):
                        if v != getStockOptionSymbol[0]:
                            t = datetime.datetime.fromtimestamp(float(result)/1000.)
                            t = t.strftime("%Y-%m-%d")
                            yield t
                            
                elif isinstance(v, list):
                    if v != getStockOptionSymbol[0]:
                        for d in v:
                            for result in findkey(key, d):
                                yield result

        
        getStockOptionSymbol = list(firstkey('symbol',optionsData_dict))
        stockoptionexpDateList = list(findexpirationDateKey('expirationDate',optionsData_dict))
        print("length of optionExpiration Dates is :",len(stockoptionexpDateList)) 
        
        if(len(stockoptionexpDateList) != 0):
            stockOptionExpDateList = stockoptionexpDateList
            
            return stockoptionexpDateList
        else:
            print("length of optionExpiration Dates  in else is :",len(stockoptionexpDateList))
            del stockOptionExpDateList[:]
            print("length of optionExpiration Dates  stockOptionExpDateList ='' in else is :",len(stockOptionExpDateList))
            return 0

def getOptionsStrikePrice(symbol,expDate,index):
        global stockStrikepricesList
        global stockOptionSymbolList
        payload = {'apikey':api_key.API_KEY,
            'symbol':symbol,
            'contractType':contractType[index],
            'strikeCount':strikeCount,
            'includeQuotes':'TRUE',
            'strategy':'SINGLE',   
            'toDate':expDate,
            'optionType':'S'
        }
        content = requests.get(url = endpoint, params = payload)
        data = content.json()
        with open('OptionStrike.json', 'w') as outfile:
            json.dump(data, outfile)
        with open('OptionStrike.json', 'r') as f:
           optionsData_dict = json.load(f)
       
        def firstkey(key,dictionary):
            for k, value in data.items():
                if k == key:
                    yield value

        def findStrikePriceKey(key, dictionary):
            for k, v in dictionary.items():
                if k == key:
                    if v != getStockOptionSymbol[0]:
                        yield v
                        
                elif isinstance(v, dict):
                    for result in findStrikePriceKey(key, v):
                        if v != getStockOptionSymbol[0]:
                            yield result
                elif isinstance(v, list):
                    if v != getStockOptionSymbol[0]:
                        for d in v:
                            for result in findStrikePriceKey(key, d):
                                yield result

        def findSymbolKey(key, dictionary):
            for k, v in dictionary.items():
                if k == key:
                    if v != getStockOptionSymbol[0]:
                        yield v
                        
                elif isinstance(v, dict):
                    for result in findSymbolKey(key, v):
                        if v != getStockOptionSymbol[0]:
                            yield result
                elif isinstance(v, list):
                    if v != getStockOptionSymbol[0]:
                        for d in v:
                            for result in findSymbolKey(key, d):
                                yield result

        getStockOptionSymbol = list(firstkey('symbol',optionsData_dict))
        stockOptionSymbolList = list(findSymbolKey('symbol',optionsData_dict))
        stockStrikepricesList = list(findStrikePriceKey('strikePrice',optionsData_dict))
        totalStrikePrices_Alldates = len(stockStrikepricesList)

def getOpenInterest(symbol,expDate,strikePrice,optionType):
    global optionVolume
    global optionPrice
    global StockVolume
    global StockPrice
    
   # print("symbol,expDate,strikePrice,optionType is :",symbol,expDate,strikePrice,optionType)
    payload = {'apikey':api_key.API_KEY,
            'symbol':symbol,
            'contractType':optionType,
            'includeQuotes':'TRUE',
            'strategy':'SINGLE',            
            'strike':strikePrice,
            'fromDate':expDate,
            'toDate':expDate,
            'optionType':'S'
        }
    content = requests.get(url = endpoint, params = payload)
    data = content.json()
    with open('OpenInterest.json', 'w') as outfile:
        json.dump(data, outfile)
    with open('OpenInterest.json', 'r') as f:
       optionsData_dict = json.load(f)
   
    def findSymbolKey(key,dictionary):
        for k, value in data.items():
            if k == key:
                yield value

    def findopenInterestKey(key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                if v != getStockOptionSymbol[0]:
                    yield v
                    
            elif isinstance(v, dict):
                for result in findopenInterestKey(key, v):
                    if v != getStockOptionSymbol[0]:
                        yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findopenInterestKey(key, d):
                            yield result

    def findoptionVolumeKey(key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                if v != getStockOptionSymbol[0]:
                    yield v
                    
            elif isinstance(v, dict):
                for result in findoptionVolumeKey(key, v):
                    if v != getStockOptionSymbol[0]:
                        yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findoptionVolumeKey(key, d):
                            yield result
    def findoptionPriceKey(key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                if v != getStockOptionSymbol[0]:
                    yield v
                    
            elif isinstance(v, dict):
                for result in findoptionPriceKey(key, v):
                    if v != getStockOptionSymbol[0]:
                        yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findoptionPriceKey(key, d):
                            yield result

    getStockOptionSymbol = list(findSymbolKey('symbol',optionsData_dict))
    print("getStockOptionSymbol is :",getStockOptionSymbol)
    loadopenInterest = list(findopenInterestKey('openInterest',optionsData_dict))    
    optionvolume = list(findoptionVolumeKey('totalVolume',optionsData_dict))
    print("optionvolume is in getOpenINterest is :",optionvolume)
##    if(len(optionvolume) != 0):
##        StockVolume = optionvolume[0]
##        optionVolume = optionvolume[1]
##    else:
##        StockVolume = 0
##        optionVolume = optionvolume
##
##    optionprice = list(findoptionPriceKey('last',optionsData_dict))
##    if(len(optionprice) != 0):
##        StockPrice = optionprice[0]
##        optionPrice = optionprice[1]
##    else:
##        StockPrice= 0
##        optionPrice = optionprice
##        


    
    if(optionType == 'CALL'):
        if(len(optionvolume) != 0):
            StockVolume = optionvolume[1]
            optionVolume = optionvolume[0]
        else:
            StockVolume = 0
            optionVolume = optionvolume
    else:
        if(len(optionvolume) != 0):
            StockVolume = optionvolume[0]
            optionVolume = optionvolume[1]
        else:
            StockVolume = 0
            optionVolume = optionvolume
        
    print("optionvolume is in getOpenINterest is :",optionVolume)
    optionprice = list(findoptionPriceKey('last',optionsData_dict))
    if(optionType == 'CALL'):
        if(len(optionprice) != 0):
            StockPrice = optionprice[1]
            optionPrice = optionprice[0]
        else:
            StockPrice= 0
            optionPrice = optionprice
    else:
        if(len(optionprice) != 0):
            StockPrice = optionprice[0]
            optionPrice = optionprice[1]
        else:
            StockPrice= 0
            optionPrice = optionprice
        
    print("symbol,loadopenInterest,optionvolume,optionprice in  getOpenInterest from TD:",symbol,loadopenInterest,optionVolume,optionPrice)
    return loadopenInterest

def getOpenInterestFromJson(symbol):
    global loadopenInterest
    global optionVolume
    global optionPrice
    
    with open('OptionsDataBase.json', 'r') as f:
       optionsData_dict = json.load(f)
       
    def firstkey(key,dictionary):
        for k, value in optionsData_dict.items():
            if k == key:
                yield value


    def findOpenInterestKey(key, dictionary):
        global loadopenInterest
        
        optionSymbolExist =0
        value = symbol
        for k, v in dictionary.items():
            if k == 'symbol':
                if(v == value):
                    optionSymbolExist += 1
        if(optionSymbolExist == 1):
            for k, v in dictionary.items():
                if k == key:
                    loadopenInterest = v
                    yield v
   #     return v

    def findOptionVolume(key, dictionary):
        global optionVolume        
        optionSymbolExist =0
        value = symbol
        for k, v in dictionary.items():
            if k == 'symbol':
                if(v == value):
                    optionSymbolExist += 1
        if(optionSymbolExist == 1):
            for k, v in dictionary.items():
                if k == key:
                    optionVolume = v
                    yield v
    #    return v

    def findOptionPrice(key, dictionary):
        global optionPrice        
        optionSymbolExist =0
        value = symbol
        for k, v in dictionary.items():
            if k == 'symbol':
                if(v == value):
                    optionSymbolExist += 1
        if(optionSymbolExist == 1):
            for k, v in dictionary.items():
                if k == key:
                    optionPrice = v
                    yield v
     #   return v
            
    def findSymbolKey(key, dictionary):
        global loadopenInterest
        for k, v in dictionary.items():
            if k == key:
                if(v == symbol):
                    yield v
    
            elif isinstance(v, dict):
                for result in findSymbolKey(key, v):
                    if v != getStockOptionSymbol[0]:
                        if(result == symbol):                            
                            break
                            
                            yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findOpenInterestKey('openInterest', d):
                            loadopenInterest = result
                            break
                            if(result == symbol):
                                yield result
                        for result in findOptionVolume('totalVolume', d):
                            optionVolume = result
                            break
                            if(result == symbol):
                                yield result
                        for result in findOptionPrice('last', d):
                            optionPrice = result
                            break
                            if(result == symbol):
                                yield result
            
            
    getStockOptionSymbol = list(firstkey('symbol',optionsData_dict))
    stockOptionSymbol = list(findSymbolKey('symbol',optionsData_dict))
    print("symbol :, loadopenInterest : optionVolume :,optionPrice : from json ",symbol,loadopenInterest,optionVolume,optionPrice)
    return loadopenInterest

def getOpenInterestFromJson1(symbol):
    global loadopenInterest
    global optionVolume
    global optionPrice
    with open('OptionStrike.json', 'r') as f:
       optionsData_dict = json.load(f)
       
    def firstkey(key,dictionary):
        for k, value in optionsData_dict.items():
            if k == key:
                yield value


    def findOpenInterestKey(key, dictionary):
        global loadopenInterest
        
        optionSymbolExist =0
        value = symbol
        for k, v in dictionary.items():
            if k == 'symbol':
                if(v == value):
                    optionSymbolExist += 1
        if(optionSymbolExist == 1):
            for k, v in dictionary.items():
                if k == key:
                    loadopenInterest = v
                    yield v
   #     return v

    def findOptionVolume(key, dictionary):
        global optionVolume        
        optionSymbolExist =0
        value = symbol
        for k, v in dictionary.items():
            if k == 'symbol':
                if(v == value):
                    optionSymbolExist += 1
        if(optionSymbolExist == 1):
            for k, v in dictionary.items():
                if k == key:
                    optionVolume = v
                    yield v
    #    return v

    def findOptionPrice(key, dictionary):
        global optionPrice        
        optionSymbolExist =0
        value = symbol
        for k, v in dictionary.items():
            if k == 'symbol':
                if(v == value):
                    optionSymbolExist += 1
        if(optionSymbolExist == 1):
            for k, v in dictionary.items():
                if k == key:
                    optionPrice = v
                    yield v
     #   return v
            
    def findSymbolKey(key, dictionary):
        global loadopenInterest
        for k, v in dictionary.items():
            if k == key:
                if(v == symbol):
                    yield v
    
            elif isinstance(v, dict):
                for result in findSymbolKey(key, v):
                    if v != getStockOptionSymbol[0]:
                        if(result == symbol):                            
                            break
                            
                            yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findOpenInterestKey('openInterest', d):
                            loadopenInterest = result
                            break
                            if(result == symbol):
                                yield result
                        for result in findOptionVolume('totalVolume', d):
                            optionVolume = result
                            break
                            if(result == symbol):
                                yield result
                        for result in findOptionPrice('last', d):
                            optionPrice = result
                            break
                            if(result == symbol):
                                yield result
            
            
    getStockOptionSymbol = list(firstkey('symbol',optionsData_dict))
    stockOptionSymbol = list(findSymbolKey('symbol',optionsData_dict))
    print("symbol :, loadopenInterest : optionVolume :,optionPrice : from json ",symbol,loadopenInterest,optionVolume,optionPrice)
    return loadopenInterest

def isDateValid(date, pattern = "%y-/%m-/%d"):
    try:
        datetime.datetime.strptime(date, pattern)
        print("valid date")
    except ValueError:
        print("Not valid date:",date)

def getStockVolumeFromJson(symbol):
    stockvolume = 0
    global StockVolume
    print("symbol for to  getStockVolumefromJson:",symbol)
   
    with open('OptionsDataBase.json', 'r') as f:
       optionsData_dict = json.load(f)
   
    def firstkey(key,dictionary):
        for k, value in dictionary.items():
            if k == key:
                yield value

    def findkey(key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                if v != getStockOptionSymbol[0]:
                    yield v
                    
            elif isinstance(v, dict):
                for result in findkey(key, v):
                    if v != getStockOptionSymbol[0]:
                        yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findkey(key, d):
                            yield result

    getStockOptionSymbol = list(firstkey('symbol',optionsData_dict))    
    stockvolume = list(findkey('totalVolume',optionsData_dict))
    if(len(stockvolume) != 0):
        StockVolume = stockvolume[0]
        print("symbol, stockVolume is from json:",symbol,StockVolume)
        return stockvolume[0]
    else:
        StockVolume = 0
        return 0
    print("symbol, stockVolume is :",symbol,StockVolume)
     
    
    
    

def getStockPriceFromJson(symbol):
    stockprice = 0
    global StockPrice
    print("symbol for to  getStockVolumefromJson:",symbol)
   
    with open('OptionsDataBase.json', 'r') as f:
       optionsData_dict = json.load(f)
   
    def firstkey(key,dictionary):
        for k, value in dictionary.items():
            if k == key:
                yield value

    def findkey(key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                if v != getStockOptionSymbol[0]:
                    yield v
                    
            elif isinstance(v, dict):
                for result in findkey(key, v):
                    if v != getStockOptionSymbol[0]:
                        yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findkey(key, d):
                            yield result

    getStockOptionSymbol = list(firstkey('symbol',optionsData_dict))
    stockprice =  list(findkey('last',optionsData_dict))
    print("stockprice is from json  :",stockprice)
    if(len(stockprice) != 0):
        StockPrice = stockprice[0]
        print("symbol, stockPrice is from json:",symbol,StockPrice)
        return stockprice[0]
    else:
        StockPrice = 0
        return 0
    print("symbol, stockPrice is :",symbol,StockPrice)
    
   
    
def getStockPriceFromTD(symbol):
    stockprice  = 0
    global StockPrice

    print("symbol for to  getStockPrice:",symbol)
    payload = {'apikey':api_key.API_KEY,
            'symbol':symbol,
            'includeQuotes':'TRUE',
            'strategy':'SINGLE',            
            'optionType':'S'
        }
    content = requests.get(url = endpoint, params = payload)
    data = content.json()
    with open('StockPrice.json', 'w') as outfile:
        json.dump(data, outfile)
    with open('StockPrice.json', 'r') as f:
       optionsData_dict = json.load(f)
   
    def firstkey(key,dictionary):
        for k, value in dictionary.items():
            if k == key:
                yield value

    def findkey(key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                if v != getStockOptionSymbol[0]:
                    yield v
                    
            elif isinstance(v, dict):
                for result in findkey(key, v):
                    if v != getStockOptionSymbol[0]:
                        yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findkey(key, d):
                            yield result

    getStockOptionSymbol = list(firstkey('symbol',optionsData_dict))
    stockprice =  list(findkey('last',optionsData_dict))
    if(len(stockprice) != 0):
        print("symbol, stockVolume is  fron TD:",symbol,stockprice)
        StockPrice = stockprice[0]
        print("stockprice is :",stockprice)
        if os.path.exists('StockPrice.json'):
            print("file exists")
            #os.remove('StockPrice.json')
        else:
            print("The file does not exist")
        return stockprice[0]
    else:
        StockPrice = 0
        return 0
    print("symbol,stock price  is :",symbol,Stockprice)
    
def getStockVolumeFromTD(symbol):
    stockvolume = 0
    global StockVolume 
    print("symbol for to  getStockPrice:",symbol)
    payload = {'apikey':api_key.API_KEY,
            'symbol':symbol,
            'includeQuotes':'TRUE',
            'strategy':'SINGLE',            
            'optionType':'S'
        }
    content = requests.get(url = endpoint, params = payload)
    data = content.json()
    with open('StockVolume.json', 'w') as outfile:
        json.dump(data, outfile)
    with open('StockVolume.json', 'r') as f:
       optionsData_dict = json.load(f)
   
    def firstkey(key,dictionary):
        for k, value in dictionary.items():
            if k == key:
                yield value

    def findkey(key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                if v != getStockOptionSymbol[0]:
                    yield v
                    
            elif isinstance(v, dict):
                for result in findkey(key, v):
                    if v != getStockOptionSymbol[0]:
                        yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findkey(key, d):
                            yield result

    getStockOptionSymbol = list(firstkey('symbol',optionsData_dict))    
    stockvolume = list(findkey('totalVolume',optionsData_dict))
    if(len(stockvolume) != 0):
        StockVolume = stockvolume[0]
        print("symbol, stockVolume is : from TD",symbol,stockvolume)
        if os.path.exists('StockVolume.json'):
            os.remove('StockVolume.json')
        else:
            print("The file does not exist")
        return stockvolume[0]
        
    else:
        StockVolume = 0
        return 0
    
def getOpenInterestFromTD(optionSymbol,optiontype):
    
    symbol,date = optionSymbol.split('_')
    date = list(str(date))
    length = len(date)
    expdate = '20'+date[4]+date[5]+'-'+date[0]+date[1]+'-'+date[2]+date[3]
    length = length -6
    optionType = date[6]
    if(optionType == 'C'):
        optionType = 'CALL'
    else:
        optionType = 'PUT'
    length = length -1
    optionStrikePrice =[]
    length = len(date) - length
    for length in range(length,len(date)):
        optionStrikePrice.append(date[length])
    optionStrikePrice =''.join(optionStrikePrice)
    optionopenInterest = getOpenInterest(symbol,expdate,optionStrikePrice,optiontype)
    return optionopenInterest

def getDate(optionSymbol):
    symbol,date = optionSymbol.split('_')
    date = list(str(date))
    length = len(date)
    expdate = '20'+date[4]+date[5]+'/'+date[0]+date[1]+'/'+date[2]+date[3]
    #print("expdate is :",expdate)
    return expdate
    

def extractString(string, start='[', stop=']'):
        return string[string.index(start)+1:string.index(stop)]
    
def mainloop():
    global StockPrice
    global optionVolume
    global optionPrice
    global CSVOptionSymbolList
    global totalStocks
    global totalCols
    global StockVolume
    stockp = 0
    stockv = 0
    
    generateTotalStockList()
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            ofile = getStockCSVFiles(contracttype,index)
            lines = list()
            if os.path.exists(ofile):
                print("File Exists:",ofile)
                today = datetime.date.today()
                today= datetime.datetime.strftime((today), '%Y/%m/%d')
                with open(ofile, 'rU') as readFile:
                    readCSV = csv.reader(readFile)
                    fields = next(readCSV)
                    lines.append(fields)
                    for row in readCSV:
                        lines.append(row)
                        date1 = getDate(row[0])
                        if(date1< today):
                            lines.remove(row)
                with open(ofile, 'w') as writeCSV:
                        writer = csv.writer(writeCSV,lineterminator='\r')
                        writer.writerows(lines)
            else:
                print("File Does not Exists:",ofile)
        
    for index in range(totalStocks):
        Index = index
        print("stockOptionSymbol[index] in main is :",stockSymbol[index])
        
        stockoptionexpDateList = [] 
        StockPrice = 0
        StockVolume = 0
        stockp = 0
        stockv = 0
        print("stockSymbol[index] :StockPrice,StockVolume,stockp,stockv in main :",stockSymbol[index],StockPrice,StockVolume,stockp,stockv)
        if os.path.exists('OptionsDataBase.json'):
            os.remove('OptionsDataBase.json')
        else:
            print("The file 'OptionsDataBase.json' does not exist")
        for contracttype in range(len(contractType)):
            getStockOptionExpDates(stockSymbol[Index],stockOptionExpDate[Index],contracttype)
            if(len(stockOptionExpDateList) == 0):
                getStockOptionExpDates(stockSymbol[Index],stockOptionExpDate[Index],contracttype)
            getOptionsStrikePrice(stockSymbol[Index],stockOptionExpDate[Index],contracttype)
            csvStockFileName = getStockCSVFiles(contracttype,Index)
##            if(len(stockOptionExpDateList) != 0):
##                getStockPriceFromJson(stockSymbol[Index])
##            else:
##                print("get price from TD")
##                getStockPriceFromTD(stockSymbol[Index])
##                
##            if(len(stockOptionExpDateList) != 0):
##                getStockVolumeFromJson(stockSymbol[Index])
##            else:
##                getStockVolumeFromTD(stockSymbol[Index])

            ofile =  csvStockFileName
            lists =[]
            if os.path.exists(ofile):
                    print("File Exists:",ofile)                                    
            else:
                    print("File does not Exists:",ofile)
                    with open(ofile, 'w') as myfile:
                        writer = csv.writer(myfile)
                        writer.writerow(['Symbol'])
            if os.path.exists(ofile):
                print("File Exists")
                data_frame = pd.read_csv(ofile, index_col = False)
                countRows = data_frame.shape[0]
                countCols = data_frame.shape[1]
                if(countCols == 1):
                        data_frame['Symbol'] = stockOptionSymbolList
                        today = datetime.date.today()
                        today= datetime.datetime.strftime((today), '%Y%m%d')
                        data_frame[today] = today
                        data_frame.to_csv(ofile,index = False)
                CSVOptionSymbolList= data_frame.Symbol.tolist()
                today = datetime.date.today()
                today= datetime.datetime.strftime((today), '%Y%m%d')
                todayOptionSymbolList = stockOptionSymbolList
                print("CSVOptionSymbolList  and length is  :",CSVOptionSymbolList,len(CSVOptionSymbolList))
                print("todayOptionSymbolList and length is  :",todayOptionSymbolList,len(todayOptionSymbolList))
                commonOptionSymbolList = list(set(todayOptionSymbolList)& set(CSVOptionSymbolList))
                merged_list = CSVOptionSymbolList + list(set(todayOptionSymbolList) - set(CSVOptionSymbolList))

                print(" commonOptionSymbolList is  and length is :",commonOptionSymbolList,len(commonOptionSymbolList))

######          Common option symbol generated today and which is present in csv file before
        
                for index in range(len(commonOptionSymbolList)):
                    if(index == 0):
                        today = datetime.date.today()
                        today= datetime.datetime.strftime((today), '%Y%m%d')
                        data_frame[today] = today
                        data_frame.to_csv(ofile,index = False)
                        optionOpenInterest= 0
                        rows =[]
                        stockPrice =[]
                        stockVolume =[]
                        csvDateColumnlists = data_frame.columns
                        if today in csvDateColumnlists:
                            data_frame = pd.read_csv(ofile, index_col = False)
                            countRows = data_frame.shape[0]
                            countCols = data_frame.shape[1]
                            totalCols = countCols
                            CSVOptionSymbolList = data_frame['Symbol']
                            optionOpenInterest = getOpenInterestFromTD(CSVOptionSymbolList[0],contractType[contracttype])
                            
                            optionopenInterestIsEmpty = len(optionOpenInterest)
                            if(optionopenInterestIsEmpty == 0):
                                print("optionopenInterestIsEmpty == 0 so getting option openInterest from TD")
                                optionOpenInterest =getOpenInterestFromTD(CSVOptionSymbolList[0],contractType[contracttype])
                            if(StockPrice != 0):
                                stockPrice = StockPrice
                                rows.append(StockPrice)
                                stockp = StockPrice
                            else:
                                 rows.append(stockp)
                            if(StockVolume != 0):
                                rows.append(StockVolume)
                                stockv = StockVolume
                            else:
                                rows.append(stockv)
                            print("stockPrice = StockVolume :",stockPrice,StockVolume)
                            

                            optionPrice = str(optionPrice).replace('[','')
                            optionPrice = str(optionPrice).replace(']','')
                            if(optionPrice =='' or optionPrice == '.'):
                                optionPrice = 'U'    
                            rows.append(optionPrice)
                            
                            optionVolume = str(optionVolume).replace('[','')
                            optionVolume = str(optionVolume).replace(']','')
                            if(optionVolume == '' or optionVolume == '.'):
                                optionVolume = 'U'
                            rows.append(optionVolume)
                            
                            string = ':'.join(str(v) for v in rows)
                            stPstVopPopV =string
                            optionOpenInterest = extractString(str(optionOpenInterest))
                            if(optionOpenInterest == '' or optionOpenInterest == '.'):
                                optionOpenInterest = 'U'
                            optionOpenInterest = str(optionOpenInterest)+':'+str(stPstVopPopV)
                            print("todaySymbolList[0]: rows : optionOpenInterest",CSVOptionSymbolList[0],rows,optionOpenInterest)
                            data_frame.iloc[0,countCols-1]= optionOpenInterest
                            data_frame.to_csv(ofile,index = False)
                                
                    data_frame = pd.read_csv(ofile, index_col = False)
                    countRows = data_frame.shape[0]
                    countCols = data_frame.shape[1]
                
                            
                    csvDateColumnlists = data_frame.columns
                    if today in csvDateColumnlists:
                        CSVOptionSymbolList = data_frame['Symbol']
                        i = 0
                        length = len(CSVOptionSymbolList)
                        optionOpenInterest = 0 
                        rows =[]
                        stockPrice =[]
                        stockVolume =[]
                        while i < length:
                            if commonOptionSymbolList[index] == CSVOptionSymbolList[i]:
                                data_frame = pd.read_csv(csvStockFileName, index_col = False)
                                countRows = data_frame.shape[0]
                                countCols = data_frame.shape[1]
                                if(len(stockOptionExpDateList) != 0):
                                    optionOpenInterest = getOpenInterestFromJson(CSVOptionSymbolList[i])            
                                optionOpenInterest =[optionOpenInterest]
                                optionopenInterestIsEmpty = len(optionOpenInterest)
                                
                                if(optionopenInterestIsEmpty == 0):
                                    print("optionopenInterestIsEmpty == 0 from Json so getting option openInterest from TD")
                                    optionOpenInterest =getOpenInterestFromTD(CSVOptionSymbolList[i],contractType[contracttype])
                                    #optionOpenInterest =[optionOpenInterest]
                                print("symbolCSVOptionSymbolList[i] is optionOpenInterest is :",optionOpenInterest)
                                if(StockPrice != 0):
                                    stockPrice = StockPrice
                                    stockp = StockPrice
                                    rows.append(StockPrice)                                    
                                else:
                                     rows.append(stockp)
                                     
                                if(StockVolume != 0):
                                    stockv = StockVolume
                                    rows.append(StockVolume)                                    
                                else:
                                    rows.append(stockv)
                                print("stockPrice = StockVolume :",stockPrice,StockVolume)
                                
                                optionPrice = str([optionPrice])[1:-1]
                                if(optionPrice =='' or optionPrice == '.'):
                                    optionPrice = 'U'                                
                                rows.append(optionPrice)
                                
                                optionVolume = str([optionVolume])[1:-1]
                                if(optionVolume == '' or optionVolume == '.'):
                                    optionVolume = 'U'
                                rows.append(optionVolume)
                                
                                string = ':'.join(str(v) for v in rows)
                                stPstVopPopV =string
                                optionOpenInterest = extractString(str(optionOpenInterest))
                                if(optionOpenInterest == '' or optionOpenInterest == '.'):
                                    optionOpenInterest = 'U'
                                optionOpenInterest = str(optionOpenInterest)+':'+str(stPstVopPopV)
                                #print("symbol:",CSVOptionSymbolList[i])
                                print("todaySymbolList[i] : ,rows : ,optionOpenInterest",CSVOptionSymbolList[i],rows,optionOpenInterest )
                                data_frame.iloc[i,countCols-1]= optionOpenInterest
                                data_frame.to_csv(ofile,index = False)                                           
                            i += 1
                              
                            
                data_frame = pd.read_csv(ofile, index_col = False)
                CSVOptionSymbolList= data_frame.Symbol.tolist()
                todayOptionSymbolList = stockOptionSymbolList
                prevCSVOptionSymbolList = list(set(CSVOptionSymbolList) - set(todayOptionSymbolList))

######          Option Symbol which were present in csv file before but not generated today
                print("prevCSVOptionSymbolList and prevCSVOptionSymbolList len is :",prevCSVOptionSymbolList,len(prevCSVOptionSymbolList))
                for index in range(len(prevCSVOptionSymbolList)):
                    j=0
                    i=0
                    data_frame = pd.read_csv(ofile, index_col = False)
                    countCols = data_frame.shape[1]
                    lists = data_frame.columns
                    if today in lists:
                        CSVOptionSymbolList = data_frame.Symbol.tolist()
                        length = len(CSVOptionSymbolList)
                        optionOpenInterest = 0
                        rows =[]
                        stockPrice =[]
                        stockVolume =[]
                        while j < length:
                            
                            if prevCSVOptionSymbolList[index] == CSVOptionSymbolList[j]:
                                data_frame = pd.read_csv(csvStockFileName, index_col = False)
                                countRows = data_frame.shape[0]
                                countCols = data_frame.shape[1]
                                optionOpenInterest = getOpenInterestFromTD(prevCSVOptionSymbolList[index],contractType[contracttype])
                                optionopenInterestIsEmpty = len(optionOpenInterest)
                                print("optionopenInterestIsEmpty = len(optionOpenInterest) is :", optionopenInterestIsEmpty,len(optionOpenInterest))
                                                                
                                if(optionopenInterestIsEmpty == 0):
                                    optionOpenInterest =getOpenInterestFromTD(prevCSVOptionSymbolList[index],contractType[contracttype])
                                if(StockPrice != 0):
                                    stockPrice = StockPrice
                                    rows.append(StockPrice)
                                    stockp = StockPrice
                                else:
                                     rows.append(stockp)
                                if(StockVolume != 0):
                                    rows.append(StockVolume)
                                    stockv = StockVolume
                                else:
                                    rows.append(stockv)
                                print("stockPrice = StockVolume :",stockPrice,StockVolume)
                                #optionPrice = str(optionPrice)[1:-1]
                                optionPrice = str(optionPrice).replace('[','')
                                optionPrice = str(optionPrice).replace(']','')
                                if(optionPrice =='' or optionPrice == '.'):
                                    optionPrice = 'U'        
                                rows.append(optionPrice)
                                
                                #optionVolume = str(optionVolume)[1:-1]
                                optionVolume = str(optionVolume).replace('[','')
                                optionVolume = str(optionVolume).replace(']','')
                                if(optionVolume == '' or optionVolume == '.'):
                                    optionVolume = 'U'
                                rows.append(optionVolume)
                                
                                string = ':'.join(str(v) for v in rows)
                                stPstVopPopV =string
                                optionOpenInterest = extractString(str(optionOpenInterest))
                                if(optionOpenInterest == '' or optionOpenInterest == '.'):
                                    optionOpenInterest = 'U'
                                optionOpenInterest = str(optionOpenInterest)+':'+str(stPstVopPopV)
                                #print("symbol:",CSVOptionSymbolList[j])
                                data_frame.iloc[j,countCols-1]= optionOpenInterest
                                data_frame.to_csv(ofile,index = False)
                                #print("openinterest ...............main..................:",optionOpenInterest)
                                print("CSVOptionSymbolList[j]:optionOpenInterest",CSVOptionSymbolList[j],rows,optionOpenInterest )
                            j += 1
                    else:
                        today = datetime.date.today()
                        today= datetime.datetime.strftime((today), '%Y%m%d')
                        data_frame[today] = today
                        data_frame.to_csv(ofile,index = False)
                        CSVOptionSymbolList= data_frame.Symbol.tolist()
                        length = len(prevCSVOptionSymbolList)
                        optionOpenInterest = 0
                        stockPrice =[]
                        stockVolume =[]
                        while i < length:
                            
                            if prevCSVOptionSymbolList[index] == CSVOptionSymbolList[i]:
                                data_frame = pd.read_csv(ofile, index_col = False)
                                countRows = data_frame.shape[0]
                                countCols = data_frame.shape[1]
                                optionOpenInterest = getOpenInterestFromTD(prevCSVOptionSymbolList[index],contractType[contracttype])                                
                                optionopenInterestIsEmpty = len(optionOpenInterest)
                                if(optionopenInterestIsEmpty == 0):
                                    print("optionopenInterestIsEmpty == 0 so getting option openInterest from TD")
                                    optionOpenInterest =getOpenInterestFromTD(prevCSVOptionSymbolList[index],contractType[contracttype])
                                if(StockPrice != 0):
                                    stockPrice = StockPrice
                                    rows.append(StockPrice)
                                    stockp = StockPrice
                                else:
                                    rows.append(stockp)
                                if(StockVolume != 0):
                                    rows.append(StockVolume)
                                    stockv = StockVolume
                                else:
                                    rows.append(stockv)
                                print("stockPrice = StockVolume :",StockPrice,StockVolume)
                                optionPrice = str(optionPrice).replace('[','')
                                optionPrice = str(optionPrice).replace(']','') 
                                if(optionPrice =='' or optionPrice == '.'):
                                    optionPrice = 'U'        
                                rows.append(optionPrice)
                                
                                optionVolume = str(optionVolume).replace('[','')
                                optionVolume = str(optionVolume).replace(']','')
                                if(optionVolume == '' or optionVolume == '.'):
                                    optionVolume = 'U'
                                rows.append(optionVolume)
                                
                                string=':'.join(str(v) for v in rows)
                                stPstVopPopV =string
                                optionOpenInterest = extractString(str(optionOpenInterest))
                                if(optionOpenInterest == '' or optionOpenInterest == '.'):
                                    optionOpenInterest = 'U'
                                optionOpenInterest = str(optionOpenInterest)+':'+str(stPstVopPopV)
                                print("symbol:",CSVOptionSymbolList[i])
                                data_frame.iloc[i,countCols-1]= optionOpenInterest
                                data_frame.to_csv(ofile,index = False)
                                print("CSVOptionSymbolList[i] : ,optionOpenInterest : ",CSVOptionSymbolList[i],rows,optionOpenInterest )
                            i += 1

######          New symbol generated today which is not present in csv file
                                      
                data_frame = pd.read_csv(ofile, index_col = False)
                CSVOptionSymbolList= data_frame.Symbol.tolist()
                todayOptionSymbolList = stockOptionSymbolList
                print("todayOptionSymbolList and length is :",todayOptionSymbolList,len(todayOptionSymbolList))
                print("len of CSVOptionSymbolList is :",len(CSVOptionSymbolList))
                newOptionSymbolList = list(set(todayOptionSymbolList) - set(CSVOptionSymbolList))
                #newOptionSymbolList.sort()
            
                print("new_symbol_list are :",newOptionSymbolList)
                
                for index in range(len(newOptionSymbolList)):
                    m1=[]
                    data =[]
                    rows =[]
                    optionOpenInterest =0
                    optionSymbol =0
                    for i in range(countCols):
                        if(i == 0):
                            optionSymbol = newOptionSymbolList[index]
                            optionSymbol=[str(optionSymbol)]

                        elif( i == countCols-1):
                            optionOpenInterest = getOpenInterestFromJson(newOptionSymbolList[index])
                            optionopenInterest = optionOpenInterest
                            optionopenInterest =[optionopenInterest] 
                            optionopenInterestIsEmpty = len(optionopenInterest)
                            if(optionopenInterestIsEmpty == 0):
                                print("optionopenInterestIsEmpty == 0 from Json so getting option openInterest from TD")
                                optionOpenInterest =getOpenInterestFromTD(newOptionSymbolList[index],contractType[contracttype])
                            if(StockPrice != 0):
                                stockPrice = StockPrice
                                rows.append(StockPrice)
                            else:
                                rows.append(stockp)
                            if(StockVolume != 0):
                                rows.append(StockVolume)
                            else:
                                rows.append(stockv)
                            
                            optionPrice = str(optionPrice)
                            if(optionPrice =='' or optionPrice == '.'):
                                    optionPrice = 'U'
                            rows.append(optionPrice)
                            
                            optionVolume = str(optionVolume)
                            if(optionVolume == '' or optionVolume == '.'):
                                    optionVolume = 'U'
                            rows.append(optionVolume)
                            
                            string = ':'.join(str(v) for v in rows)
                            stPstVopPopV =string
                            if(optionOpenInterest == '' or optionOpenInterest == '.'):
                                optionOpenInterest = 'U'
                            
                            optionOpenInterest = str(optionOpenInterest)+':'+str(stPstVopPopV)
                            
                            optOpenInterest = optionOpenInterest
                            print("symbol is :",newOptionSymbolList[index])
                            print("newOptionSymbolList[index]: ,optionOpenInterest :",newOptionSymbolList[index],rows,optionOpenInterest )
                        else:
                            m2='U'
                            m1.append(m2)
                    data = [optionSymbol+m1]

                    
                    with open(ofile, 'a') as csvfile:
                        wr = csv.writer(csvfile,lineterminator='\r')
                        for row in data:
                            wr.writerow(row)
                    data_frame = pd.read_csv(csvStockFileName, index_col = False)
                    countRows = data_frame.shape[0]
                    countCols = data_frame.shape[1]
                    data_frame.iloc[countRows-1,countCols-1]= optOpenInterest
                    data_frame.to_csv(ofile,index = False) 
                    

mainloop() 
                    
print('done')
