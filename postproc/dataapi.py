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
OITMOI =['ITMOI','OTMOI']
OITM =['ITM','OTM']

csvDataFilePath = './../datacolls/output/'
debug = 0

#return stockCsvfile
def getStockCSVFile(index,symbol,ifilepath):
    stockCsvfilename = ifilepath + symbol+'_'+contractType[index]+'.csv'
    if os.path.exists(stockCsvfilename):
        call_error = globalheader.Success
        return call_error,stockCsvfilename
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        return call_error,stockCsvfilename

#return generated stock symbol,expdate list from stock csv file
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

#return data frame data like total cols, headerlist,symbol list ,date from an stock csv file
def getdataframedata(Symbol,exp_date,strikeprice,date,contracttype):
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
                return call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols
            else:
                return call_error,0,0,0,0,0
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE 
            return date_error,0,0,0,0,0
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return file_error,0,0,0,0,0

#return data frame data like total cols, headerlist,symbol list from an stock csv file
def getdataframeData(Symbol,exp_date,strikeprice,contracttype):
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)

    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile)
        countCols = data_frame.shape[1]
        columnList= data_frame.columns.tolist()     
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikeprice)
        if(call_error == globalheader.Success):
            return call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols
        else:
            return call_error,0,0,0,0
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return file_error,0,0,0,0

#return option interest of the stock of the particular exp date of the particular trading day of an option type
def getOIdata(Symbol,exp_date,date,contracttype,strikepricelist):
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            openinterest_list = []
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                length = len(CSVOptionSymbolList)
                while i < length:
                    if(symbol == CSVOptionSymbolList[i]):
                        #openinterest = getrowdata(i,countcols,Symbol,contracttype)
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
                                return 0,openInterest_error
                            else:
                                openinterest_list.append(openInterest['OI'])
                        else:
                            call_error, OI =Commonapi.getopenInterest(openInterest)
                            openinterest_list.append(OI)
                    i += 1
                
            return call_error,openinterest_list
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE 
            return date_error,0
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return file_error,0

#return option price of the stock of the particular exp date of the particular trading day of an option type    
def getOPdata(Symbol,exp_date,date,contracttype,strikepricelist):
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            optionPrice_list = []
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                length = len(CSVOptionSymbolList)
                while i < length:
                    if(symbol == CSVOptionSymbolList[i]):
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
                                return 0,optionPrice_error
                            else:
                                optionPrice_list.append(optionPrice['OP'])
                        else:
                            call_error, OI =Commonapi.getoptionPrice(optionPrice)
                            optionPrice_list.append(OI)
                    i += 1
            return call_error,optionPrice_list
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE 
            return date_error,0
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return file_error,0

#return option volume of the stock of the particular exp date of the particular trading day of an option type
def getOVdata(Symbol,exp_date,date,contracttype,strikepricelist):
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            optionVolume_list = []
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                length = len(CSVOptionSymbolList)
                while i < length:
                    if(symbol == CSVOptionSymbolList[i]):
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
                                return 0,optionVolume_error
                            else:
                                optionVolume_list.append(optionVolume['OV'])
                        else:
                            call_error, OV =Commonapi.getoptionVolume(optionVolume )
                            optionVolume_list.append(OV)
                    i += 1
            return call_error,optionVolume_list
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE 
            return date_error,0
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return file_error,0

#return stock volume of the stock of the particular exp date of the particular trading day of an option type
def getSVdata(Symbol,exp_date,date,contracttype,strikepricelist):
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error ==  globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            stockVolume_list = []
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                length = len(CSVOptionSymbolList)
                while i < length:
                    if(symbol == CSVOptionSymbolList[i]):
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
                                return 0,stockVolume_error
                            else:
                                stockVolume_list.append(optionPrice['OV'])
                        else:
                            call_error, SV =Commonapi.getstockVolume(stockVolume)
                            stockVolume_list.append(SV)
                    i += 1
            return call_error,stockVolume_list
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE 
            return date_error,0
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return file_error,0

#return stock price of the stock of the particular exp date of the particular trading day of an option type
def getSPdata(Symbol,exp_date,date,contracttype,strikepricelist):
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        data_frame = getdataframe(iCSVFile) 
        CSVOptionSymbolList= data_frame.Symbol.tolist()
        csvDateHeaderlist = data_frame.columns.tolist()
        if date in csvDateHeaderlist:
            countcols = csvDateHeaderlist.index(date)
            stockPrice_list = []
            for i in range(len(strikepricelist)):
                call_error,symbol = Commonapi.getSymbol(Symbol,exp_date,contracttype,strikepricelist[i])
                length = len(CSVOptionSymbolList)
                while i < length:
                    if(symbol == CSVOptionSymbolList[i]):
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
                                return 0,stockPrice_error
                            else:
                                stockPrice_list.append(optionPrice['SP'])
                        else:
                            call_error, SP =Commonapi.getstockPrice(stockPrice)
                            stockPrice_list.append(SV)
                    i += 1
                
            return call_error,stockPrice_list
            
        else:
            date_error = globalheader.DATE_DOESNOT_EXIST_IN_STOCK_CSV_DATA_FILE 
            return date_error,0
    else:
        file_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return file_error,0
    
#send data frame of csv file input
def getdataframe(iCSVfile):    
    data_frame = pd.read_csv(iCSVfile, index_col = False)
    return data_frame



#return all expdates from stock csv file
def getExpDatesListFromCSV(iCSVFile):    
    
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
    return finalOptionExpDateList

#return all strikeprices of an exp date from stock csv file
def strikePricesFromCSV(expdate,iCSVFile):
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
#    print("strikepriceList = sorted(strikepriceList) is ..................:",strikepriceList)
    return strikepriceList


#return parsed rowdata of the particular cell
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
                OI = 0
            else:
                openInterest_error = globalheader.Success
                OI = openInterest['OI']
        else:
            call_error, OI =Commonapi.getopenInterest(openInterest)            
    return openInterest_error,OI

#return parsed rowdata of the particular cell
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
                OI = 0
            else:
                openInterest_error = globalheader.Success
                OI = openInterest['OI']

        else:
            openInterest_error, OI =Commonapi.getopenInterest(rowData)            
    return openInterest_error,OI


#return parsed rowdata of the particular cell
def parseInputRowDatas(colFrom,row,Symbol,contracttype,data_frame):
    rowData = []
    #rowData = getrowdata(row,colFrom,Symbol,contracttype)
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

#return row data of the cell        
def getrowdata(i,countcols,Symbol,contracttype):
    call_error,iCSVFile = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    data_frame = getdataframe(iCSVFile)
    oirowdata = data_frame.iloc[i,countcols]
    return oirowdata

#return data frame of stock csv file
def getDataFrame(ifile):    
    data_frame = pd.read_csv(ifile, index_col = False)
    countRows = data_frame.shape[0]
    countCols = data_frame.shape[1]
    columnList= data_frame.columns.tolist()
    colFrom = countCols-1      
    CSVOptionSymbolList= data_frame.Symbol.tolist()
    
    return columnList,colFrom,CSVOptionSymbolList


#process data csv cols equal than requested col data 
def processColEqual(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol):
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
                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optSymbol)
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
            print(" rowData is :",rowData)
            Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)

#process data csv cols greater than requested col data 
def processColGreater(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol):
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
                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optSymbol)
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            rowData = [(optSymbol)+(outPutValue)]
            print(" rowData is :",rowData)
            Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)

#process data csv cols less than requested col data            
def processColLess(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol):
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
                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optSymbol)
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            colItem = []
            rowItem =[]
            totalBlankColsData = getNumberColsData - countCols +1                                            

            for i in range(totalBlankColsData):
                value = 0
                rowItem.append(value)                                            
            
            rowData = [(optSymbol)+(rowItem)+(outPutValue)]
            print(" rowData is :",rowData)
            Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)


# return getStrikePriceMaxPain
def getStrikePriceMaxPain(strikepriceList,stockprice,strikePriceFromCSV,row,OptionExpDate,colFrom,contracttype,max_pain,symbol,exp_date,data_frame):
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
    return (round)(max_pain)

def getMaxPain(Symbol,exp_date,contracttype):
    maxpain_dict = OrderedDict()
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
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

            return call_error,maxpain_dict       
        else:
            call_error = globalheader.STOCK_OPT_EXPDATE_DOES_NOT_EXIST
            return call_error,0
            
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        return call_error,0

def getAllMaxPain(Symbol,contracttype):
    #maxpain_dict = defaultdict(lambda : defaultdict(OrderedDict))
    maxpain_dict = defaultdict(lambda : OrderedDict())
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if(call_error == globalheader.Success):
        print("File Exists")
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

        return call_error,maxpain_dict       
        
            
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        return call_error,0


def getStrikePriceMoneyInv(strikepriceList,stockprice,strikePriceFromCSV,row,OptionExpDate,colFrom,contracttype,money_inv,symbol,data_frame):
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

    return (round)(money_inv)

    
def getmoneyInv(Symbol,exp_date,contracttype):
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
            return call_error,moneyinv_dict       
        else:
            call_error = globalheader.STOCK_OPT_EXPDATE_DOES_NOT_EXIST
            return call_error,0
            
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        return call_error,0


def getAllmoneyInv(Symbol,contracttype):
#    moneyinv_dict = defaultdict(lambda : defaultdict(OrderedDict))
    moneyinv_dict = defaultdict(lambda : OrderedDict())
    finalOptionExpDateList =[]    
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    #Loop around num of expiration x contracttype x getNumberColsData x strikeprices
    if(call_error == globalheader.Success):
        print("File Exists")
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
        return call_error,moneyinv_dict       

    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
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


def getStrikePriceMoneyInvExpDateAllData(strikepriceList,stockprice,strikePriceFromCSV,row,OptionExpDate,colFrom,contracttype,money_inv,symbol,data_frame,OTM,OTMOI):
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

    return (round)(money_inv),OTM,OTMOI

def getmoneyInvExpDateAllData(Symbol,exp_date,contracttype):
    moneyinv_dict = OrderedDict()
    OTM_dict =OrderedDict()
    OTMOI_dict = OrderedDict()
    TM_dict = OrderedDict()
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
                
            return call_error,moneyinv_dict,OTM_dict,OTMOI_dict,TM_dict      
        else:
            call_error = globalheader.STOCK_OPT_EXPDATE_DOES_NOT_EXIST
            return call_error,0,0,0,0
            
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        return call_error,0,0,0,0

def getmoneyInvAllExpDateAllData(Symbol,contracttype):
    moneyinv_dict = defaultdict(lambda : OrderedDict())
    OTM_dict = defaultdict(lambda : OrderedDict())
    OTMOI_dict = defaultdict(lambda : OrderedDict())
    TM_dict = defaultdict(lambda : OrderedDict())
    finalOptionExpDateList =[]
    
    call_error,istockCSVfilename = getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    #Loop around num of expiration x contracttype x getNumberColsData x strikeprices
    if(call_error == globalheader.Success):
        print("File Exists")
        data_frame = getdataframe(istockCSVfilename)
        finalOptionExpDateList = getExpDatesListFromCSV(istockCSVfilename)
        print("finalOptionExpDateList = getExpDatesListFromCSV(istockCSVfilename) is :",finalOptionExpDateList)
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
                
        return call_error,moneyinv_dict,OTM_dict,OTMOI_dict,TM_dict      
            
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST
        return call_error,0,0,0,0

def parseOIdata(openinterest,symbol):
    OI_dict = dict()
    openInterest = str(openinterest).split(':')
    if Commonapi.listOfStr[0] in openInterest:
        openInterest = Commonapi.ConvertLst_Dict(openInterest)
        OI = openInterest['OI']
        OI = str(OI)
        OI = OI.split(',')
        openInterest['OI'] = OI[0]
        if(openInterest['OI'] == 'U' or openInterest['OI'] == '' or openInterest['OI'] == ',' or openInterest['OI'] == "'" or openInterest['OI'] == ''):
            openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
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
           return openInterest_error, OI

def parseOPdata(optionprice,symbol):
    OP_dict = dict()
    optionPrice = str(optionprice).split(Commonapi.data_seperator)
    if Commonapi.listOfStr[3] in optionPrice:
        optionPrice = Commonapi.ConvertLst_Dict(optionPrice)
        OP = optionPrice['OP']
        OP = str(OP)
        OP = OP.split(',')
        optionPrice['OP'] = OP[0]
        if(optionPrice['OP'] == 'U' or optionPrice['OP'] == '.' or optionPrice['OP'] == ',' or optionPrice['OP'] == "'"):
            optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
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
           return optionPrice_error, OP

def parseOVdata(optionvolume,symbol):
    optionVolume = str(optionvolume).split(Commonapi.data_seperator)
    if Commonapi.listOfStr[4] in optionVolume:
        optionVolume = Commonapi.ConvertLst_Dict(optionVolume)
        OV = optionVolume['OV']
        OV = str(OV)
        OV = OV.split(',')
        optionVolume['OV'] = OV[0]
        if(optionVolume['OV'] == 'U' or optionVolume['OV'] == ',' or optionVolume['OV'] == '.' or optionVolume['OV'] == "'"):
            optionVolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
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
           return optionVolume_error, OV
        
def jumpinOI(todayrowData,yestrowData,thresold,money_margin,symbol):

    call_error_TodayOI,TodayOI = parseOIdata(todayrowData,symbol)
    call_error_YestOI,YestOI = parseOIdata(yestrowData,symbol)
    call_error_TodayOP,TodayOP = parseOPdata(todayrowData,symbol)

    print("TodayOI,YestOI is :",TodayOI,YestOI)
  
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
                            return call_error_TodayOI,value
                        else:
                            optionInterest_error = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                            return optionInterest_error,value
                    else:
                        optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
                        return optionPrice_error,0  
                else:
                    optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                    return optionInterest_error,0
            else:
                optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
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
                                return call_error_TodayOI,value
                            else:
                                optionInterest_error = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                                return optionInterest_error,0
                        else:
                            return call_error_TodayOP,0
                    else:
                        optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                        return optionInterest_error,0
 
                else:
                    optionInterest_error = globalheader.STOCK_OPEN_INT_NO_CHANGE_IN_PERCENTAGE
                    return optionInterest_error,0 
            else:
                optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                return optionInterest_error,0
        else:
            optionInterest_error = globalheader.STOCK_OPEN_INT_ZERO
            return optionInterest_error,0 

    else:
        optionInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
        return optionInterest_error,0 
    
    

def jumpOIAllstocks(totalStocks,stockSymbol,ofilename,thresold,Percentage_OI_Jump,money_margin,getNumberColsData):
    oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)    
    
    if os.path.exists(oCSVOIJumpFile):
        print("file exists:",oCSVOIJumpFile)
        os.remove(oCSVOIJumpFile)
        print("file removed")
        
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)
            data_frame = 0
            if os.path.exists(oCSVOIJumpFile):
                print("file exists:",oCSVOIJumpFile)
            else:
                print("file doesnot exists:",oCSVOIJumpFile)
                if(index == 0):
                    dateList = Commonapi.generateDateList(oCSVOIJumpFile,getNumberColsData)
            call_error,iCSVFile = getStockCSVFile(contracttype,stockSymbol[index],csvDataFilePath)
            if(call_error == globalheader.Success):
                
                print("File Exists:",iCSVFile)
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
                                    print("oi is :",OI,row_index)
                                    if(countCols == getNumberColsData):
                                        processcolEqual(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)
                                    elif(countCols > getNumberColsData and countCols != getNumberColsData ):
                                        processcolGreater(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)                                                       
                                    else:
                                        processcolLess(oCSVOIJumpFile,optionSymbol,row_index,getNumberColsData,contracttype,stockSymbol[index],data_frame)
                                        
                        row_index += 1
                    
            else:
                print("File Does not Exists:",iCSVFile)
                return call_error
            
    call_error = globalheader.Success
    return call_error
        
#process data csv cols equal than requested col data 
def processcolEqual(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol,data_frame):
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
                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optSymbol)
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
            print(" rowData is :",rowData)
            Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)

#process data csv cols greater than requested col data 
def processcolGreater(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol,data_frame):
    print("processcolGreater Symbol,row_index is:",Symbol,row_index)
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
                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optSymbol)
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            rowData = [(optSymbol)+(outPutValue)]
            print(" rowData is :",rowData)
            Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)

#process data csv cols less than requested col data            
def processcolLess(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol,data_frame):
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
                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optSymbol)
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            colItem = []
            rowItem =[]
            totalBlankColsData = getNumberColsData - countCols +1                                            

            for i in range(totalBlankColsData):
                value = 0
                rowItem.append(value)                                            
            
            rowData = [(optSymbol)+(rowItem)+(outPutValue)]
            print(" rowData is :",rowData)
            Commonapi.writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)


# process the diff between Today OI and Today OV
def getPercentage(TodayOV,TodayOI,Diff_IN_OI_OV_Percentage_Above,thresold):
    if((int)(TodayOV)>(int)(thresold) and (int)(TodayOI)>(int)(thresold)):
        if((int)(TodayOV)>(int)(TodayOI)):
            value = ((((int)(TodayOV) - (int)(TodayOI))/(int)(TodayOI))*100)
            if(value >= Diff_IN_OI_OV_Percentage_Above):
                print("getDiff(TodayOV,TodayOI) :",value)
                return 1
            else:
                return 0
        return 0
    return 0

#calculate the jump in today OV and yest OV and return value
def jumpinOV(todayrowData,yestrowData,thresold,money_margin,symbol,Diff_IN_OI_OV_Percentage_Above):
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
            return optionvolume_error,0
        
        elif(((int)(TodayOV) == 0) and ((int)(YestOV ) != 0)):
            optionvolume_error = globalheader.STOCK_OPEN_INT_ZERO            
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
                                    return call_error_TodayOI,value
                                else:
                                    optionvolume_error  = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                                    return optionvolume_error ,0
                            else:
                                optionPrice_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
                                return optionPrice_error,0
                        else:
                            optionPrice_error = globalheader.STOCK_OPT_VOL_OI_OV_DIFF_NOT_GREATERTHAN_PERCENTAGE_SET
                            return optionPrice_error,0
                    else:
                        optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                        return optionvolume_error,0
                else:
                    optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                    return optionvolume_error,0
            else:
                optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
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
                                        return call_error_TodayOI,value
                                    else:
                                        optionvolume_error  = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                                        return optionvolume_error ,0
                                else:
                                    return call_error_TodayOP,0
                            else:
                                optionvolume_error = globalheader.STOCK_OPT_VOL_OI_OV_DIFF_NOT_GREATERTHAN_PERCENTAGE_SET
                                return optionvolume_error,0
                        else:
                            optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                            return optionvolume_error,0
                    else:
                        optionvolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
                        return optionvolume_error,0
                else:
                    optionvolume_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                    return optionvolume_error,0
            else:
                optionvolume_error = globalheader.STOCK_OPEN_INT_ZERO
                return optionvolume_error,0
        
    else:
        optionvolume_error_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
        return optionvolume_error_error,0 
    
# calculates Jump in otion volume of all stocks from stocklist
def jumpOVAllstocks(totalStocks,stockSymbol,ofilename,thresold,Percentage_OV_Jump,money_margin,getNumberColsData,Diff_IN_OI_OV_Percentage_Above):
    
    oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)    
    
    if os.path.exists(oCSVOIJumpFile):
        print("file exists:",oCSVOIJumpFile)
        os.remove(oCSVOIJumpFile)
        print("file removed")
        
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)
            data_frame = 0
            if os.path.exists(oCSVOIJumpFile):
                print("file exists:",oCSVOIJumpFile)
            else:
                print("file doesnot exists:",oCSVOIJumpFile)
                if(index == 0):
                    dateList = Commonapi.generateDateList(oCSVOIJumpFile,getNumberColsData)
            call_error,iCSVFile = getStockCSVFile(contracttype,stockSymbol[index],csvDataFilePath)
            if(call_error == globalheader.Success):
                
                print("File Exists:",iCSVFile)
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
                print("File Does not Exists:",iCSVFile)
                return call_error
            
    call_error = globalheader.Success
    return call_error

#compares OI today and yest send result if greater than percentage down thresold
def downinOI(todayrowData,yestrowData,thresold,money_margin,symbol):
    
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
                            return call_error_TodayOI,value                         
                        else:
                            optionInterest_error = globalheader.STOCK_OPT_PRICE_LESSTHAN_MARGIN_VALVE_SET
                            return optionInterest_error,0
                    else:
                        return call_error_TodayOP,0
                else:
                    optionInterest_error = globalheader.STOCK_OPEN_INT_NOT_GREATERTHAN_THRESOLD_SET
                    return optionInterest_error,0              
            else:
                optionInterest_error = globalheader.STOCK_OPEN_INT_NO_CHANGE_IN_PERCENTAGE 
                return optionInterest_error,0
        else:
            optionInterest_error = globalheader.STOCK_OPEN_INT_ZERO 
            return optionInterest_error,0
       
    else:
        optionInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE 
        return optionInterest_error,0    


def downOIAllstocks(totalStocks,stockSymbol,ofilename,getNumberColsData,Percentage_OI_Down,thresold,money_margin):
    oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)    
    
    if os.path.exists(oCSVOIJumpFile):
        print("file exists:",oCSVOIJumpFile)
        os.remove(oCSVOIJumpFile)
        print("file removed")
        
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)
            data_frame = 0
            if os.path.exists(oCSVOIJumpFile):
                print("file exists:",oCSVOIJumpFile)
            else:
                print("file doesnot exists:",oCSVOIJumpFile)
                if(index == 0):
                    dateList = Commonapi.generateDateList(oCSVOIJumpFile,getNumberColsData)
            call_error,iCSVFile = getStockCSVFile(contracttype,stockSymbol[index],csvDataFilePath)
            if(call_error == globalheader.Success):
                
                print("File Exists:",iCSVFile)
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
                print("File Does not Exists:",iCSVFile)
                return call_error
            
    call_error = globalheader.Success
    return call_error
