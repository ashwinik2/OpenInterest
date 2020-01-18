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
from datetime import timedelta
import enum
import sys
import Commonapi
import globalheader
from collections import defaultdict
from collections import OrderedDict

csv.field_size_limit(sys.maxsize)
contractType =['CALL','PUT']
csvDataFilePath = './../datacolls/output/'

# getStockCSVFile(index,symbol,ifilepath) check whether stock csv file present in dase base if present send stock csv file name   
    #input
        #symbol - name of the stock
        #index - call(0) or put(1) 
        #ifilepath - path location of data base stock csv file
    #output
        #stockCsvfilename - './../datacolls/output/AAPL_CALL's
        #call_error  - Success or Standard defined error
def getStockCSVFile(index,symbol,ifilepath):
    stockCsvfilename = ifilepath + symbol+'_'+contractType[index]+'.csv'
    if os.path.exists(stockCsvfilename):
        call_error = globalheader.Success
        return call_error,stockCsvfilename
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        return call_error,stockCsvfilename

# generateTotalStockList(ifilestocklist) generate stock list and exp date list from stocklist  
    #input
        #ifilestocklist - stockList.csv
    #output
        # totalStocks - num of stocks
        #stockSymbol  - stock symbol list
        #stockExpDate - stock exp list
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
            stockSymbol.append(stocksymbol)
            #print("stockexpdate is before validating:",stockexpdate)        
            stockExpDate.append(stockexpdate)
            
        print(stockSymbol)
        print(stockExpDate)
        totalStocks = len(stockSymbol)        
    return totalStocks,stockSymbol,stockExpDate

# generateTotalStockList(ifilestocklist) generate stock list and exp date list from stocklist  
    #input
        #ifilestocklist - stockList.csv
    #output
        # totalStocks - num of stocks
        #stockSymbol  - stock symbol list
        #stockExpDate - stock exp list
#return data frame data like total cols, headerlist,symbol list ,date from an stock csv file
def getdataframedata(Symbol,exp_date,strikeprice,date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getdataframedata Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)

    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile)
        countCols = data_frame.shape[1]
        columnList= data_frame.columns.tolist()     
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikeprice)
            if(call_error == globalheader.Success):
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.getdataframedata Ended')
                return call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.getdataframedata Ended')
                globalheader.logging.error('%s %d', 'Commonapi.getSymbol Error', call_error)

                return call_error,0,0,0,0,0
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getdataframedata Ended')
            globalheader.logging.error('%s %d', 'dataapi.getdataframedata date Error', date_error)
            return date_error,0,0,0,0,0
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getdataframedata Ended')
        globalheader.logging.error('%s %d', 'dataapi.getStockCSVFile Error', file_error)

        return file_error,0,0,0,0,0

# getdataframeData(Symbol,exp_date,strikeprice,contracttype) generate stock csv file data like option symbol strike list,column header list, number of columns and option symbol   
    #input
        #Symbol - stock symbol
        # exp_date - option exp date
        #strikeprice - option strikeprice
        #contractype - call(0) or put(1)
    #output
        # call_error - success or standard erro
        #symbol  - option symbol
        #CSVOptionSymbolList - stock option symbol list
        #csvDateHeaderlist - date header column list
        #countCols - num of columns in the stock csv file
def getdataframeData(Symbol,exp_date,strikeprice,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getdataframeData Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)

    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile)
        countCols = data_frame.shape[1]
        columnList= data_frame.columns.tolist()     
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikeprice)
        if(call_error == globalheader.Success):
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getdataframeData Ended')
            return call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols
        else:
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getdataframeData Ended')
            globalheader.logging.error('%s %d', 'Commonapi.getSymbol Error', call_error)

            return call_error,0,0,0,0
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getdataframeData Ended')
        globalheader.logging.error('%s %d', 'dataapi.getStockCSVFile Error', file_error)

        return file_error,0,0,0,0

# getOIdata(Symbol,exp_date,date,contracttype,strikepricelist) return return option interest of the stock of the particular exp date of the particular trading day of an option type(call or put)   
    #input
        #Symbol - stock symbol
        # exp_date - option exp date
        #date - trading date
        #contractype - call(0) or put(1)
        #strikepricelist - option strike price list
    #output
        # call_error - success or standard error
        #OI_dict  - 2d open interest dictionary
        
def getOIdata(Symbol,exp_date,date,contracttype,strikepricelist):
    OI_dict =  OrderedDict()
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getOIdata Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            openinterest_list = []
            optionsymbol_list = []
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                if(call_error ==  globalheader.Success):
                    length = len(CSVOptionSymbolList)
                    while j < length:
                        if(symbol == CSVOptionSymbolList[j]):
                            optionsymbolstrikeprice_list.append(strikepricelist[i])
                            openinterest = data_frame.iloc[i,countcols]                    
                            openInterest = str(openinterest).split(Commonapi.data_seperator)
                            if Commonapi.listOfStr[0] in openInterest:
                                openInterest = Commonapi.ConvertLst_Dict(openInterest)
                                OI = openInterest['OI']
                                OI = str(OI)
                                OI = OI.split(',')
                                openInterest['OI'] = OI[0]
                                if(openInterest['OI'] == 'U' or openInterest['OI'] == '.' or openInterest['OI'] == ',' or openInterest['OI'] == "'" or openInterest['OI'] == ''):
                                    openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
                                    if(globalheader.info == 1):
                                        globalheader.logging.info('dataapi.getOIdata Endeded')
                                    globalheader.logging.error('%s %d', 'dataapi.getOIdata Error', openInterest_error)

                                    return openInterest_error,0
                                else:
                                    openinterest_list.append(openInterest['OI'])
                            else:
                                call_error, OI =Commonapi.getopenInterest(openInterest)
                                openinterest_list.append(OI)
                        j += 1
                else:
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.getOIdata Endeded')
                    globalheader.logging.error('%s %d', 'Commonapi.getSymbol Error', file_error)
                    return openInterest_error,0
                    
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getOIdata Ended')
            zipbObj = zip(optionsymbolstrikeprice_list,openinterest_list)
            dictofOI = OrderedDict(zipbObj)
            optionsymbol = str(Symbol)+'_'+str(exp_date)
            OI_dict[optionsymbol]= dictofOI
            return call_error,OI_dict
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getOIdata Endeded')
            globalheader.logging.error('%s %d', 'dataapi.getOIdata date Error', date_error)

            return date_error,OI_dict
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getOIdata Endeded')
        globalheader.logging.error('%s %d', 'dataapi.getOIdata file Error', file_error)

        return file_error,OI_dict


# getOPdata(Symbol,exp_date,date,contracttype,strikepricelist) return option price of the stock of the particular exp date of the particular trading day of an option type(call or put)   
    #input
        #Symbol - stock symbol
        # exp_date - option exp date
        #date - trading date
        #contractype - call(0) or put(1)
        #strikepricelist - option strike price list
    #output
        # call_error - success or standard erro
        #OP_dict  - 2d option price dictionary   
def getOPdata(Symbol,exp_date,date,contracttype,strikepricelist):
    OP_dict = OrderedDict()
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getOPdata Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            optionPrice_list = []
            optionsymbolstrikeprice_list =[]
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                if(call_error ==  globalheader.Success):
                    length = len(CSVOptionSymbolList)
                    while i < length:
                        if(symbol == CSVOptionSymbolList[i]):
                            optionsymbolstrikeprice_list.append(strikepricelist[i])
                            optionPrice = getrowdata(i,countcols,Symbol,contracttype)
                            optionPrice = str(optionPrice).split(Commonapi.data_seperator)
                            if Commonapi.listOfStr[3] in optionPrice:
                                optionPrice = Commonapi.ConvertLst_Dict(optionPrice)
                                OP = optionPrice['OP']
                                OP = str(OP)
                                OP = OP.split(',')
                                optionPrice['OP'] = OP[0]
                                if(optionPrice['OP'] == 'U' or optionPrice['OP'] == '.' or optionPrice['OP'] == ',' or optionPrice['OP'] == "'" or optionPrice['OP'] == ''):
                                    optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
                                    if(globalheader.info == 1):
                                        globalheader.logging.info('dataapi.getOPdata Ended')
                                    globalheader.logging.error('%s %d', 'dataapi.getOPdata Error', file_error)

                                    return optionPrice_error,0
                                else:
                                    optionPrice_list.append(optionPrice['OP'])
                            else:
                                call_error, OP =Commonapi.getoptionPrice(optionPrice)
                                optionPrice_list.append(OP)
                        i += 1
                else:
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.getOPdata Endeded')
                    globalheader.logging.error('%s %d', 'Commonapi.getSymbol Error', file_error)
                    return optionPrice_error,0
                    
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getOPdata Ended')
            zipbObj = zip(optionsymbolstrikeprice_list,optionPrice_list)
            dictofOP = OrderedDict(zipbObj)
            optionsymbol = str(Symbol)+'_'+str(exp_date)
            OP_dict[optionsymbol]= dictofOP
            return call_error,OP_dict
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getOPdata Ended')
            globalheader.logging.error('%s %d', 'Commonapi.getOPdata date Error', date_error)
            return date_error,OV_dict
        
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getOPdata Ended')
        globalheader.logging.error('%s %d', 'Commonapi.getOPdata file Error', file_error)

        return file_error,OV_dict

# getOVdata(Symbol,exp_date,date,contracttype,strikepricelist) return option volume of the stock of the particular exp date of the particular trading day of an option type(call or put)   
    #input
        #Symbol - stock symbol
        # exp_date - option exp date
        #date - trading date
        #contractype - call(0) or put(1)
        #strikepricelist - option strike price list
    #output
        # call_error - success or standard erro
        #OV_dict  - 2d option volume dictionary
def getOVdata(Symbol,exp_date,date,contracttype,strikepricelist):
    OV_dict = OrderedDict()
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getOVdata Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            optionVolume_list = []
            optionsymbolstrikeprice_list = []
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                if(call_error == globalheader.Success):
                    length = len(CSVOptionSymbolList)
                    while i < length:
                        if(symbol == CSVOptionSymbolList[i]):
                            optionsymbolstrikeprice_list.append(strikepricelist[i])
                            optionVolume = getrowdata(i,countcols,Symbol,contracttype)
                            optionVolume = str(optionVolume).split(Commonapi.data_seperator)
                            if Commonapi.listOfStr[4] in optionVolume:
                                optionVolume = Commonapi.ConvertLst_Dict(optionVolume)
                                OV = optionVolume['OV']
                                OV = str(OV)
                                OV = OV.split(',')
                                optionVolume['OV'] = OV[0]
                                if(optionVolume['OV'] == 'U' or optionVolume['OV'] == ',' or optionVolume['OV'] == '.' or optionVolume['OV'] == "'" or  optionVolume['OV'] == ''):
                                    optionVolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
                                    if(globalheader.info == 1):
                                        globalheader.logging.info('dataapi.getOVdata Ended')
                                    globalheader.logging.error('%s %d', 'dataapi.getOVdata file Error', optionVolume_error)       
                                    return optionVolume_error,0
                                else:
                                    optionVolume_list.append(optionVolume['OV'])
                            else:
                                call_error, OV =Commonapi.getoptionVolume(optionVolume )
                                optionVolume_list.append(OV)
                        i += 1
                else:
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.getOVdata Ended')
                    globalheader.logging.error('%s %d', 'Commonapi.getSymbol file Error', call_error)                    
                    return call_error,OV_dict
                
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getOVdata Ended')
            zipbObj = zip(optionsymbolstrikeprice_list,optionVolume_list)
            dictofOV = OrderedDict(zipbObj)
            optionsymbol = str(Symbol)+'_'+str(exp_date)
            OV_dict[optionsymbol]= dictofOV
            return call_error,OV_dict
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getOVdata Ended')
            globalheader.logging.error('%s %d', 'dataapi.getOVdata date Error', date_error)
            return date_error,OV_dict
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getOVdata Ended')
        globalheader.logging.error('%s %d', 'dataapi.getOVdata file Error', file_error)
        return file_error,OV_dict

# getSVdata(Symbol,exp_date,date,contracttype,strikepricelist) return stock volume of the stock of the particular exp date of the particular trading day of an option type(call or put)   
    #input
        #Symbol - stock symbol
        # exp_date - option exp date
        #date - trading date
        #contractype - call(0) or put(1)
        #strikepricelist - option strike price list
    #output
        # call_error - success or standard erro
        #SV_dict  - 2d stock volume dictionary
def getSVdata(Symbol,exp_date,date,contracttype,strikepricelist):
    SV_dict = OrderedDict()
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getSVdata Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error ==  globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            stockVolume_list = []
            optionsymbolstrikeprice_list = []
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                if(call_error ==  globalheader.Success):
                    length = len(CSVOptionSymbolList)
                    while i < length:
                        if(symbol == CSVOptionSymbolList[i]):
                            optionsymbolstrikeprice_list.append(strikepricelist[i])
                            stockVolume = getrowdata(i,countcols,Symbol,contracttype)
                            stockVolume = str(stockVolume).split(Commonapi.data_seperator)
                            if Commonapi.listOfStr[2] in stockVolume:
                                stockVolume = Commonapi.ConvertLst_Dict(stockVolume)
                                SV = stockVolume['SV']
                                SV = str(SV)
                                SV = SV.split(',')
                                stockVolume['SV'] = SV[0]
                                if(stockVolume['SV'] == 'U' or stockVolume['SV'] == '' or stockVolume['SV'] == '.' or stockVolume['SV'] == "'" or stockVolume['SV'] == ','):
                                    stockVolume_error = globalheader.STOCK_VOL_UNAVAILABLE
                                    if(globalheader.info == 1):
                                        globalheader.logging.info('dataapi.getSVdata Ended')
                                    globalheader.logging.error('%s %d', 'dataapi.getSVdata file Error', file_error)
                                    return stockVolume_error,0
                                else:
                                    stockVolume_list.append(optionPrice['OV'])
                            else:
                                call_error, SV =Commonapi.getstockVolume(stockVolume)
                                stockVolume_list.append(SV)
                        i += 1
                else:
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.getSVdata Ended')
                    globalheader.logging.error('%s %d', 'Commonapi.getSymbol file Error', call_error)
                    return call_error,stockVolume_list
                
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getSVdata Ended')
            zipbObj = zip(optionsymbolstrikeprice_list,stockVolume_list)
            dictofSV = OrderedDict(zipbObj)
            optionsymbol = str(Symbol)+'_'+str(exp_date)
            SV_dict[optionsymbol]= dictofSV
            return call_error,SV_dict
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getSVdata Ended')
            globalheader.logging.error('%s %d', 'dataapi.getSVdata date Error', date_error)
            return date_error,SV_dict
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getSVdata Ended')
        globalheader.logging.error('%s %d', 'dataapi.getSVdata file Error', file_error)
        return file_error,SV_dict
    
# getSPdata(Symbol,exp_date,date,contracttype,strikepricelist) return stock price of the stock of the particular exp date of the particular trading day of an option type(call or put)   
    #input
        #Symbol - stock symbol
        # exp_date - option exp date
        #date - trading date
        #contractype - call(0) or put(1)
        #strikepricelist - option strike price list
    #output
        # call_error - success or standard erro
        #SP_dict  - 2d stock price dictionary
def getSPdata(Symbol,exp_date,date,contracttype,strikepricelist):
    SP_dict = OrderedDict()
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getSPdata Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            stockPrice_list = []
            optionsymbolstrikeprice_list = []
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                if(call_error == globalheader.Success):
                    length = len(CSVOptionSymbolList)
                    while i < length:
                        if(symbol == CSVOptionSymbolList[i]):
                            optionsymbolstrikeprice_list.append(strikepricelist[i])
                            stockPrice = getrowdata(i,countcols,Symbol,contracttype)
                            stockPrice = str(stockPrice).split(Commonapi.data_seperator)
                            if Commonapi.listOfStr[1] in stockPrice:
                                stockPrice = Commonapi.ConvertLst_Dict(stockPrice)
                                SP = stockVolume['SP']
                                SP = str(SP)
                                SP = SP.split(',')
                                stockPrice['SP'] = SP[0]
                                if(stockPrice['SP'] == 'U' or stockPrice['SP'] == '' or stockPrice['SP'] == '.' or stockPrice['SP'] == ',' or stockPrice['SP'] == "'"):
                                    stockPrice_error = globalheader.STOCK_PRICE_UNAVAILABLE
                                    if(globalheader.info == 1):
                                        globalheader.logging.info('dataapi.getSPdata Ended')
                                    globalheader.logging.error('%s %d', 'dataapi.getSPdata Error', stockPrice_error)
                                    return stockPrice_error,0
                                else:
                                    stockPrice_list.append(optionPrice['SP'])
                            else:
                                call_error, SP =Commonapi.getstockPrice(stockPrice)
                                stockPrice_list.append(SV)
                        i += 1
                else:
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.getSPdata Ended')
                    globalheader.logging.error('%s %d', 'Commonapi.getSymbol file Error', call_error)
                    return call_error,stockPrice_list
                
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getSPdata Ended')
            zipbObj = zip(optionsymbolstrikeprice_list,stockPrice_list)
            dictofSP = OrderedDict(zipbObj)
            optionsymbol = str(Symbol)+'_'+str(exp_date)
            SP_dict[optionsymbol]= dictofSP
            return call_error,SP_dict
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getSPdata Ended')
            globalheader.logging.error('%s %d', 'dataapi.getSPdata date Error', date_error)
            return date_error,SP_dict
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getSPdata Ended')
        globalheader.logging.error('%s %d', 'dataapi.getSPdata file Error', file_error)
        return file_error,SP_dict

#getdataframe(iCSVfile) return data frame of stock database csv file  
    #input
        #iCSVfile - stock database csv file
    #output
        # data_frame
def getdataframe(iCSVfile):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getdataframe Started')    
    data_frame = pd.read_csv(iCSVfile, index_col = False)
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getdataframe Endd')
    return data_frame

#getExpDatesListFromCSV(iCSVFile) return exp date list from stock csv file  
    #input
        #iCSVfile - stock database csv file
    #output
        # finalOptionExpDateList - stock exp date list from database csv file
def getExpDatesListFromCSV(iCSVFile):    
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getExpDatesListFromCSV Started')  
    expDateList =[]
    finalOptionExpDateList = []
    data_frame = pd.read_csv(iCSVFile, index_col = False)
    CSVOptionSymbolList= data_frame.Symbol.tolist()
    if(debug == 1):
        print("CSVOptionSymbolList  and length is  :",CSVOptionSymbolList,len(CSVOptionSymbolList))
        
    for index in range(0,len(CSVOptionSymbolList)):
        expdatelist = Commonapi.getOptExpDateFromCSV(CSVOptionSymbolList[index])
        expDateList.append(expdatelist)                
    
    expDateList = Commonapi.removeDuplicateItems(expDateList)
    expDateList= sorted(expDateList)

    for i in range(len(expDateList)):
        finalOptionExpDateList.append(expDateList[i])
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getExpDatesListFromCSV Ended')
    return finalOptionExpDateList

#getExpDatesListFromCSV(iCSVFile) return all strikeprices of an exp date from database stock csv file 
    #input
        #iCSVfile - stock database csv file
        #expdate - expdate of the stock
    #output
        # strikepriceList - list of strikeprices of an exp date from database stock csv file 
def strikePricesFromCSV(expdate,iCSVFile):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.strikePricesFromCSV Started')
    strikepriceList =[]
    data_frame = getdataframe(iCSVFile)
    CSVOptionSymbolList= data_frame.Symbol.tolist()

    strikepricelist =[]
    for index in range(0,len(CSVOptionSymbolList)):                                    
        symbolexpdate1 = Commonapi.getOptExpDateFromCSV(CSVOptionSymbolList[index])
        if(symbolexpdate1 == expdate):
            strikeprice = Commonapi.getOptionStrikePrice(CSVOptionSymbolList[index])
            strikepricelist.append(strikeprice)
    
    strikepricelist = Commonapi.removeDuplicateItems(strikepricelist)
    strikepriceList = sorted(strikepricelist)
    strikepriceList.sort(key=float)
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.strikePricesFromCSV Ended')
    return strikepriceList

#parseInputRowData(colFrom,row,Symbol,contracttype) return parsed open interest from row col cell data 
    #input
        #colFrom - col index
        #row - row index
        #Symbol - option symbol
        #contracttype - call(0) or put(1)s
    #output
        # error - success or standard error
        # OI - open interest
def parseInputRowData(colFrom,row,Symbol,contracttype):    
    rowData = []
    rowData = getrowdata(row,colFrom,Symbol,contracttype)
    if(rowData == 'U'):
        OI =0
        SP =0
        stockPrice = (float)(0)
        strikePrice = (float)(0)
        openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
    else:        
        rowData = str(rowData).replace('[','')
        rowData = str(rowData).replace(']','')
        rowData = str(rowData).split(':')
        if Commonapi.listOfStr[0] in rowData:
            openInterest = Commonapi.ConvertLst_Dict(rowData)
            OI = openInterest['OI']
            OI = str(OI)
            OI = OI.split(',')
            OI = OI[0]
            openInterest['OI'] = OI
            if(openInterest['OI'] == 'U' or openInterest['OI'] == '' or openInterest['OI'] == ',' or openInterest['OI'] == "'"):
                openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
                globalheader.logging.error('%s %d', 'dataapi.parseInputRowData open int Error', openInterest_error)
                OI = 0
            else:
                openInterest_error = globalheader.Success
                OI = openInterest['OI']
        else:
            call_error, OI =Commonapi.getopenInterest(openInterest)
    return openInterest_error,OI

#parseInputRowData(colFrom,row,Symbol,contracttype) return parsed open interest from row col cell data 
    #input
        #colFrom - col index
        #row - row index
        #Symbol - option symbol
        #contracttype - call(0) or put(1)
        #data_frame - stock data frame
    #output
        # error - success or standard error
        # OI - open interest
def parseInputRowData(colFrom,row,Symbol,contracttype,data_frame):    
    rowData = []
    rowData = data_frame.iloc[row,colFrom]
    OI =0
    SP = 0
    if(rowData == 'U'):
        OI =0
        SP =0
        stockPrice = (float)(0)
        strikePrice = (float)(0)
        openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
    else:        
        rowData = str(rowData).replace('[','')
        rowData = str(rowData).replace(']','')
        rowData = str(rowData).split(':')
        if Commonapi.listOfStr[0] in rowData:
            openInterest = Commonapi.ConvertLst_Dict(rowData)
            OI = openInterest['OI']
            OI = str(OI)
            OI = OI.split(',')
            openInterest['OI'] = OI[0]
            if(openInterest['OI'] == 'U' or openInterest['OI'] == '' or openInterest['OI'] == ',' or openInterest['OI'] == "'"):
                openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
                globalheader.logging.error('%s %d', 'dataapi.parseInputRowData open int Error', openInterest_error)
                OI = 0
            else:
                openInterest_error = globalheader.Success
                OI = openInterest['OI']

        else:
            openInterest_error, OI =Commonapi.getopenInterest(rowData)            
    return openInterest_error,OI


#parseInputRowDatas(colFrom,row,Symbol,contracttype) return parsed open interest,option price,stock price from row col cell data 
    #input
        #colFrom - col index
        #row - row index
        #Symbol - option symbol
        #contracttype - call(0) or put(1)
        #data_frame - stock data frame
    #output
        # error - success or standard error
        # OI,OP,SP - open interest,option price,Stock price
def parseInputRowDatas(colFrom,row,Symbol,contracttype,data_frame):
    rowData = []
    rowData = data_frame.iloc[row,colFrom]
    if(rowData == 'U'):
        OI =0
        SP =0
        OP = 0
        data_error = globalheader.STOCK_OPENINT_PRICE_OPTPRICE_UNAVAILABLE
    else:
        rowData = str(rowData).replace('[','')
        rowData = str(rowData).replace(']','')
        rowData = str(rowData).split(':')
        OI = 0
        SP =0
        OP =0
        liststr = ["OI", "SP" ,"OP" ]
        rowdata = Commonapi.ConvertLst_Dict(rowData)
        for i in range(len(liststr)):
            if liststr[i] in rowdata:
                data = rowdata[liststr[i]]
                data = str(data)
                data = data.split(',')
                rowdata[liststr[i]] = data[0]
                if(rowdata[liststr[i]] == 'U' or rowdata[liststr[i]] == '.' or rowdata[liststr[i]] == '' or rowdata[liststr[i]] == "'"):
                    data_error = globalheader.STOCK_OPENINT_PRICE_OPTPRICE_UNAVAILABLE
                    globalheader.logging.error('%s %d', 'dataapi.parseInputRowDatas open int,opt price, stock price  Error', data_error)

                    OI = 0
                    SP = 0
                    OP = 0
                else:
                    data_error = globalheader.Success
                    OI = rowdata['OI']
                    SP = rowdata['SP']
                    OP = rowdata['OP']

            else:
                call_error, OI =Commonapi.getopenInterest(rowData)
                call_error, SP =Commonapi.getstockPrice(rowData)
                call_error, OP =Commonapi.getoptionPrice(rowData)
                data_error = globalheader.Success
                              
    return data_error,OI,OP,SP

#getrowdata(rowindex,colindex,Symbol,contracttype) return row col cell data 
    #input
        #colindex - col index of stock csv fole
        # row index- row index of stock csv file
        #Symbol - stock symbol
        #contracttype - call(0) or put(1)
    #output
        # error - success or standard error
        # rowdata - row col data
def getrowdata(rowindex,colindex,Symbol,contracttype):
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    data_frame = getdataframe(iCSVFile)
    rowdata = data_frame.iloc[rowindex,colindex]
    return rowdata

#getDataFrame(istockfile) return total columns, option symbol list and column header list of the stock call or put csv file
    #input
        #istockfile - database stock csv file
    #output
        #columnheaderList - stock column header list of call or put
        #totalcols - total cols of stock call or put csv file
        #CSVOptionSymbolList - option symbol list of call or put
def getDataFrame(istockfile):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getDataFrame Started')
    data_frame = pd.read_csv(istockfile, index_col = False)
    countRows = data_frame.shape[0]
    countCols = data_frame.shape[1]
    columnheaderList= data_frame.columns.tolist()
    totalcols = countCols-1      
    CSVOptionSymbolList= data_frame.Symbol.tolist()
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getDataFrame Ended')
    return columnheaderList,totalcols,CSVOptionSymbolList

#processColEqual(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol) process data csv cols equal requested col data and writes num of trading days row data of stock file to local output csv file
    #input
        #oCSVOIJumpFile- local output csv file
        #Symbol - option symbol
        #row_index - row index of local output csv file
        #getNumberColsData - num of trading days
        #contracttype - call(0) or put(1)
        #Sym_bol - stock symbol
def processColEqual(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processColEqual Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Sym_bol,csvDataFilePath)
    data_frame = pd.read_csv(iCSVFile, index_col = False)
    colFrom =0
    colTo =0
    countCols = data_frame.shape[1]
    colFrom = countCols-getNumberColsData+1
    colTo = countCols
    totalBlankColsData = getNumberColsData - countCols +1
    outPutValue = []
    rowData =[]
    pastColsDat =[]
    pastColsDat =[]
    doProcess = 1
    j =0
    i =0
    pastColsDat =data_frame.iloc[row_index,colFrom:colTo]

    ### Dd process if columns does not contain 'U'
    for j in range(0,len(pastColsDat)):
        if(pastColsDat[j] == 'U'):
            doProcess = 1
        
    if(doProcess == 1):
        optSymbol = Symbol
        addDataoFile = 1
        outPutValue =[]
        rowData = data_frame.iloc[row_index,colFrom:colTo]
        outPutValue = Commonapi.parseURowData(rowData)
        
        for item in range(0,len(outPutValue)):
            if(outPutValue[item] == 'NU'):
                addDataoFile = 0
                    
        if(addDataoFile == 1):                                            
            colItem = []
            rowItem =[]
            k = 0
            totalBlankColsData = getNumberColsData - countCols +1                                            
            for i in range(totalBlankColsData):
                value = 0
                rowItem.append(value)
            
            rowData = [(optSymbol)+(rowItem)+(outPutValue)]
            globalheader.logging.warning('%s %d', 'dataapi.processColEqual rowdata', rowData)
            call_error = Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processColEqual Ended')


#processColGreater(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol)process data csv cols greater than requested col data and  writes num of trading days row data of stock file to local output csv file
    #input
        #oCSVOIJumpFile- local output csv file
        #Symbol - option symbol
        #row_index - row index of local output csv file
        #getNumberColsData - num of trading days
        #contracttype - call(0) or put(1)
        #Sym_bol - stock symbol
 
def processColGreater(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processColGreater Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Sym_bol,csvDataFilePath)
    data_frame = pd.read_csv(iCSVFile, index_col = False)
    colFrom =0
    colTo =0
    outPutValue = []
    rowData =[]
    pastColsDat =[]
    countCols = data_frame.shape[1]
    colFrom = countCols-getNumberColsData
    colTo = countCols                                    
    pastColsDat =data_frame.iloc[row_index,colFrom:colTo]
    doProcess = 1
     
    ### Dd process if columns does not contain 'U'
    for j in range(0,len(pastColsDat)):
        if(pastColsDat[j] == 'U'):
            #print("No operation row[j],j,optionSymbol: ",pastColsDat[j],j,optionSymbol)
            doProcess = 1
            
    if(doProcess == 1):
        optSymbol = Symbol
        addDataoFile = 1
        outPutValue =[]
        fill = []
        rowFindU =[]
        rowData = data_frame.iloc[row_index,colFrom:colTo]
        
        outPutValue = Commonapi.parseURowData(rowData)           
        for item in range(0,len(outPutValue)):
            if(outPutValue[item] == 'NU'):
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            rowData = [(optSymbol)+(outPutValue)]
            globalheader.logging.warning('%s %d', 'dataapi.processColGreater rowdata', rowData)
            call_error = Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)
            
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processColGreater Ended')


#processColLess(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol)process data csv cols lesser than requested col data and  writes num of trading days row data of stock file to local output csv file
    #input
        #oCSVOIJumpFile- local output csv file
        #Symbol - option symbol
        #row_index - row index of local output csv file
        #getNumberColsData - num of trading days
        #contracttype - call(0) or put(1)
        #Sym_bol - stock symbol
def processColLess(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processColLess Started')
    call_error,iCSVFile = getStockCSVFile(contracttype,Sym_bol,csvDataFilePath)
    data_frame = pd.read_csv(iCSVFile, index_col = False)
    colFrom =0
    colTo =0
    outPutValue = []
    rowData =[]
    pastColsDat =[]
    countCols = data_frame.shape[1]
    colFrom = countCols-(countCols -1)
    colTo = countCols
    rowsData =[]    
    doProcess = 1
    j =0
    i =0
    
    pastColsDat =data_frame.iloc[row_index,colFrom:colTo]
    
    ### Dd process if columns does not contain 'U'
    for j in range(0,len(pastColsDat)):
        if(pastColsDat[j] == 'U'):
            doProcess = 1
            
    if(doProcess == 1):
        optSymbol = Symbol
        addDataoFile = 1
        outPutValue =[]
        rowData = data_frame.iloc[row_index,colFrom:colTo]

        outPutValue = Commonapi.parseURowData(rowData)
        for item in range(0,len(outPutValue)):
            if(outPutValue[item] == 'NU'):
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            colItem = []
            rowItem =[]
            totalBlankColsData = getNumberColsData - countCols +1                                            

            for i in range(totalBlankColsData):
                value = 0
                rowItem.append(value)                                            
            
            rowData = [(optSymbol)+(rowItem)+(outPutValue)]
            globalheader.logging.warning('%s %d', 'dataapi.processColLess rowdata', rowData)
            call_error = Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)
            
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processColLess Ended')


#getStrikePriceMaxPain(strikepriceList,stockprice,strikePriceFromCSV,row,OptionExpDate,colFrom,contracttype,max_pain,symbol,exp_date,data_frame) which return   max pain of call or put of stock option exp date   
    #input
        #symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #money_inv  - money_inv list
        #row - row index
        #strikepriceList - strikepricelist
        #strikePriceFromCSV - strike price
        #stockprice - stock price
        #OptionExpDate - option exp date
    #output 
        #call_error - Success or standard header error
        #maxpain - max pain of a option exp date of call or put
       
def getStrikePriceMaxPain(strikepriceList,stockprice,strikePriceFromCSV,row,OptionExpDate,colFrom,contracttype,max_pain,symbol,exp_date,data_frame):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getStrikePriceMaxPain Started')
    strikeexpdate = Commonapi.getOptExpDateFromCSV(strikePriceFromCSV[row])
    strikeprice = strikepriceList[stockprice]

    if(strikeexpdate == OptionExpDate):
        strikePrice = Commonapi.getOptionStrikePrice(strikePriceFromCSV[row])                        
        stockPrice = strikeprice
    
        stockPrice = (float)(stockPrice)
        strikePrice = (float)(strikePrice)
        call_error,OI = parseInputRowData(colFrom,row,symbol,contracttype,data_frame)
        
        if(contracttype == Commonapi.Contracttype.CALL.value):
            if(stockPrice > strikePrice):                                           
               maxpain = abs(stockPrice-strikePrice)
               max_pain +=maxpain*(float)(OI)
            elif(stockPrice < strikePrice):
               max_pain += 0
            else:
               if(stockPrice == strikePrice):
                    max_pain += 0
               else:
                    max_pain += 0

        if(contracttype == Commonapi.Contracttype.PUT.value):
            if(stockPrice < strikePrice):
               maxpain = abs(stockPrice-strikePrice)
               max_pain += maxpain*(float)(OI)
            elif(stockPrice > strikePrice):
                max_pain += 0 
            else:
                if(stockPrice == strikePrice):
                    max_pain += 0
                else:
                    max_pain += 0
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getStrikePriceMaxPain Ended')
    return (round)(max_pain)


# getMaxPain(Symbol,exp_date,contracttype)  which return  2d dict of max pain of call or put of stock a option exp date of a stock  
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #maxpain_dict - 2d dict of max pain of a option exp date of call or put of a stock
def getMaxPain(Symbol,exp_date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getMaxPain Started')
    maxpain_dict = OrderedDict()
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(istockCSVfilename)
        finalOptionExpDateList = getExpDatesListFromCSV(istockCSVfilename)
        if exp_date in finalOptionExpDateList:
            expdate = finalOptionExpDateList.index(exp_date)
            expDate =[]
            expDate = finalOptionExpDateList[expdate]            
        
            colFrom = 0
            strikeprices = []
            strikeprices_max_pain = []

            del strikeprices[:]
            del strikeprices_max_pain[:]            
           
            columnList,colFrom,strikePriceFromCSV = getDataFrame(istockCSVfilename)
            #initLocalList(MAX_PAIN,colFrom,1)

            strikepriceList = []
            strikepriceList = strikePricesFromCSV(expDate,istockCSVfilename)
            strikeprices = strikepriceList
                
            for col in range(1,colFrom+1):                    
                del strikeprices_max_pain[:]
                    
                for stockprice in range(0,len(strikepriceList)):
                    max_pain = 0
                        
                    for row in range(0,len(strikePriceFromCSV)):
                        max_pain = getStrikePriceMaxPain(strikepriceList,stockprice,strikePriceFromCSV,row,expDate,col,contracttype,max_pain,Symbol,exp_date,data_frame)                                  
                                                                                                                                                   
                    strikeprices_max_pain.append(max_pain)
                        
        #### Adding call max pain of individual strikeprice to excel sheet
                row = col+1                    
                call_error = globalheader.Success
                label = str(columnList[col])            
                zipbObj = zip(strikeprices,strikeprices_max_pain)
                dictofmaxpain = OrderedDict(zipbObj)
                maxpain_dict[label]= dictofmaxpain
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getMaxPain Ended')
            return call_error,maxpain_dict       
        else:
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getMaxPain Ended')
            call_error = globalheader.STOCK_OPT_EXPDATE_DOES_NOT_EXIST
            globalheader.logging.error('%s %d', 'dataapi.getMaxPain stock Error', call_error)

            return call_error,0
            
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getMaxPain Ended')
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        globalheader.logging.error('%s %d', 'dataapi.getMaxPain file Error', call_error)

        return call_error,0


# getAllMaxPain(Symbol,contracttype) which return  3d dict of max pain of call or put of stock all option exp date of a stock  
    #input
        #Symbol - stock symbol
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #maxpain_dict - 3d dict of max pain of all option exp date of call or put of a stock
def getAllMaxPain(Symbol,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getAllMaxPain Started')
    #maxpain_dict = defaultdict(lambda : defaultdict(OrderedDict))
    maxpain_dict = defaultdict(lambda : OrderedDict())
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(istockCSVfilename)
        finalOptionExpDateList = getExpDatesListFromCSV(istockCSVfilename)
        for exp_date in range(0,len(finalOptionExpDateList)):
            expDate = finalOptionExpDateList[exp_date]            
        
            colFrom = 0
            strikeprices = []
            strikeprices_max_pain = []

            del strikeprices[:]
            del strikeprices_max_pain[:]            
           
            columnList,totalcols,strikePriceFromCSV = getDataFrame(istockCSVfilename)
            #initLocalList(MAX_PAIN,colFrom,1)
            colFrom = totalcols - 40
            
            strikepriceList = []
            strikepriceList = strikePricesFromCSV(expDate,istockCSVfilename)
            strikeprices = strikepriceList
                
            for col in range(colFrom,totalcols+1):                    
                del strikeprices_max_pain[:]
                for stockprice in range(0,len(strikepriceList)):
                    max_pain = 0
                        
                    for row in range(0,len(strikePriceFromCSV)):
                        max_pain = getStrikePriceMaxPain(strikepriceList,stockprice,strikePriceFromCSV,row,expDate,col,contracttype,max_pain,Symbol,exp_date,data_frame)                                  
                                                                                                                                                   
                    strikeprices_max_pain.append(max_pain)
                        
        #### Adding call max pain of individual strikeprice to excel sheet
                call_error = globalheader.Success
                label = str(columnList[col])            
                zipbObj = zip(strikeprices,strikeprices_max_pain)
                dictofmaxpain = OrderedDict(zipbObj)
                maxpain_dict[expDate][label]= dictofmaxpain
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getAllMaxPain Ended')
        return call_error,maxpain_dict       
                    
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getAllMaxPain Ended')
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        globalheader.logging.error('%s %d', 'dataapi.getAllMaxPain stock Error', call_error)
        return call_error,0

#getStrikePriceMoneyInv(strikepriceList,stockprice,strikePriceFromCSV,row,OptionExpDate,colFrom,contracttype,money_inv,symbol,data_frame) which return  2d dict of money investment of call or put of stock option exp date   
    #input
        #symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #money_inv  - money_inv list
        #row - row index
        #strikepriceList - strikepricelist
        #strikePriceFromCSV - strike price
        #stockprice - stock price
        #OptionExpDate - option exp date
        #colFrom - col index of stock database csv file

    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 2d dict of money investment of a option exp date of call or put
def getStrikePriceMoneyInv(strikepriceList,stockprice,strikePriceFromCSV,row,OptionExpDate,colFrom,contracttype,money_inv,symbol,data_frame):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getStrikePriceMoneyInv Started')
    strikeexpdate = Commonapi.getOptExpDateFromCSV(strikePriceFromCSV[row])
    strikeprice = (float)(Commonapi.getOptionStrikePrice(strikePriceFromCSV[row]))
    strikeprice = (float)(strikeprice)

    if((strikeexpdate == OptionExpDate) and ((float)(strikepriceList[stockprice]) == strikeprice)):
        strikePrice = Commonapi.getOptionStrikePrice(strikePriceFromCSV[row])                        
        stockPrice = strikeprice
        
        stockPrice = (float)(stockPrice)
        strikePrice = (float)(strikePrice)
        call_error,OI,OP,SP= parseInputRowDatas(colFrom,row,symbol,contracttype,data_frame)
        if(call_error == globalheader.Success):
            money_inv = (float)(OI)*(float)(OP)*100
            money_inv = money_inv/1000
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getStrikePriceMoneyInv Ended')
    return (round)(money_inv)


#getmoneyinv(Symbol,exp_date,contracttype) which return  2d dict of money investment of call or put of stock option exp date   
    #input
        #Sym_bol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 2d dict of money investment of a option exp date of call or put    
def getmoneyInv(Symbol,exp_date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getmoneyInv Started')
    moneyinv_dict = OrderedDict()
    finalOptionExpDateList =[]    
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    #Loop around num of expiration x contracttype x getNumberColsData x strikeprices
    if(call_error == globalheader.Success):
        print("File Exists")
        data_frame = getdataframe(istockCSVfilename)
        finalOptionExpDateList = getExpDatesListFromCSV(istockCSVfilename)
        if exp_date in finalOptionExpDateList:
            expdate = finalOptionExpDateList.index(exp_date)
            expDate =[]
            expDate = finalOptionExpDateList[expdate]                           
    
            colFrom = 0
            strikeprices = []
            strike_money_inv = []
            col=[]
            columnList,colFrom,strikePriceFromCSV = getDataFrame(istockCSVfilename)
#            print("len(columnList) is :",columnList)
            
            strikepriceList = []
            strikepriceList = strikePricesFromCSV(expDate,istockCSVfilename)
            strikeprices = strikepriceList

            for col in range(1,colFrom+1):                    
                del strike_money_inv[:]
                
                for stockprice in range(0,len(strikepriceList)):
                    money_inv = 0
                    
                    for row in range(0,len(strikePriceFromCSV)):
                        money_inv= getStrikePriceMoneyInv(strikepriceList,stockprice,strikePriceFromCSV,row,finalOptionExpDateList[expdate],col,contracttype,money_inv,Symbol,data_frame)
                                                                   
                    strike_money_inv.append(money_inv)
                
                call_error = globalheader.Success
                label = str(columnList[col])
            
                zipbObj = zip(strikeprices,strike_money_inv)
                dictofmoneyinv = OrderedDict(zipbObj)
                moneyinv_dict[label]= dictofmoneyinv
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getmoneyInv Ended')
            return call_error,moneyinv_dict       
        else:
            call_error = globalheader.STOCK_OPT_EXPDATE_DOES_NOT_EXIST
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getmoneyInv Ended')
            globalheader.logging.error('%s %d', 'dataapi.getmoneyInv stock  opt exp Error', call_error)
            return call_error,0
            
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getmoneyInv Ended')
        globalheader.logging.error('%s %d', 'dataapi.getmoneyInv stock file Error', call_error)

        return call_error,0

#getAllmoneyinv(Symbol,contracttype) which return  3d dict of money investment of call or put of stock all option exp date of a stock  
    #input
        #Symbol - stock symbol
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 3d dict of money investment of all option exp date of call or put of a stock
def getAllmoneyInv(Symbol,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getAllmoneyInv Started')
    moneyinv_dict = defaultdict(lambda : OrderedDict())
    finalOptionExpDateList =[]    
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(istockCSVfilename)
        finalOptionExpDateList = getExpDatesListFromCSV(istockCSVfilename)
        for exp_date in range(len(finalOptionExpDateList)):
            expdate = finalOptionExpDateList[exp_date]                           
    
            colFrom = 0
            strikeprices = []
            strike_money_inv = []
            col=[]
            columnList,totalCols,strikePriceFromCSV = getDataFrame(istockCSVfilename)
            colFrom = totalCols - 40
            strikepriceList = []
            strikepriceList = strikePricesFromCSV(expdate,istockCSVfilename)
            strikeprices = strikepriceList

            for col in range(colFrom,totalcols+1):                    
                del strike_money_inv[:]
                
                for stockprice in range(0,len(strikepriceList)):
                    money_inv = 0
                    
                    for row in range(0,len(strikePriceFromCSV)):
                        money_inv= getStrikePriceMoneyInv(strikepriceList,stockprice,strikePriceFromCSV,row,expdate,col,contracttype,money_inv,Symbol,data_frame)
                                                                   
                    strike_money_inv.append(money_inv)
                
                call_error = globalheader.Success
                
                label = str(columnList[col])            
                zipbObj = zip(strikeprices,strike_money_inv)
                dictofmoneyinv = OrderedDict(zipbObj)
                moneyinv_dict[expdate][label]= dictofmoneyinv
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getAllmoneyInv Ended')
        return call_error,moneyinv_dict       

    else:
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getAllmoneyInv Ended')
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        globalheader.logging.error('%s %d', 'dataapi.getmoneyInv stock file Error', call_error)

        return call_error,0  

def initLocalList(OTM,OTMOI,finalOptionExpDateList,getNumberColsData):
    for i in range(0,len(finalOptionExpDateList)):
        OTM.append([])                
        for j in range(0,getNumberColsData):
            OTM[i].append([])
            for k in range(len(OITM)):
                OTM[i][j].append([])
    for i in range(0,len(finalOptionExpDateList)):
        for j in range(0,getNumberColsData):
            for k in range(len(OITM)):
                val = (int)(0)
                OTM[i][j][k] = val

    for i in range(0,len(finalOptionExpDateList)):
        OTMOI.append([])                
        for j in range(0,getNumberColsData):
            OTMOI[i].append([])
            for k in range(len(OITM)):
                OTMOI[i][j].append([])
    for i in range(0,len(finalOptionExpDateList)):
        for j in range(0,getNumberColsData):
            for k in range(len(OITM)):
                val = (int)(0)
                OTMOI[i][j][k] = val

#getStrikePriceMoneyInvExpDateAllData(strikepriceList,stockprice,strikePriceFromCSV,row,OptionExpDate,colFrom,contracttype,money_inv,symbol,data_frame,OTM,OTMOI) which return  2d dict of money investment,OTM,OTMOI of call or put of stock option exp date   
    #input
        #symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #money_inv  - money_inv list
        #row - row index
        #strikepriceList - strikepricelist
        #strikePriceFromCSV - strike price
        #stockprice - stock price
        #OptionExpDate - option exp date
        #colFrom - col index of stock database csv file
        #OTM - out-of the-money- in-the-money list
        #OTMOI out-of the-money- in-the-money list open interest list
    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 2d dict of money investment of a option exp date of call or put
        #OTM_dict - 2d dict of in-the-money,out-of-the-money investment of a option exp date of call or put
        #OTMIO_dict - 2d dict of in-the-money,out-of-the-money open interest of a option exp date of call or put
def getStrikePriceMoneyInvExpDateAllData(strikepriceList,stockprice,strikePriceFromCSV,row,OptionExpDate,colFrom,contracttype,money_inv,symbol,data_frame,OTM,OTMOI):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getStrikePriceMoneyInvExpDateAllData Started')
    strikeexpdate = Commonapi.getOptExpDateFromCSV(strikePriceFromCSV[row])
    strikeprice = (float)(Commonapi.getOptionStrikePrice(strikePriceFromCSV[row]))
    strikeprice = (float)(strikeprice)

    if((strikeexpdate == OptionExpDate) and ((float)(strikepriceList[stockprice]) == strikeprice)):
        strikePrice = Commonapi.getOptionStrikePrice(strikePriceFromCSV[row])                        
        stockPrice = strikeprice
        
        stockPrice = (float)(stockPrice)
        strikePrice = (float)(strikePrice)
        call_error,OI,OP,SP= parseInputRowDatas(colFrom,row,symbol,contracttype,data_frame)
        if(call_error == globalheader.Success):
            money_inv = (float)(OI)*(float)(OP)*100
            money_inv = money_inv/1000

            if(contracttype == Commonapi.Contracttype['CALL'].value):
                if((float)(SP) > (float)(strikeprice)):
                    value = OTM[0]
                    value += money_inv 
                    OTM[0] = (round)(value)
                    value = OTMOI[0]
                    value += (float)(OI)
                    OTMOI[0] = (round)(value)
                else:
                    value = OTM[1]
                    value += money_inv 
                    OTM[1] = (round)(value)
                    value = OTMOI[1]
                    value += (float)(OI)
                    OTMOI[1] = (round)(value)

            if(contracttype == Commonapi.Contracttype['PUT'].value):
                if((float)(SP) < (float)(strikeprice)):
                    value = OTM[0]
                    value += money_inv 
                    OTM[0] = (round)(value)
                    value = OTMOI[0]
                    value += (float)(OI)
                    OTMOI[0] = (round)(value)
                else:
                    value = OTM[1]
                    value += money_inv 
                    OTM[1] = (round)(value)
                    value = OTMOI[1]
                    value += (float)(OI)
                    OTMOI[1] = (round)(value)
                    
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getStrikePriceMoneyInvExpDateAllData Ended')
    return (round)(money_inv),OTM,OTMOI


#getmoneyInvExpDateAllData(Symbol,exp_date,contracttype) which return  2d dict of money investment,2d dict of total money,in-the-money,out-of-the-money open interest
#in-the-money,out-of-the-money total money of call or put of stock option exp date   
    #input
        #Sym_bol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 2d dict of money investment of a option exp date of call or put
        #OTM_dict - 2d dict of in-the-money,out-of-the-money investment of a option exp date of call or put
        #OTMIO_dict - 2d dict of in-the-money,out-of-the-money open interest of a option exp date of call or put
        #TMI_dict - 2d dict of total money investment of a option exp date of call or put
def getmoneyInvExpDateAllData(Symbol,exp_date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getmoneyInvExpDateAllData Started')
    moneyinv_dict = OrderedDict()
    OTM_dict =OrderedDict()
    OTMOI_dict = OrderedDict()
    TM_dict = OrderedDict()
    finalOptionExpDateList =[]
    
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    #Loop around num of expiration x contracttype x getNumberColsData x strikeprices
    if(call_error == globalheader.Success):
        data_frame = getdataframe(istockCSVfilename)
        finalOptionExpDateList = getExpDatesListFromCSV(istockCSVfilename)
        if exp_date in finalOptionExpDateList:
            expdate = finalOptionExpDateList.index(exp_date)
            expDate =[]
            expDate = finalOptionExpDateList[expdate]                           
    
            colFrom = 0
            strikeprices = []
            strike_money_inv = []
                        
            col=[]
            total_money_inv = [0]
            columnList,colFrom,strikePriceFromCSV = getDataFrame(istockCSVfilename)
            
            strikepriceList = []
            strikepriceList = strikePricesFromCSV(expDate,istockCSVfilename)
            strikeprices = strikepriceList

            for col in range(1,colFrom+1):                    
                del strike_money_inv[:]
                OTM = [0,0]
                OTMOI = [0,0]
                TMI = [0]
                for stockprice in range(0,len(strikepriceList)):
                    money_inv = 0                  
                    for row in range(0,len(strikePriceFromCSV)):
                        money_inv,OTM,OTMOI= getStrikePriceMoneyInvExpDateAllData(strikepriceList,stockprice,strikePriceFromCSV,row,finalOptionExpDateList[expdate],col,contracttype,money_inv,Symbol,data_frame,OTM,OTMOI)
                        
                    strike_money_inv.append(money_inv)
                    TMI[0] += money_inv
                
                call_error = globalheader.Success
                label = str(columnList[col])            
                zipbObj = zip(strikeprices,strike_money_inv)
                dictofmoneyinv = OrderedDict(zipbObj)
                moneyinv_dict[label]= dictofmoneyinv
                
                if(contracttype == Commonapi.Contracttype['CALL'].value):                    
                    TM =['CallTM']  
                    zipbObj = zip(TM,TMI)
                    dictofmoneyinvTM = OrderedDict(zipbObj)
                    TM_dict[label]= dictofmoneyinvTM
                else:
                    TM =['PutTM']  
                    zipbObj = zip(TM,TMI)
                    dictofmoneyinvTM = OrderedDict(zipbObj)
                    TM_dict[label]= dictofmoneyinvTM
                    
                if(contracttype == Commonapi.Contracttype['CALL'].value):                    
                    OITM =['CallITM','CallOTM']  
                    zipbObj = zip(OITM,OTM)
                    dictofmoneyinvOTM = OrderedDict(zipbObj)
                    OTM_dict[label]= dictofmoneyinvOTM
                else:
                    OITM =['PutITM','PutOTM']  
                    zipbObj = zip(OITM,OTM)
                    dictofmoneyinvOTM = OrderedDict(zipbObj)
                    OTM_dict[label]= dictofmoneyinvOTM

                if(contracttype == Commonapi.Contracttype['CALL'].value):
                    OITMOI =['CallITMOI','CallOTMOI']
                    zipbObj = zip(OITMOI,OTMOI)
                    dictofmoneyinvOTMOI = OrderedDict(zipbObj)
                    OTMOI_dict[label]= dictofmoneyinvOTMOI
                else:
                    OITMOI =['PutITMOI','PtOTMOI']
                    zipbObj = zip(OITMOI,OTMOI)
                    dictofmoneyinvOTMOI = OrderedDict(zipbObj)
                    OTMOI_dict[label]= dictofmoneyinvOTMOI
                    
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getmoneyInvExpDateAllData Ended')    
            return call_error,moneyinv_dict,OTM_dict,OTMOI_dict,TM_dict      
        else:
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.getmoneyInvExpDateAllData Ended')
            call_error = globalheader.STOCK_OPT_EXPDATE_DOES_NOT_EXIST
            globalheader.logging.error('%s %d', 'dataapi.getmoneyInvExpDateAllData stock opt exp Error', call_error)

            return call_error,0,0,0,0
            
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getmoneyInvExpDateAllData Ended')
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        globalheader.logging.error('%s %d', 'dataapi.getmoneyInvExpDateAllData stock file Error', call_error)

        return call_error,0,0,0,0


#getmoneyInvExpDateAllData(Symbol,exp_date,contracttype) which return  3d dict of money investment,2d dict of total money,in-the-money,out-of-the-money open interest
#in-the-money,out-of-the-money total money of call or put of all stock option exp date   
    #input
        #Sym_bol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 3d dict of money investment of a option exp date of call or put
        #OITM_dict - 3d dict of in-the-money,out-of-the-money investment of all option exp date of call or put
        #OTMOI_dict - 3d dict of in-the-money,out-of-the-money open interest of all option exp date of call or put
        #TMI_dict - 3d dict of total money investment of all option exp date of call or put
def getmoneyInvAllExpDateAllData(Symbol,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.getmoneyInvAllExpDateAllData Started')
    moneyinv_dict = defaultdict(lambda : OrderedDict())
    OTM_dict = defaultdict(lambda : OrderedDict())
    OTMOI_dict = defaultdict(lambda : OrderedDict())
    TM_dict = defaultdict(lambda : OrderedDict())
    finalOptionExpDateList =[]
    
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    #Loop around num of expiration x contracttype x getNumberColsData x strikeprices
    if(call_error == globalheader.Success):
        data_frame = getdataframe(istockCSVfilename)
        finalOptionExpDateList = getExpDatesListFromCSV(istockCSVfilename)
        for exp_date in range(0,len(finalOptionExpDateList)):
            expDate =[]
            expDate = finalOptionExpDateList[exp_date]                           
    
            colFrom = 0
            strikeprices = []
            strike_money_inv = []            
            
            col=[]
            total_money_inv = [0]
            columnList,totalcols,strikePriceFromCSV = getDataFrame(istockCSVfilename)
            colFrom = totalcols - 40
            strikepriceList = []
            strikepriceList = strikePricesFromCSV(expDate,istockCSVfilename)
            strikeprices = strikepriceList

            for col in range(colFrom,totalcols+1):                    
                del strike_money_inv[:]
                OTM = [0,0]
                OTMOI = [0,0]
                TMI = [0]
                for stockprice in range(0,len(strikepriceList)):
                    money_inv = 0                  
                    for row in range(0,len(strikePriceFromCSV)):
                        money_inv,OTM,OTMOI= getStrikePriceMoneyInvExpDateAllData(strikepriceList,stockprice,strikePriceFromCSV,row,finalOptionExpDateList[exp_date],col,contracttype,money_inv,Symbol,data_frame,OTM,OTMOI)
                        
                    strike_money_inv.append(money_inv)
                    TMI[0] += money_inv
                
                call_error = globalheader.Success
                label = str(columnList[col])            
                zipbObj = zip(strikeprices,strike_money_inv)
                dictofmoneyinv = OrderedDict(zipbObj)
                moneyinv_dict[expDate][label]= dictofmoneyinv
                
                if(contracttype == Commonapi.Contracttype['CALL'].value):                    
                    TM =['CallTM']  
                    zipbObj = zip(TM,TMI)
                    dictofmoneyinvTM = OrderedDict(zipbObj)
                    TM_dict[expDate][label]= dictofmoneyinvTM
                else:
                    TM =['PutTM']  
                    zipbObj = zip(TM,TMI)
                    dictofmoneyinvTM = OrderedDict(zipbObj)
                    TM_dict[expDate][label]= dictofmoneyinvTM
                    
                if(contracttype == Commonapi.Contracttype['CALL'].value):                    
                    OITM =['CallITM','CallOTM']  
                    zipbObj = zip(OITM,OTM)
                    dictofmoneyinvOTM = OrderedDict(zipbObj)
                    OTM_dict[expDate][label]= dictofmoneyinvOTM
                else:
                    OITM =['PutITM','PutOTM']  
                    zipbObj = zip(OITM,OTM)
                    dictofmoneyinvOTM = OrderedDict(zipbObj)
                    OTM_dict[expDate][label]= dictofmoneyinvOTM

                if(contracttype == Commonapi.Contracttype['CALL'].value):
                    OITMOI =['CallITMOI','CallOTMOI']
                    zipbObj = zip(OITMOI,OTMOI)
                    dictofmoneyinvOTMOI = OrderedDict(zipbObj)
                    OTMOI_dict[expDate][label]= dictofmoneyinvOTMOI
                else:
                    OITMOI =['PutITMOI','PtOTMOI']
                    zipbObj = zip(OITMOI,OTMOI)
                    dictofmoneyinvOTMOI = OrderedDict(zipbObj)
                    OTMOI_dict[expDate][label]= dictofmoneyinvOTMOI
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getmoneyInvAllExpDateAllData Ended')        
        return call_error,moneyinv_dict,OTM_dict,OTMOI_dict,TM_dict      
            
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.getmoneyInvAllExpDateAllData Ended')
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        globalheader.logging.error('%s %d', 'dataapi.getmoneyInvAllExpDateAllData stock file Error', call_error)

        return call_error,0,0,0,0

    
#parseOIdata(openinterest,symbol) return parsed open interest from row cell data  
    #input
        #openinterest - col row cell data
        #symbol - stock symbol
    #output 
        #openInterest_error - Success or STOCK_OPEN_INT_UNAVAILABLE
        #OI - open interest value
def parseOIdata(openinterest,symbol):
    OI_dict = OrderedDict()
    openInterest = str(openinterest).split(Commonapi.data_seperator)
    if Commonapi.listOfStr[0] in openInterest:
        openInterest = Commonapi.ConvertLst_Dict(openInterest)
        OI = openInterest['OI']
        OI = str(OI)
        OI = OI.split(',')
        openInterest['OI'] = OI[0]
        if(openInterest['OI'] == 'U' or openInterest['OI'] == '' or openInterest['OI'] == ',' or openInterest['OI'] == "'" or openInterest['OI'] == ''):
            openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
            globalheader.logging.error('%s %d', 'dataapi.parseOIdata Error', openInterest_error)
            return openInterest_error,0
        else:
            openInterest_error = globalheader.Success
            OI = openInterest['OI']                        
            return openInterest_error, OI
        
    else:
        openInterest_error, OI =Commonapi.getopenInterest(openInterest)
        if(openInterest_error == globalheader.Success):            
            return openInterest_error, OI
        else:
            globalheader.logging.error('%s %d', 'dataapi.parseOIdata Error', openInterest_error)
            return openInterest_error, OI

#parseOPdata(optionprice,symbol) return parsed option price from row cell data  
    #input
        #option price - col row cell data
        #symbol - stock symbol
    #output 
        #option price_error - Success or STOCK_OPT_PRICE_UNAVAILABLE
        #OP - option price value
def parseOPdata(optionprice,symbol):
    OP_dict = OrderedDict()
    optionPrice = str(optionprice).split(Commonapi.data_seperator)
    if Commonapi.listOfStr[3] in optionPrice:
        optionPrice = Commonapi.ConvertLst_Dict(optionPrice)
        OP = optionPrice['OP']
        OP = str(OP)
        OP = OP.split(',')
        optionPrice['OP'] = OP[0]
        if(optionPrice['OP'] == 'U' or optionPrice['OP'] == '.' or optionPrice['OP'] == ',' or optionPrice['OP'] == "'" or optionPrice['OP'] == ''):
            optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
            globalheader.logging.error('%s %d', 'dataapi.parseOPdata Error', optionPrice_error)
            return optionPrice_error,0
        else:
            optionPrice_error = globalheader.Success
            OP = optionPrice['OP']            
            return optionPrice_error, OP
        
    else:
        optionPrice_error, OP =Commonapi.getoptionPrice(optionPrice)
        if(optionPrice_error == globalheader.Success):            
            return optionPrice_error, OP
        else:
            globalheader.logging.error('%s %d', 'dataapi.parseOPdata Error', optionPrice_error)
            return optionPrice_error, OP

#parseOVdata(optionvolume,symbol) return parsed option volume from row cell data  
    #input
        #option volume - col row cell data
        #symbol - stock symbol
    #output 
        #optionVolume_error - Success or STOCK_OPT_VOLUME_UNAVAILABLE
        #OV - option volume value
def parseOVdata(optionvolume,symbol):
    optionVolume = str(optionvolume).split(Commonapi.data_seperator)
    if Commonapi.listOfStr[4] in optionVolume:
        optionVolume = Commonapi.ConvertLst_Dict(optionVolume)
        OV = optionVolume['OV']
        OV = str(OV)
        OV = OV.split(',')
        optionVolume['OV'] = OV[0]
        if(optionVolume['OV'] == 'U' or optionVolume['OV'] == ',' or optionVolume['OV'] == '.' or optionVolume['OV'] == "'" or optionVolume['OV'] == ''):
            optionVolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
            globalheader.logging.error('%s %d', 'dataapi.parseOVdata Error', optionVolume_error)
            return optionVolume_error,0
        else:
            optionVolume_error = globalheader.Success
            OV = optionVolume['OV']            
            return optionVolume_error, OV
    else:
        optionVolume_error, OV =Commonapi.getoptionVolume(optionVolume)
        if(optionVolume_error == globalheader.Success):            
            return optionVolume_error, OV
        else:
            globalheader.logging.error('%s %d', 'dataapi.parseOVdata Error', optionVolume_error)
            return optionVolume_error, OV

#jumpinOI(todayrowData,yestrowData,thresold,money_margin,symbol) compares today OI,OV with yest OI,OV than send value if greater than thresold
    #input
        #todayrowData - col row cell data open interest
        #testrowData - col row cell data open interest
        #symbol - stock symbol
        #thresold - min value open interest, option volume should be
        #money_margin - min money invested in option strike price
        
    #output 
        #optionInterest_error - Success or standard error
        #OI - open interest value        
def jumpinOI(todayrowData,yestrowData,thresold,money_margin,symbol):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.jumpinOI Started')
    call_error_TodayOI,TodayOI = parseOIdata(todayrowData,symbol)
    call_error_YestOI,YestOI = parseOIdata(yestrowData,symbol)
    call_error_TodayOP,TodayOP = parseOPdata(todayrowData,symbol)

    if(globalheader.debug == 1):
        globalheader.logging.error('%s %d %d', 'dataapi.jumpinOI data', TodayOI,YestOI)

    if(call_error_TodayOI == globalheader.Success and call_error_YestOI == globalheader.Success):
        if((int)(TodayOI)!=0 and (int)(YestOI)==0):
            if((int)(TodayOI) > (int)(thresold)):
                value = (((int)(TodayOI)/100)*100)
                value = (round)(value)
                if(value > thresold):
                    if(call_error_TodayOP == globalheader.Success):
                        moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                        if(moneyinv > money_margin):
                            value = (round)(value)
                            if(globalheader.info == 1):
                                globalheader.logging.info('dataapi.jumpinOI Ended')
                            return call_error_TodayOI,value
                        else:
                            optionInterest_error = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                            if(globalheader.info == 1):
                                globalheader.logging.info('dataapi.jumpinOI Ended')
                            globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock opt price Error', optionInterest_error)
                            return optionInterest_error,value
                    else:
                        optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
                        if(globalheader.info == 1):
                            globalheader.logging.info('dataapi.jumpinOI Ended')
                        globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock opt price Error', optionInterest_error)
                        return optionPrice_error,0  
                else:
                    optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.jumpinOI Ended')
                    globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock open int Error', optionInterest_error)
                    return optionInterest_error,0
            else:
                optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.jumpinOI Ended')
                globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock open int Error', optionInterest_error)
                return optionInterest_error,0

            
        elif((int)(TodayOI)!=0 and (int)(YestOI)!=0):
            if((int)(TodayOI)>(int)(thresold) and (int)(YestOI)>(int)(thresold)):
                if((int)(TodayOI) == (int)(YestOI)):
                    value = 0
                    optionInterest_error = globalheader.STOCK_OPEN_INT_ZERO
                    return optionInterest_error,value
                elif((int)(TodayOI)>(int)(YestOI)):
                    value = ((((int)(TodayOI) - (int)(YestOI))/(int)(YestOI))*100)
                    value = (round)(value)
                    if(value > thresold):
                        if(call_error_TodayOP == globalheader.Success):
                            moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                            if(moneyinv > money_margin):
                                value = (round)(value)
                                if(globalheader.info == 1):
                                    globalheader.logging.info('dataapi.jumpinOI Ended')
                                return call_error_TodayOI,value
                            else:
                                optionInterest_error = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                                if(globalheader.info == 1):
                                    globalheader.logging.info('dataapi.jumpinOI Ended')
                                globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock opt price Error', optionInterest_error)
                                return optionInterest_error,0
                        else:
                            if(globalheader.info == 1):
                                globalheader.logging.info('dataapi.jumpinOI Ended')
                            globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock opt price Error', call_error_Today_OP)
                            return call_error_TodayOP,0
                    else:
                        if(globalheader.info == 1):
                            globalheader.logging.info('dataapi.jumpinOI Ended')
                        optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                        globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock open int Error', optionInterest_error)
                        return optionInterest_error,0
 
                else:
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.jumpinOI Ended')
                    optionInterest_error = globalheader.STOCK_OPEN_INT_NO_CHANGE_IN_PERCENTAGE
                    globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock open int Error', optionInterest_error)
                    return optionInterest_error,0 
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.jumpinOI Ended')
                optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock open int Error', optionInterest_error)
                return optionInterest_error,0
        else:
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.jumpinOI Ended')
            optionInterest_error = globalheader.STOCK_OPEN_INT_ZERO
            globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock open int Error', optionInterest_error)
            return optionInterest_error,0 

    else:
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.jumpinOI Ended')
        optionInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
        globalheader.logging.error('%s %d', 'dataapi.jumpinOI stock open int Error', optionInterest_error)
        return optionInterest_error,0 
    
    
#jumpOIAllstocks(totalStocks,stockSymbol,ofilename,thresold,Percentage_OI_Jump,money_margin,getNumberColsData) compares today OI with yest OI than campare value if greater than thresold and
#store in local output jump OI csv file of all stocks
    #input
        #totalStocks - total num of stocks
        #stockSymbol - stock symbol list
        #ofilename - local output jump OV csv file
        #todayrowData - col row cell data open interest
        #testrowData - col row cell data open interest
        #symbol - stock symbol
        #thresold - min value option volume should be
        #money_margin - min money invested in option strike price
        
    #output 
        #call_error - Success or standard error
def jumpOIAllstocks(totalStocks,stockSymbol,ofilename,thresold,Percentage_OI_Jump,money_margin,getNumberColsData):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.jumpOIAllstocks Started')
    oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)    
    
    if os.path.exists(oCSVOIJumpFile):
        globalheader.logging.warning('%s %s', 'dataapi.jumpOIAllstocks file exists', oCSVOIJumpFile)
        os.remove(oCSVOIJumpFile)
        globalheader.logging.warning('file removed')
        
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)
            data_frame = 0
            if os.path.exists(oCSVOIJumpFile):
                globalheader.logging.warning('%s %s', 'dataapi.jumpOIAllstocks file exists', oCSVOIJumpFile)
            else:
                globalheader.logging.warning('%s %s', 'dataapi.jumpOIAllstocks file doesnot exists', oCSVOIJumpFile)
                if(index == 0):
                    call_error = Commonapi.generateDateList(oCSVOIJumpFile,getNumberColsData)

            call_error,iCSVFile = getStockCSVFile(contracttype,stockSymbol[index],csvDataFilePath)            
            if(call_error == globalheader.Success):
                data_frame = pd.read_csv(iCSVFile, index_col = False)
                countCols = data_frame.shape[1]
                countRows = data_frame.shape[0]
                todayrowData = countCols-1
                yestrowData = countCols-2
                
                optionSymbol =[]
                row_index = 0
                
                with open(iCSVFile, 'rU') as readFile:
                    readCSV = csv.reader(readFile)
                    fields = next(readCSV)
                    for row in readCSV:
                        optionSymbol = [str(row[0])]
                        call_error,OI = jumpinOI(row[todayrowData],row[yestrowData],thresold,money_margin,optionSymbol)
                        
                        if(call_error == globalheader.Success):
                            if(OI !=0):
                                if(OI >= Percentage_OI_Jump):
                                    if(countCols == getNumberColsData):
                                        processcolEqual(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)
                                    elif(countCols > getNumberColsData and countCols != getNumberColsData ):
                                        processcolGreater(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)                                                       
                                    else:
                                        processcolLess(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)
                                        
                        row_index += 1
                    
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.jumpOIAllstocks Ended')
                globalheader.logging.error('%s %s', 'dataapi.jumpOIAllstocks file doesnot exists', iCSVFile)
                return call_error
            
    call_error = globalheader.Success
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.jumpOIAllstocks Ended')
    return call_error



#processcolEqual(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol,data_fraem) process data csv cols equal requested col data and writes num of trading days row data of stock file to local output csv file
    #input
        #oCSVOIJumpFile- local output csv file
        #Symbol - option symbol
        #row_index - row index of local output csv file
        #getNumberColsData - num of trading days
        #contracttype - call(0)
        #data_frame - stock data frame

def processcolEqual(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol,data_frame):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processcolEqual Started')
    colFrom =0
    colTo =0
    countCols = data_frame.shape[1]
    colFrom = countCols-getNumberColsData+1
    colTo = countCols
    totalBlankColsData = getNumberColsData - countCols +1
    outPutValue = []
    rowData =[]
    pastColsDat =[]
    pastColsDat =[]
    doProcess = 1
    j =0
    i =0
    pastColsDat =data_frame.iloc[row_index,colFrom:colTo]

    ### Dd process if columns does not contain 'U'
    for j in range(0,len(pastColsDat)):
        if(pastColsDat[j] == 'U'):
            doProcess = 1
        
    if(doProcess == 1):
        optSymbol = Symbol
        addDataoFile = 1
        outPutValue =[]
        rowData = data_frame.iloc[row_index,colFrom:colTo]
        outPutValue = Commonapi.parseURowData(rowData)
        
        for item in range(0,len(outPutValue)):
            if(outPutValue[item] == 'NU'):
                addDataoFile = 0
                    
        if(addDataoFile == 1):                                            
            colItem = []
            rowItem =[]
            k = 0
            totalBlankColsData = getNumberColsData - countCols +1                                            
            for i in range(totalBlankColsData):
                value = 0
                rowItem.append(value)
            
            rowData = [(optSymbol)+(rowItem)+(outPutValue)]
            if(globalheader.debug == 1):
                globalheader.logging.debug('%s %s', 'dataapi.processcolEqual rowdata', rowdata)
            call_error = Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processcolEqual Ended')



#processcolGreater(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol,data_frame) process data csv cols greater than requested col data and writes num of trading days row data of stock file to local output csv file
    #input
        #oCSVOIJumpFile- local output csv file
        #Symbol - option symbol
        #row_index - row index of local output csv file
        #getNumberColsData - num of trading days
        #contracttype - call(0)
        #data_frame - stock data frame
#process data csv cols greater than requested col data 
def processcolGreater(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol,data_frame):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processcolGreater Started')
    colFrom =0
    colTo =0
    outPutValue = []
    rowData =[]
    pastColsDat =[]
    countCols = data_frame.shape[1]
    colFrom = countCols-getNumberColsData
    colTo = countCols                                    
    pastColsDat =data_frame.iloc[row_index,colFrom:colTo]
    doProcess = 1
     
    ### Dd process if columns does not contain 'U'
    for j in range(0,len(pastColsDat)):
        if(pastColsDat[j] == 'U'):
            doProcess = 1
            
    if(doProcess == 1):
        optSymbol = Symbol
        addDataoFile = 1
        outPutValue =[]
        fill = []
        rowFindU =[]
        rowData = data_frame.iloc[row_index,colFrom:colTo]
        
        outPutValue = Commonapi.parseURowData(rowData)           
        for item in range(0,len(outPutValue)):
            if(outPutValue[item] == 'NU'):
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            rowData = [(optSymbol)+(outPutValue)]
            if(globalheader.debug == 1):
                globalheader.logging.debug('%s %s', 'dataapi.processcolGreater rowdata', rowdata)
            call_error = Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)
            
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processcolGreater Ended')



#processcolLess(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol,,data_frame) process data csv cols less than requested col data and writes num of trading days row data of stock file to local output csv file
    #input
        #oCSVOIJumpFile- local output csv file
        #Symbol - option symbol
        #row_index - row index of local output csv file
        #getNumberColsData - num of trading days
        #contracttype - call(0)
        #,data_frame - stock csv data frame
def processcolLess(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol,data_frame):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processcolLess Started')
    colFrom =0
    colTo =0
    outPutValue = []
    rowData =[]
    pastColsDat =[]
    countCols = data_frame.shape[1]
    colFrom = countCols-(countCols -1)
    colTo = countCols
    rowsData =[]    
    doProcess = 1
    j =0
    i =0
    
    pastColsDat =data_frame.iloc[row_index,colFrom:colTo]
    
    ### Dd process if columns does not contain 'U'
    for j in range(0,len(pastColsDat)):
        if(pastColsDat[j] == 'U'):
            doProcess = 1
            
    if(doProcess == 1):
        optSymbol = Symbol
        addDataoFile = 1
        outPutValue =[]
        rowData = data_frame.iloc[row_index,colFrom:colTo]

        outPutValue = Commonapi.parseURowData(rowData)
        for item in range(0,len(outPutValue)):
            if(outPutValue[item] == 'NU'):
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            colItem = []
            rowItem =[]
            totalBlankColsData = getNumberColsData - countCols +1                                            

            for i in range(totalBlankColsData):
                value = 0
                rowItem.append(value)                                            
            
            rowData = [(optSymbol)+(rowItem)+(outPutValue)]
            if(globalheader.debug == 1):
                globalheader.logging.debug('%s %s', 'dataapi.processcolLess rowdata', rowdata)
            call_error = Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)

    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.processcolLess Ended')

#getPercentage(TodayOV,TodayOI,Diff_IN_OI_OV_Percentage_Above,thresold) generate percentage diff of today OI and today OV if greater than thresold return true or flase
    #input
        #TodayOV- col row cell data option volume
        #TodayOI - col row cell data open interest
        #thresold - min value option volume should be
        #Diff_IN_OI_OV_Percentage_Above - min percentage diff between open interest and option volume
        
    #output 
        #true(1) or false(0)
def getPercentage(TodayOV,TodayOI,Diff_IN_OI_OV_Percentage_Above,thresold):
    if((int)(TodayOV)>(int)(thresold) and (int)(TodayOI)>(int)(thresold)):
        if((int)(TodayOV)>(int)(TodayOI)):
            value = ((((int)(TodayOV) - (int)(TodayOI))/(int)(TodayOI))*100)
            if(value >= Diff_IN_OI_OV_Percentage_Above):
                if(globalheader.debug == 1):
                    globalheader.logging.debug('%s %d', 'dataapi.getPercentage value', value)
                return 1
            else:
                return 0
        return 0
    return 0


#jumpinOV(todayrowData,yestrowData,thresold,money_margin,symbol,Diff_IN_OI_OV_Percentage_Above) compares today OV with yest OV than send value if greater than thresold and return value
    #input
        #todayrowData - col row cell data option volume
        #testrowData - col row cell data option volume
        #symbol - stock symbol
        #thresold - min value option volume should be
        #money_margin - min money invested in option strike price
        #Diff_IN_OI_OV_Percentage_Above - min percentage diff between open interest and option volume
        
    #output 
        #optionInterest_error - Success or standard error
        #OV - option volume value 
def jumpinOV(todayrowData,yestrowData,thresold,money_margin,symbol,Diff_IN_OI_OV_Percentage_Above):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.jumpinOV Started')
    doProcessOV = 0
    
    call_error_TodayOI,TodayOI = parseOIdata(todayrowData,symbol)
    call_error_YestOI,YestOI = parseOIdata(yestrowData,symbol)
    call_error_TodayOP,TodayOP = parseOPdata(todayrowData,symbol)
    call_error_TodayOV,TodayOV = parseOVdata(todayrowData,symbol)
    call_error_YestOV,YestOV = parseOVdata(yestrowData,symbol)
    
    print("TodayOV,YestOV is :",TodayOV,YestOV)
    if(call_error_TodayOI ==  globalheader.Success and call_error_YestOI == globalheader.Success):
        if((int)(TodayOI) != 0 and (int)(YestOI) !=0):
            if((int)(TodayOI)>(int)(thresold)):
                if((int)(TodayOI) == (int)(YestOI)):
                  doProcessOV = 1  
                elif((int)(TodayOI)>(int)(YestOI)):
                    value = ((((int)(TodayOI) - (int)(YestOI))/(int)(YestOI))*100)
                    if(value > thresold):
                        doProcessOV = 0
                    else:
                        doProcessOV = 1
                else:
                    value = ((((int)(YestOI) - (int)(TodayOI))/(int)(TodayOI))*100)
                    if(value > thresold):
                        doProcessOV = 0
                    else:
                        doProcessOV = 1
        
    if(call_error_TodayOV == 0 and call_error_YestOV == 0):        
        if(((int)(TodayOV) == 0) and ((int)(YestOV )== 0)):
            optionvolume_error = globalheader.STOCK_OPEN_INT_ZERO
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.jumpinOV Ended')
            globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock open int Error', optionvolume_error)
            return optionvolume_error,0
        
        elif(((int)(TodayOV) == 0) and ((int)(YestOV ) != 0)):
            optionvolume_error = globalheader.STOCK_OPEN_INT_ZERO
            globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock open int Error', optionvolume_error)
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.jumpinOV Ended')
            return optionvolume_error,0
        
        elif(((int)(YestOV) ==0) and ((int)(TodayOV) !=0)):
            if((int)(TodayOV)>(int)(thresold)):
                if(doProcessOV == 1):
                    value = (((int)(TodayOV)/100)*100)
                    if(value > thresold):
                        Process = getPercentage(TodayOV,TodayOI,Diff_IN_OI_OV_Percentage_Above,thresold)
                        if(Process == 1):
                            if(call_error_TodayOP == globalheader.Success):
                                moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                                if(moneyinv > money_margin):
                                    print("(int)(TodayOI)>(int)(YestOI) is :",value)
                                    value = (round)(value)
                                    if(globalheader.info == 1):
                                        globalheader.logging.info('dataapi.jumpinOV Ended')
                                    return call_error_TodayOI,value
                                else:
                                    optionvolume_error  = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                                    globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock opt price Error', optionvolume_error)

                                    if(globalheader.info == 1):
                                        globalheader.logging.info('dataapi.jumpinOV Ended')
                                    return optionvolume_error ,0
                            else:
                                optionPrice_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
                                globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock opt vol Error', optionvolume_error)
                                if(globalheader.info == 1):
                                    globalheader.logging.info('dataapi.jumpinOV Ended')
                                return optionPrice_error,0
                        else:
                            optionPrice_error = globalheader.STOCK_OPT_VOL_OI_OV_DIFF_NOT_GREATERTHAN_PERCENTAGE_SET
                            globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock opt vol Error', optionvolume_error)

                            if(globalheader.info == 1):
                                globalheader.logging.info('dataapi.jumpinOV Ended')
                            return optionPrice_error,0
                    else:
                        optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                        globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock open int Error', optionvolume_error)
                        if(globalheader.info == 1):
                            globalheader.logging.info('dataapi.jumpinOV Ended')
                        return optionvolume_error,0
                else:
                    optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                    globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock open int Error', optionvolume_error)    
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.jumpinOV Ended')
                    return optionvolume_error,0
            else:
                optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock open int Error', optionvolume_error)
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.jumpinOV Ended')
                return optionvolume_error,0
            
        elif((int)(TodayOV)!=0 and (int)(YestOV)!=0):
            if((int)(TodayOV)>(int)(thresold) ):
                if(doProcessOV == 1):
                    if((int)(TodayOV) == (int)(YestOV)):
                        value = 0
                        optionvolume_error = globalheader.STOCK_OPEN_INT_ZERO
                        return optionvolume_error,0
                    elif((int)(TodayOV)>(int)(YestOV)):
                        value = ((((int)(TodayOV) - (int)(YestOV))/(int)(YestOV))*100)
                        if(value > thresold):
                            Process = getPercentage(TodayOV,TodayOI,Diff_IN_OI_OV_Percentage_Above,thresold)
                            if(Process == 1):
                                if(call_error_TodayOP == globalheader.Success):
                                    moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                                    if(moneyinv > money_margin):
                                        print("(int)(TodayOI)>(int)(YestOI) is :",value)
                                        value = (round)(value)
                                        if(globalheader.info == 1):
                                            globalheader.logging.info('dataapi.jumpinOV Ended')
                                        return call_error_TodayOI,value
                                    else:
                                        optionvolume_error  = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                                        globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock opt price Error', optionvolume_error)
                                        if(globalheader.info == 1):
                                            globalheader.logging.info('dataapi.jumpinOV Ended')
                                        return optionvolume_error ,0
                                else:
                                    if(globalheader.info == 1):
                                        globalheader.logging.info('dataapi.jumpinOV Ended')
                                    return call_error_TodayOP,0
                            else:
                                optionvolume_error = globalheader.STOCK_OPT_VOL_OI_OV_DIFF_NOT_GREATERTHAN_PERCENTAGE_SET
                                globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock opt vol Error', optionvolume_error)
                                if(globalheader.info == 1):
                                    globalheader.logging.info('dataapi.jumpinOV Ended')
                                return optionvolume_error,0
                        else:
                            optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                            globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock open int Error', optionvolume_error)
                            if(globalheader.info == 1):
                                globalheader.logging.info('dataapi.jumpinOV Ended')
                            return optionvolume_error,0
                    else:
                        optionvolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
                        globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock opt vol Error', optionvolume_error)
                        if(globalheader.info == 1):
                            globalheader.logging.info('dataapi.jumpinOV Ended')
                        return optionvolume_error,0
                else:
                    optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                    globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock open int Error', optionvolume_error)
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.jumpinOV Ended')
                    return optionvolume_error,0
            else:
                optionvolume_error = globalheader.STOCK_OPEN_INT_ZERO
                globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock open int Error', optionvolume_error)
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.jumpinOV Ended')
                return optionvolume_error,0
        
    else:
        optionvolume_error_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
        globalheader.logging.error('%s %d', 'dataapi.jumpinOV stock opt vol Error', optionvolume_error)

        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.jumpinOV Ended')
        return optionvolume_error_error,0 


#jumpOVAllstocks(totalStocks,stockSymbol,ofilename,thresold,Percentage_OV_Jump,money_margin,getNumberColsData,Diff_IN_OI_OV_Percentage_Above) compares today OV with yest OV than campare value if greater than thresold and
#store in local output jump OV csv file
    #input
        #totalStocks - total num of stocks
        #stockSymbol - stock symbol list
        #ofilename - local output jump OV csv file
        #todayrowData - col row cell data option volume
        #testrowData - col row cell data option volume
        #symbol - stock symbol
        #thresold - min value option volume should be
        #money_margin - min money invested in option strike price
        #Diff_IN_OI_OV_Percentage_Above - min percentage diff between open interest and option volume
        
    #output 
        #call_error - Success or standard error
           
def jumpOVAllstocks(totalStocks,stockSymbol,ofilename,thresold,Percentage_OV_Jump,money_margin,getNumberColsData,Diff_IN_OI_OV_Percentage_Above):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.jumpOVAllstocks Started')
    oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)    
    
    if os.path.exists(oCSVOIJumpFile):
        globalheader.logging.warning('%s %s', 'dataapi.jumpOVAllstocks file exists', oCSVOIJumpFile)
        os.remove(oCSVOIJumpFile)
        globalheader.logging.warning('file removed')
        
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)
            data_frame = 0
            if os.path.exists(oCSVOIJumpFile):
                globalheader.logging.warning('%s %s', 'dataapi.jumpOVAllstocks file exists', oCSVOIJumpFile)
            else:
                globalheader.logging.warning('%s %s','file doesnot exists',oCSVOIJumpFile)
                if(index == 0):
                    call_error = Commonapi.generateDateList(oCSVOIJumpFile,getNumberColsData)
            call_error,iCSVFile = getStockCSVFile(contracttype,stockSymbol[index],csvDataFilePath)
            if(call_error == globalheader.Success):
                data_frame = pd.read_csv(iCSVFile, index_col = False)
                countCols = data_frame.shape[1]
                countRows = data_frame.shape[0]
                todayrowData = countCols-1
                yestrowData = countCols-2
                
                optionSymbol =[]
                row_index = 0
                
                with open(iCSVFile, 'rU') as readFile:
                    readCSV = csv.reader(readFile)
                    fields = next(readCSV)
                    for row in readCSV:
                        optionSymbol = [str(row[0])]
                        call_error,OV = jumpinOV(row[todayrowData],row[yestrowData],thresold,money_margin,optionSymbol,Diff_IN_OI_OV_Percentage_Above)
                        
                        if(call_error == globalheader.Success):
                            if(OV !=0):
                                if(OV >= Percentage_OV_Jump):
                                    if(countCols == getNumberColsData):
                                        processcolEqual(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)
                                    elif(countCols > getNumberColsData and countCols != getNumberColsData ):
                                        processcolGreater(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)                                                       
                                    else:
                                        processcolLess(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)
                                        
                        row_index += 1
                    
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.jumpOVAllstocks Ended')
                globalheader.logging.warning('%s %s', 'dataapi.jumpOVAllstocks file does not exists', iCSVFile)
                return call_error

    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.jumpOVAllstocks Ended')        
    call_error = globalheader.Success
    return call_error

#downinOI(todayrowData,yestrowData,thresold,money_margin,symbol) compares today OI with yest OI than send value if percentage down thresold
    #input
        #todayrowData - col row cell data open interest
        #testrowData - col row cell data open interest
        #symbol - stock symbol
        #thresold - min value open interest, option volume should be
        #money_margin - min money invested in option strike price
        
    #output 
        #optionInterest_error - Success or standard error
        #OI - open interest value   
#compares OI today and yest send result if greater than percentage down thresold
def downinOI(todayrowData,yestrowData,thresold,money_margin,symbol):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.downinOI Started')
    call_error_TodayOI,TodayOI = parseOIdata(todayrowData,symbol)
    call_error_YestOI,YestOI = parseOIdata(yestrowData,symbol)
    call_error_TodayOP,TodayOP = parseOPdata(todayrowData,symbol)
  
    if(call_error_TodayOI == globalheader.Success and call_error_YestOI == globalheader.Success):        
        if((int)(TodayOI)!=0 and (int)(YestOI)!=0):
            if((int)(TodayOI)<(int)(YestOI)):   
                value = ((((float)(YestOI) - (float)(TodayOI))/(float)(TodayOI))*100)
                if(value > thresold):
                    if(call_error_TodayOP == globalheader.Success):
                        moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                        if(moneyinv  >money_margin):
                            value = (round)(value)
                            if(globalheader.info == 1):
                                globalheader.logging.info('dataapi.downinOI Ended')
                            return call_error_TodayOI,value                         
                        else:
                            optionInterest_error = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                            globalheader.logging.error('%s %d', 'dataapi.downinOI stock opt price Error', optionInterest_error)
                            if(globalheader.info == 1):
                                globalheader.logging.info('dataapi.downinOI Ended')
                            return optionInterest_error,0
                    else:
                        if(globalheader.info == 1):
                            globalheader.logging.info('dataapi.downinOI Ended')
                        return call_error_TodayOP,0
                else:
                    optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                    globalheader.logging.error('%s %d', 'dataapi.downinOI stock open int Error', optionInterest_error)
                    if(globalheader.info == 1):
                        globalheader.logging.info('dataapi.downinOI Ended')
                    return optionInterest_error,0              
            else:
                optionInterest_error = globalheader.STOCK_OPEN_INT_NO_CHANGE_IN_PERCENTAGE
                globalheader.logging.error('%s %d', 'dataapi.downinOI stock open int Error', optionInterest_error)
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.downinOI Ended')
                return optionInterest_error,0
        else:
            optionInterest_error = globalheader.STOCK_OPEN_INT_ZERO
            globalheader.logging.error('%s %d', 'dataapi.downinOI stock open int Error', optionInterest_error)
            if(globalheader.info == 1):
                globalheader.logging.info('dataapi.downinOI Ended')
            return optionInterest_error,0
       
    else:
        optionInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
        globalheader.logging.error('%s %d', 'dataapi.downinOI stock open int Error', optionInterest_error)
        if(globalheader.info == 1):
            globalheader.logging.info('dataapi.downinOI Ended')
        return optionInterest_error,0    

#downOIAllstocks(totalStocks,stockSymbol,ofilename,thresold,Percentage_OI_Jump,money_margin,getNumberColsData) compares today OI with yest OI if there is down in percentage than campare value if percentage down thresold and
#store in local output down OI csv file of all stocks
    #input
        #totalStocks - total num of stocks
        #stockSymbol - stock symbol list
        #ofilename - local output down OI csv file
        #todayrowData - col row cell data open interest
        #testrowData - col row cell data open interest
        #symbol - stock symbol
        #thresold - min value option volume should be
        #money_margin - min money invested in option strike price
        
    #output 
        #call_error - Success or standard error
def downOIAllstocks(totalStocks,stockSymbol,ofilename,getNumberColsData,Percentage_OI_Down,thresold,money_margin):
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.downOIAllstocks Started')
    oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)    
    
    if os.path.exists(oCSVOIJumpFile):
        globalheader.logging.warning('%s %s', 'dataapi.downOIAllstocks file exists', oCSVOIJumpFile)
        os.remove(oCSVOIJumpFile)
        globalheader.logging.warning('file removed')
        
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)
            data_frame = 0
            if os.path.exists(oCSVOIJumpFile):
                globalheader.logging.warning('%s %s', 'dataapi.downOIAllstocks file exists', oCSVOIJumpFile)
            else:
                globalheader.logging.warning('%s %s', 'dataapi.downOIAllstocks  file does not exists', oCSVOIJumpFile)
                if(index == 0):
                    call_error = Commonapi.generateDateList(oCSVOIJumpFile,getNumberColsData)
            call_error,iCSVFile = getStockCSVFile(contracttype,stockSymbol[index],csvDataFilePath)
            if(call_error == globalheader.Success):
                data_frame = pd.read_csv(iCSVFile, index_col = False)
                countCols = data_frame.shape[1]
                countRows = data_frame.shape[0]
                todayrowData = countCols-1
                yestrowData = countCols-2
                
                optionSymbol =[]
                row_index = 0
                
                with open(iCSVFile, 'rU') as readFile:
                    readCSV = csv.reader(readFile)
                    fields = next(readCSV)
                    for row in readCSV:
                        optionSymbol = [str(row[0])]
                        call_error,OI = downinOI(row[todayrowData],row[yestrowData],thresold,money_margin,optionSymbol)
                        
                        if(call_error == globalheader.Success):
                            if(OI !=0):
                                if(OI >= Percentage_OI_Down):
                                    if(countCols == getNumberColsData):
                                        processcolEqual(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)
                                    elif(countCols > getNumberColsData and countCols != getNumberColsData ):
                                        processcolGreater(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)                                                       
                                    else:
                                        processcolLess(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)
                                        
                        row_index += 1                    
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('dataapi.downOIAllstocks Ended')
                globalheader.logging.warning('%s %s', 'dataapi.downOIAllstocks  file does not exists', iCSVFile)
                return call_error
            
    call_error = globalheader.Success
    if(globalheader.info == 1):
        globalheader.logging.info('dataapi.downOIAllstocks Ended')
    return call_error
