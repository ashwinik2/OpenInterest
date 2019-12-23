import os
import os.path
from os import path
import sys
import requests
import api_key
import json
from collections import OrderedDict
from pandas.io.json import json_normalize
import csv
import pandas as pd
from pandas import DataFrame
from datetime import datetime, timedelta
from datetime import date
import enum
##from datetime import date
##from datetime import datetime
##from datetime import timedelta
##import datetime


endpoint = r"https://api.tdameritrade.com/v1/marketdata/chains"
csv.field_size_limit(sys.maxsize)

contractType =['CALL','PUT']
ofilepath = './output/'
ifilepath = './input/'
ifilestocklist = ifilepath+'StockList.csv'

class Contracttype(enum.Enum):
    CALL = 0
    PUT = 1
    
def generateTotalStockList(ifilestocklist):
    totalStocks = 0
    stockSymbol = []
    stockExpDate = []
    
    with open(ifilestocklist) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        fields = next(readCSV)
        for row in readCSV:
            stocksymbol = row[0]
            stockexpdate = row[1]
            print("stocksymbol,stockexpdate :",stocksymbol,stockexpdate)
            stockSymbol.append(stocksymbol)
            stockExpDate.append(stockexpdate)            
        print(stockSymbol)
        print(stockExpDate)
        totalStocks = len(stockSymbol)
        print("totalStocks  is :",totalStocks)
    return totalStocks,stockSymbol,stockExpDate

def getStockCSVFile(index,stockSymbol,contractType):       
    stockCsvfilename = ofilepath + stockSymbol+'_'+contractType[index]+'.csv'
    return stockCsvfilename

def getStockOptionExpDates(symbol,expDate,index,strikeCount):
    stockOptionExpDateList = []
    Success = 'True'
    print("symbol,expDate,index,strikeCount is :",symbol,expDate,index,strikeCount)
    payload = {'apikey':api_key.API_KEY,
           'symbol':symbol,
           'contractType':contractType[index],
            'strikeCount':strikeCount,
           'includeQuotes':'TRUE',
           'strategy':'SINGLE',   
           'toDate':expDate,
           'optionType':'S'
           }
    retry_count = 0
    #loop here until the request succeed
    while(1):
        #content = requests.get(url = endpoint, params = payload)
        try:
            content = requests.get(url = endpoint, params = payload, timeout=60)
        except Timeout:
            print('####################################################################')
            print('The request timed out')
            print('Retrying...')
            print('####################################################################')
        else:
            print('The request did not time out')
            break;

        retry_count = retry_count + 1
        print('retry_count: ' + str(retry_count))

        if(retry_count > 10):
            print('The retry_count exceeded' + str(retry_count))
            break;
        
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
                        t = datetime.fromtimestamp(float(result)/1000.)
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
        Success = 'True'
        return Success,stockoptionexpDateList
    else:
        print("length of optionExpiration Dates  in else is :",len(stockoptionexpDateList))
        del stockOptionExpDateList[:]
        print("length of optionExpiration Dates  stockOptionExpDateList ='' in else is :",len(stockOptionExpDateList))
        Success = 'False'
        return Success,len(stockOptionExpDateList)

def getOptionsStrikePrice(symbol,expDate,index):
    stockStrikepricesList =  stockOptionSymbolList = []
       
    with open('OptionsDataBase.json', 'r') as f:
       optionsData_dict = json.load(f)
   
    def firstkey(key,dictionary):
        for k, value in optionsData_dict.items():
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
    return stockOptionSymbolList,stockStrikepricesList

def getOpenInterest(symbol,expDate,strikePrice,optionType):
    optionVolume = []
    optionPrice = []
    StockVolume,StockPrice = 0,0
           
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

    retry_count = 0
    #loop here until the request succeed
    while(1):
        #content = requests.get(url = endpoint, params = payload)
        try:
            content = requests.get(url = endpoint, params = payload, timeout=60)
        except Timeout:
            print('####################################################################')
            print('The request timed out')
            print('Retrying...')
            print('####################################################################')
        else:
            print('The request did not time out')
            break;

        retry_count = retry_count + 1
        print('retry_count: ' + str(retry_count))

        if(retry_count > 10):
            print('The retry_count exceeded' + str(retry_count))
            break;

    data = content.json()
    
    with open('OpenInterest.json', 'w') as outfile:
        json.dump(data, outfile)
    with open('OpenInterest.json', 'r') as f:
       optionsData_dict = json.load(f)
       
    def findSymbolKey(key,dictionary):
        for k, value in data.items():
            if k == key:
                yield value
    def findParameterKey(key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                if v != getStockOptionSymbol[0]:
                    yield v
                    
            elif isinstance(v, dict):
                for result in findParameterKey(key, v):
                    if v != getStockOptionSymbol[0]:
                        yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findParameterKey(key, d):
                            yield result    

    getStockOptionSymbol = list(findSymbolKey('symbol',optionsData_dict))
    openInterest = list(findParameterKey('openInterest',optionsData_dict))    
    optionvolume = list(findParameterKey('totalVolume',optionsData_dict))
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
    
    if(optionType == Contracttype.CALL.name):
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
            
    optionprice = list(findParameterKey('last',optionsData_dict))       
    if(optionType == Contracttype.CALL.name):
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
    print("symbol,loadopenInterest,StockPrice,StockVolume,optionvolume,optionprice in  getOpenInterest from TD:",symbol,openInterest,StockPrice,StockVolume,optionVolume,optionPrice)
    return openInterest,StockPrice,StockVolume,optionPrice,optionVolume

def getOpenInterestFromJson(symbol):
    global openInterest
    global optionVolume 
    global optionPrice 
        
    with open('OptionsDataBase.json', 'r') as f:
       optionsData_dict = json.load(f)
       
    def firstkey(key,dictionary):
        for k, value in optionsData_dict.items():
            if k == key:
                yield value

    def findOpenInterestKey(key, dictionary):
        global openInterest
        optionSymbolExist =0
        value = symbol
        for k, v in dictionary.items():
            if k == 'symbol':
                if(v == value):
                    optionSymbolExist += 1
        if(optionSymbolExist == 1):
            for k, v in dictionary.items():
                if k == key:
                    openInterest = v
                    yield v
   #     return v

    def findOptionVolume(key, dictionary):      
        optionSymbolExist =0
        value = symbol
        global optionVolume
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
        optionSymbolExist =0
        value = symbol
        global optionPrice
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
        global openInterest 
        global optionVolume 
        global optionPrice 
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
                            openInterest = result
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
    #print("symbol :, openInterest : optionVolume :,optionPrice : from json ",symbol,openInterest,optionPrice,optionVolume)
    return openInterest,optionPrice,optionVolume


def getStockPriceStockVolFromJson(symbol,contracttype):
    stockprice = stockVolume = []    

    with open('OptionsDataBase.json', 'r') as f:
       optionsData_dict = json.load(f)
   
    def stockSymbolKey(key,dictionary):
        for k, value in dictionary.items():
            if k == key:
                yield value

    def findKey(key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                if v != getStockOptionSymbol[0]:
                    yield v
                    
            elif isinstance(v, dict):
                for result in findKey(key, v):
                    if v != getStockOptionSymbol[0]:
                        yield result
            elif isinstance(v, list):
                if v != getStockOptionSymbol[0]:
                    for d in v:
                        for result in findKey(key, d):
                            yield result

    getStockOptionSymbol = list(stockSymbolKey('symbol',optionsData_dict))
    stockprice =  list(findKey('last',optionsData_dict))
    stockvolume = list(findKey('totalVolume',optionsData_dict))
    print("Contracttype.CALL.value is getStockPriceStockVolFromJson :",Contracttype.CALL.value,Contracttype.CALL.name)
    if(contracttype == Contracttype.CALL.name):
        if(len(stockprice) != 0 and len(stockvolume) != 0):
            splength = len(stockprice)
            svlength = len(stockvolume)
            print("stockprice is :",stockprice)
            StockPrice = stockprice[splength-1]
            stockVolume = stockvolume[svlength-1]
        else:
            StockPrice = 0
            stockVolume = 0
    else:
        if(len(stockprice) != 0 and len(stockvolume) != 0):
            splength = len(stockprice)
            svlength = len(stockvolume)
            print("stockprice is :",stockprice)
            StockPrice = stockprice[0]
            stockVolume = stockvolume[0]
            
        else:
            StockPrice = 0
            stockVolume = 0
    
    print("symbol, stockPrice is :",symbol,StockPrice)
    return StockPrice,stockVolume

  
def getOpenInterestFromTD(optionSymbol,optiontype):
    openInterest = 0
    StockPrice= 0
    StockVolume = 0
    optionPrice=0
    optionVolume=0

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
    openInterest,StockPrice,StockVolume,optionPrice,optionVolume = getOpenInterest(symbol,expdate,optionStrikePrice,optiontype)
    return openInterest,StockPrice,StockVolume,optionPrice,optionVolume 

def getDate(optionSymbol):
    symbol,date = optionSymbol.split('_')
    date = list(str(date))
    length = len(date)
    expdate = '20'+date[4]+date[5]+'/'+date[0]+date[1]+'/'+date[2]+date[3]
    #print("expdate is :",expdate)
    return expdate
    

def extractString(string, start='[', stop=']'):
        return string[string.index(start)+1:string.index(stop)]


def formatRowData(StockPrice,StockVolume,openInterest,optionPrice,optionVolume):
    rowData = []
    if(StockPrice != 0):                                    
        rowData.append(StockPrice)                                    
                        
    if(StockVolume != 0):
        rowData.append(StockVolume)                                                        
    optionPrice = str(optionPrice).replace('[','')
    optionPrice = str(optionPrice).replace(']','')
    if(optionPrice =='' or optionPrice == '.' or optionPrice == 'U'):
        optionPrice = 'U'                                
    rowData.append(optionPrice)
    
    optionVolume = str(optionVolume).replace('[','')
    optionVolume = str(optionVolume).replace(']','')
    if(optionVolume == '' or optionVolume == '.' or optionVolume == 'U'):
        optionVolume = 'U'
    rowData.append(optionVolume)
    
    string = ':'.join(str(v) for v in rowData)
    stPstVopPopV =string
    
    openInterest = str(openInterest).replace('[','')
    openInterest = str(openInterest).replace(']','')
    if(openInterest == '' or openInterest == '.'):
        openInterest = 'U'
        
    openInterest = str(openInterest)+':'+str(stPstVopPopV)

    return rowData,openInterest
    
def processCommonSymbolList(data_frame,stockSymbol,commonOptionSymbolList,ofile,contracttype):
    print("processCommonSymbolList is :",contracttype)
    today = date.today()                                    
    today = datetime.strftime((today), '%Y%m%d')  

    data_frame = pd.read_csv(ofile, index_col = False)   
    countCols = data_frame.shape[1]
    CSVOptionSymbolList = []
    StockPrice,stockVolume = 0,0
    StockPrice,StockVolume = getStockPriceStockVolFromJson(stockSymbol,contracttype)
    csvDateHeaderlist = data_frame.columns
    if not today in csvDateHeaderlist:
        data_frame[today] = today
        data_frame.to_csv(ofile,index = False)
        
    data_frame = pd.read_csv(ofile, index_col = False)
    csvDateHeaderlist = data_frame.columns 
    if today in csvDateHeaderlist:
        CSVOptionSymbolList = data_frame['Symbol']
        CSVOptionSymbolList = data_frame.Symbol.tolist()    
        for index in range(len(commonOptionSymbolList)):                                                    
                i = 0
                length = len(CSVOptionSymbolList)
                openInterest = 0
                optionPrice = 0
                optionVolume = 0 
                rowData =[]
                while i < length:
                    if commonOptionSymbolList[index] == CSVOptionSymbolList[i]:                                
                        openInterest,optionPrice,optionVolume = getOpenInterestFromJson(CSVOptionSymbolList[i])                                
                        rowData,openInterest = formatRowData(StockPrice,StockVolume,openInterest,optionPrice,optionVolume)
                        data_frame = pd.read_csv(ofile, index_col = False)
                        countCols = data_frame.shape[1]
                        data_frame.iloc[i,countCols-1]= openInterest
                        data_frame.to_csv(ofile,index = False)                                           
                    i += 1
        print("StockPrice,StockVolume is :",StockPrice,StockVolume)
        return StockPrice,StockVolume

def processprevCSVOptionSymbolList(data_frame,stockSymbol,prevCSVOptionSymbolList,ofile,contracttype):
    print("processprevCSVOptionSymbolList :contracttype :",contracttype)
#    today = datetime.date.today()
#    today= datetime.datetime.strftime((today), '%Y%m%d')
    today = date.today()                                       
    today = datetime.strftime((today), '%Y%m%d')   
#    print("dateListHeader is :",dates)
    
    data_frame = pd.read_csv(ofile, index_col = False)
    csvDateHeaderlist = data_frame.columns
    if not today in csvDateHeaderlist:
        data_frame[today] = today
        data_frame.to_csv(ofile,index = False)
        
    data_frame = pd.read_csv(ofile, index_col = False)
    csvDateHeaderlist = data_frame.columns
    if today in csvDateHeaderlist:
        CSVOptionSymbolList = data_frame['Symbol']    
        CSVOptionSymbolList = data_frame.Symbol.tolist()
        
        for index in range(len(prevCSVOptionSymbolList)):
            j=0               
            #in what case the new column is added and n what case it is not added
            if today in csvDateHeaderlist:            
                length = len(CSVOptionSymbolList)
                openInterest = 0
                StockPrice =0
                StockVolume=0
                rowData = []
                            
                while j < length:                    
                    if (prevCSVOptionSymbolList[index] == CSVOptionSymbolList[j]):
                        openInterest,StockPrice,StockVolume,optionPrice,optionVolume = getOpenInterestFromTD(prevCSVOptionSymbolList[index],contracttype)
                        rowData,openInterest = formatRowData(StockPrice,StockVolume,openInterest,optionPrice,optionVolume)
                        
                        data_frame = pd.read_csv(ofile, index_col = False)
                        countCols = data_frame.shape[1]
                        data_frame.iloc[j,countCols-1]= openInterest
                        data_frame.to_csv(ofile,index = False)
                    j += 1
        print("processprevCSVOptionSymbolList is :",StockPrice,StockVolume)
        return StockPrice,StockVolume

def processNewOptionSymbolList(data_frame,stockSymbol,newOptionSymbolList,ofile,contracttype,StockPrice,StockVolume):
    print("processNewOptionSymbolList StockPrice,stockVolume is :",StockPrice,StockVolume)
    for index in range(len(newOptionSymbolList)):
        unavaialbleColData=[]
        colsdata =[]
        rowData =[]        
        openInterest =[]
        optionSymbol = []
        data_frame = pd.read_csv(ofile, index_col = False)
        countRows = data_frame.shape[0]
        countCols = data_frame.shape[1]
        for col in range(countCols):
            if(col == 0):
                optionSymbol = newOptionSymbolList[index]
                optionSymbol=[str(optionSymbol)]

            elif(col == countCols-1):
                openInterest,optionPrice,optionVolume = getOpenInterestFromJson(newOptionSymbolList[index])                
                rowData,openInterest = formatRowData(StockPrice,StockVolume,openInterest,optionPrice,optionVolume)
            else:
                colData='U'
                unavaialbleColData.append(colData)
                       
        colsdata = [optionSymbol+unavaialbleColData]
        
        with open(ofile, 'a') as csvfile:
            wr = csv.writer(csvfile,lineterminator='\r')
            for row in colsdata:
                wr.writerow(row)
        data_frame = pd.read_csv(ofile, index_col = False)
        countRows = data_frame.shape[0]
        countCols = data_frame.shape[1]
        data_frame.iloc[countRows-1,countCols-1]= openInterest
        data_frame.to_csv(ofile,index = False)

def removeExpiredSymbolsFromStockOutputCSVFile(totalStocks,stockSymbol,stockExpDate):
    print("removeExpiredSymbolsFromStockOutputCSVFile")
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            ofile = getStockCSVFile(contracttype,stockSymbol[index],contractType)
            lines = list()
            if os.path.exists(ofile):
                print("File Exists44:",ofile)
                today = date.today()
                today= datetime.strftime((today), '%Y/%m/%d')
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
                print("File Does not Exists45:",ofile)

def removeExistingJsonFiles():
    if os.path.exists('OptionsDataBase.json'):
        os.remove('OptionsDataBase.json')
    else:
        print("The file 'OptionsDataBase.json' does not exist")

    if os.path.exists('OpenInterest.json'):
        os.remove('OpenInterest.json')
    else:
        print("The file 'OpenInterest.json' does not exist")

    if os.path.exists('OptionStrike.json'):
        os.remove('OptionStrike.json')
    else:
        print("The file 'OptionStrike.json' does not exist")


        
def openIntDataCollMain(strikeCount):
    
    CSVOptionSymbolList= []
    stockExpDate = []
    stockSymbol =[]
    totalStocks = 0
        
    totalStocks,stockSymbol,stockExpDate = generateTotalStockList(ifilestocklist)
    #Remove expirated dates from input csv file
    removeExpiredSymbolsFromStockOutputCSVFile(totalStocks,stockSymbol,stockExpDate)
    
#loop through total stocks
#    start_time = datetime.now()
    for stock in range(totalStocks):
        Index = stock
        StockPrice,StockVolume = 0,0
        stockoptionexpDateList = []
        stockOptionSymbolList = []
        stockStrikepricesList = []        
        removeExistingJsonFiles()        
                               
        for contracttype in range(len(contractType)):                       
            Success,stockOptionExpDateList = getStockOptionExpDates(stockSymbol[Index],stockExpDate[Index],contracttype,strikeCount)
            
            if((Success == 'False') and (stockOptionExpDateList) == 0):
                Success,stockOptionExpDateList = getStockOptionExpDates(stockSymbol[Index],stockExpDate[Index],contracttype,strikeCount)

            if((Success == 'True') and (len(stockOptionExpDateList) != 0)):
                print("Success is :",Success)
                stockOptionSymbolList,stockStrikepricesList = getOptionsStrikePrice(stockSymbol[Index],stockExpDate[Index],contracttype)
                
                ofile = getStockCSVFile(contracttype,stockSymbol[stock],contractType)

                data_frame = 0
                if os.path.exists(ofile):
                    print("File Exists:",ofile)                                    
                else:
                    print("File does not Exists:",ofile)
                    with open(ofile, 'w') as myfile:
                        writer = csv.writer(myfile)
                        writer.writerow(['Symbol'])
                    data_frame = pd.read_csv(ofile, index_col = False)
                    countRows = data_frame.shape[0]
                    countCols = data_frame.shape[1]
                    if(countCols == 1):
                            data_frame['Symbol'] = stockOptionSymbolList
                            today = date.today()
                   #         prev_days= today - timedelta(days=3)                                       
                            today = datetime.strftime((today), '%Y%m%d')
                            data_frame[today] = today
                            data_frame.to_csv(ofile,index = False)
                            
                if os.path.exists(ofile):
                    data_frame = pd.read_csv(ofile, index_col = False)                    
                    CSVOptionSymbolList= data_frame.Symbol.tolist()
                    todayOptionSymbolList = stockOptionSymbolList
                    commonOptionSymbolList = []
                    prevCSVOptionSymbolList=[]
                    newOptionSymbolList =[]
                    commonOptionSymbolList = list(set(todayOptionSymbolList)& set(CSVOptionSymbolList))
                    prevCSVOptionSymbolList = list(set(CSVOptionSymbolList) - set(todayOptionSymbolList))
                    newOptionSymbolList = list(set(todayOptionSymbolList) - set(CSVOptionSymbolList))

                    print(" commonOptionSymbolList is  and length is :",commonOptionSymbolList,len(commonOptionSymbolList))
                    print("prevCSVOptionSymbolList  and length.......................... is  :",prevCSVOptionSymbolList,len(prevCSVOptionSymbolList))
                    print("newOptionSymbolList and length is  :",newOptionSymbolList,len(newOptionSymbolList))

    ######  Common option symbol generated today and which is present in csv file before

                    if(len(commonOptionSymbolList) != 0):
                        StockPrice,StockVolume=processCommonSymbolList(data_frame,stockSymbol[stock],commonOptionSymbolList,ofile,contractType[contracttype])

    ######  Option Symbol which were present in csv file before but not generated today

                    if(len(prevCSVOptionSymbolList) != 0):
                        StockPrice,StockVolume = processprevCSVOptionSymbolList(data_frame,stockSymbol[stock],prevCSVOptionSymbolList,ofile,contractType[contracttype])
                           
    ######          New symbol generated today which is not present in csv file
                    if(len(newOptionSymbolList) != 0):
                        processNewOptionSymbolList(data_frame,stockSymbol[stock],newOptionSymbolList,ofile,contracttype,StockPrice,StockVolume)

    #After all stocks processes remove existing json files                                    
    removeExistingJsonFiles()
    #end_time = datetime.now()
    #totaltime = (end_time - start_time)
    #print("total time taken to execute total stocks is in hours:minutes:seconds",totalStocks,totaltime.hours,totaltime.minutes,totaltime.seconds)
    #print("total time taken to execute total stocks is in hours:minutes:seconds",totalStocks,totaltime)
    
if __name__ == "__main__":
    strikeCount = 70
    openIntDataCollMain(strikeCount) 
                    
print('done')
