### commonapi contains common function which use other
### py files

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

import sys
csv.field_size_limit(sys.maxsize)
contractType =['CALL','PUT']
debug = 0

#return stockCsvfile
def getStockCSVFiles(index,symbol,ifilepath):       
    stockCsvfilename = ifilepath + symbol+'_'+contractType[index]+'.csv'
    return stockCsvfilename

#return output stockCsvfile
def createoFile(symbol,ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+symbol+'_'+today+'.xlsx'
    return stockCsvfilename

#return extracted Expdate from row data
def getOptExpDateFromCSV(optionSymbol):
    symbol,date = optionSymbol.split('_')
    date = list(str(date))
    length = len(date)
    expdate = '20'+date[4]+date[5]+date[0]+date[1]+date[2]+date[3]
    return expdate

#return removed duplicates item from list
def removeDuplicateItems(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list

#return extracted strikeprice from row data
def getOptionStrikePrice(optionSymbol):
    n = 7
    symbol,strikeprice = optionSymbol.split('_')
    strikeprice  = list(str(strikeprice ))
    length = len(strikeprice )
    strikeprice= strikeprice[n:]
    strikeprice =''.join(strikeprice)
    return strikeprice

#return data_frame of input stock csv file
def getDataFrame(ifile,getNumberColsData):
    data_frame = pd.read_csv(ifile, index_col = False)
    countRows = data_frame.shape[0]
    countCols = data_frame.shape[1]
    columnList= data_frame.columns.tolist()
    colFrom = countCols-getNumberColsData      
    CSVOptionSymbolList= data_frame.Symbol.tolist()
    
    return data_frame,columnList,colFrom,CSVOptionSymbolList

#return all expdates from stock csv file
def getExpDatesListFromCSV(data_frame,num_expiration):    
    expDateList =[]
    finalOptionExpDateList = []
    
    CSVOptionSymbolList= data_frame.Symbol.tolist()
    if(debug == 1):
        print("CSVOptionSymbolList  and length is  :",CSVOptionSymbolList,len(CSVOptionSymbolList))
        
    for index in range(0,len(CSVOptionSymbolList)):
        expdatelist = getOptExpDateFromCSV(CSVOptionSymbolList[index])
        expDateList.append(expdatelist)                
    
    expDateList = removeDuplicateItems(expDateList)
    expDateList= sorted(expDateList)

    for i in range(0,(int)(num_expiration)):
        finalOptionExpDateList.append(expDateList[i])
    return finalOptionExpDateList

#return all strikeprices from stock csv file
def strikePricesFromCSV(finalOptionExpDateList,data_frame):
    strikepriceList =[]    
    CSVOptionSymbolList= data_frame.Symbol.tolist()

    strikepricelist =[]
    for index in range(0,len(CSVOptionSymbolList)):                                    
        symbolexpdate1 = getOptExpDateFromCSV(CSVOptionSymbolList[index])
        if(symbolexpdate1 == finalOptionExpDateList):
            strikeprice = getOptionStrikePrice(CSVOptionSymbolList[index])
            strikepricelist.append(strikeprice)
    
    strikepricelist = removeDuplicateItems(strikepricelist)
    strikepriceList = sorted(strikepricelist)
    strikepriceList.sort(key=float)
    print("strikepriceList = sorted(strikepriceList) is ..................:",strikepriceList)
    return strikepriceList

#return input stock csv file
def getInputFile(ifilename):       
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ifilename+'_'+today+'.csv'
    return stockCsvfilename

#return input stock csv file
def getInputfile(ifilename):       
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ifilename
    return stockCsvfilename
        
def extract(string, start=':'):
        return string[string.index(start)+1]

###return outout OI jump csv file    
##def createOIJumpFile(ofilename):
##    today = datetime.date.today()
##    today= datetime.datetime.strftime((today), '%m_%d_%Y')
##    stockCsvfilename = ofilename+'_'+today+'.csv'
##    return stockCsvfilename

#return outout xl file 
def createoxlFile(ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+today+'.xlsx'
    return stockCsvfilename

#return outout OI jump csv file
def createOutputOIJumpFile(ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+today+'.csv'
    return stockCsvfilename

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

#return generated datelist for jumpoi output csv file
def generateDateList(ofile,getNumberColsData):
    today = date.today()
    dateListHeader = []
    header_list =[]
    prev_days = [today - timedelta(days=i) for i in range(getNumberColsData*2)]
    print("prev_days is :",prev_days)
    prev_days = [d for d in prev_days if d.weekday() < 5]       
    for dateItems in prev_days[:getNumberColsData]:                                     
        print("dateItems :",dateItems)
        dates = datetime.datetime.strftime((dateItems), '%Y%m%d')
        dateListHeader.append(dates)
        print("dates:",dates)
    dateListHeader = sorted(dateListHeader)    
    header_list = ['Symbol']+dateListHeader
    header_list = [header_list]
    print("len of header_list is :",len(header_list))    
    print("header_list is :",header_list)
    
    with open(ofile, 'w') as myfile:
        writer = csv.writer(myfile)
        for row in header_list:
            writer.writerow(row)

#return parsed option price from row data
def getDataOP(todayOP,yestOP):
    todayOP = todayOP.replace("[",'')
    todayOP= todayOP.replace("]",'')
    TodayOP  = str(todayOP).split(":")
    TodayOPRef = TodayOP

    yestOP = yestOP.replace("[",'')
    yestOP = yestOP.replace("]",'')
    YestOP  = str(yestOP).split(":")
    YestOPRef = YestOP

    if(len(TodayOPRef) == 0 or len(YestOPRef) == 0): 
        if((TodayOP[0] == '' or TodayOP[0] == 'U' or TodayOP[0] == '.') or (YestOP[0] == '' or YestOP[0] == 'U' or YestOP[0] == '.')):            
            TodayOP[0] = (int)(0)
            YestOP[0] = (int)(0)
            return 0,0
        else:
            TodayOP[0] =(int)(0)
            YestOP[0] = (int)(0)
            return TodayOP[0],YestOP[0]

    if(len(TodayOPRef) == 1 or len(YestOPRef) == 1): 
        if((TodayOP[0] == '' or TodayOP[0] == 'U' or TodayOP[0] == '.') or (YestOP[0] == '' or YestOP[0] == 'U' or YestOP[0] == '.')):            
            TodayOP[0] = (int)(0)
            YestOP[0] = (int)(0)
            return 0,0
        else:
            TodayOP[0] =(int)(0)
            YestOP[0] = (int)(0)
            return TodayOP[0],YestOP[0]

    if(len(TodayOPRef) > 1 or len(YestOPRef) > 1):
        if((TodayOP[3] == '' or TodayOP[3] == 'U' or TodayOP[3] == '.') or (YestOP[3] == '' or YestOP[3] == 'U' or YestOP[3] == '.')):
            TodayOP[3] =(int)(0)
            YestOP[3] = (int)(0)
            
        if((TodayOP[3] == 0) or (YestOP[3] == 0)):
            return 0,0
        else:
            return TodayOP[3],YestOP[3]
    
#return parsed option interest from row data
def getDataOI(todayOI,yestOI):    
    todayOI = todayOI.replace("[",'')
    todayOI = todayOI.replace("]",'')
    TodayOI  = str(todayOI).split(":")
    TodayOIRef = TodayOI

    yestOI = yestOI.replace("[",'')
    yestOI = yestOI.replace("]",'')
    YestOI  = str(yestOI).split(":")
    YestOIRef = YestOI

    if(len(TodayOIRef) == 0 or len(YestOIRef) == 0): 
        if((TodayOI[0] == '' or TodayOI[0] == 'U' or TodayOI[0] == '.') or (YestOI[0] == '' or YestOI[0] == 'U' or YestOI[0] == '.')):            
            TodayOI[0] = (int)(0)
            YestOI[0] = (int)(0)
            return 0,0
        else:
            TodayOI[0] =(int)(0)
            YestOI[0] = (int)(0)
            return TodayOI[0],YestOI[0]

    if(len(TodayOIRef) == 1 or len(YestOIRef) == 1): 
        if((TodayOI[0] == '' or TodayOI[0] == 'U' or TodayOI[0] == '.') or (YestOI[0] == '' or YestOI[0] == 'U' or YestOI[0] == '.')):            
            TodayOI[0] = (int)(0)
            YestOI[0] = (int)(0)
            return 0,0
        else:
            TodayOI[0] =(int)(0)
            YestOI[0] = (int)(0)
            return TodayOI[0],YestOI[0]

    if(len(TodayOIRef) > 1 or len(YestOIRef) > 1):  
        if((TodayOI[0] == '' or TodayOI[0] == 'U' or TodayOI[0] == '.') or (YestOI[0] == '' or YestOI[0] == 'U' or YestOI[0] == '.')):
            TodayOI[0] =(int)(0)
            YestOI[0] = (int)(0)
            
        if((TodayOI[0] == 0) or (YestOI[0] == 0)):
            return 0,0
        else:
            return TodayOI[0],YestOI[0]

#return parsed option volume from row data
def getDataOV(todayOV,yestOV):
    todayOV = todayOV.replace("[",'')
    todayOV = todayOV.replace("]",'')
    TodayOV  = str(todayOV).split(":")
    TodayOVRef = TodayOV

    yestOV = yestOV.replace("[",'')
    yestOV = yestOV.replace("]",'')
    YestOV  = str(yestOV).split(":")
    YestOVRef = YestOV

    if(len(TodayOVRef) == 0 or len(YestOVRef) == 0): 
        if((TodayOV[0] == '' or TodayOV[0] == 'U' or TodayOV[0] == '.') or (YestOV[0] == '' or YestOV[0] == 'U' or YestOV[0] == '.')):            
            TodayOV[0] = (int)(0)
            YestOV[0] = (int)(0)
            return 0,0
        else:
            TodayOV[0] =(int)(0)
            YestOV[0] = (int)(0)
            return TodayOV[0],YestOV[0]

    if(len(TodayOVRef) == 1 or len(YestOVRef) == 1): 
        if((TodayOV[0] == '' or TodayOV[0] == 'U' or TodayOV[0] == '.') or (YestOV[0] == '' or YestOV[0] == 'U' or YestOV[0] == '.')):            
            TodayOV[0] = (int)(0)
            YestOV[0] = (int)(0)
            return 0,0
        else:
            TodayOV[0] =(int)(0)
            YestOV[0] = (int)(0)
            return TodayOV[0],YestOV[0]

    if(len(TodayOVRef) > 1 or len(YestOVRef) > 1):  
        if((TodayOV[4] == '' or TodayOV[4] == 'U' or TodayOV[4] == '.') or (YestOV[4] == '' or YestOV[4] == 'U' or YestOV[4] == '.')):
            TodayOV[4] =(int)(0)
            YestOV[4] = (int)(0)
            
        if((TodayOV[4] == 0) or (YestOV[4] == 0)):
            return 0,0
        else:
            return TodayOV[4],YestOV[4]

#write row datas to jumpOI/jumpOV output csv file        
def writeOIrOVtolocalCSV(ofile,rowData):
    if os.path.exists(ofile):
        with open(ofile, 'a') as ocsvfile:
            wr = csv.writer(ocsvfile,lineterminator='\r')
            for row in rowData:
                wr.writerow(row)
    else:
        with open(ofile, 'w') as ocsvfile:
            writer = csv.writer(ocsvfile)
            writer.writerow(['Symbol','YestOI','TodayOI','%Jump'])

#parse the row data
def parseURowData(rowData):
    outPutValue = []
    for item in range(0,len(rowData)):
        rowData[item] = rowData[item].replace('[','')
        rowFindU  = str(rowData[item]).split(":")
        result = str(rowFindU).find('U')
        if(result == -1):
            outPutValue.append(rowData[item])
        else:
            rowData[item] = 0
            outPutValue.append(rowData[item])

    return outPutValue

#process data csv cols equal than requested col data 
def processColEqual(oCSVOIJumpFile,data_frame,optionSymbol,row_index,getNumberColsData):

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
        optSymbol = optionSymbol
        addDataoFile = 1
        outPutValue =[]
        rowData = data_frame.iloc[row_index,colFrom:colTo]
        outPutValue = parseURowData(rowData)
        
        for item in range(0,len(outPutValue)):
            if(outPutValue[item] == 'NU'):
                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optionSymbol)
                addDataoFile = 0
                    
        if(addDataoFile == 1):                                            
            colItem = []
            rowItem =[]
            k = 0
            totalBlankColsData = getNumberColsData - countCols +1                                            
            for i in range(totalBlankColsData):
                value = 0
                rowItem.append(value)
            
            rowData = [(optionSymbol)+(rowItem)+(outPutValue)]
            writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)

#process data csv cols greater than requested col data 
def processColGreater(oCSVOIJumpFile,data_frame,optionSymbol,row_index,getNumberColsData):
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
        optSymbol = optionSymbol
        addDataoFile = 1
        outPutValue =[]
        fill = []
        rowFindU =[]
        rowData = data_frame.iloc[row_index,colFrom:colTo]
        print("rowData in cols >getnumcols is and optionSymbol :",rowData,optSymbol)
        
        outPutValue = parseURowData(rowData)           
        print("outPutValue.............. is :",outPutValue)
        for item in range(0,len(outPutValue)):
            if(outPutValue[item] == 'NU'):
                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optionSymbol)
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            print(" rowData is :",rowData)
            rowData = [(optionSymbol)+(outPutValue)]
            writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)

#process data csv cols less than requested col data            
def processColLess(oCSVOIJumpFile,data_frame,optionSymbol,row_index,getNumberColsData):
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
        optSymbol = optionSymbol
        addDataoFile = 1
        outPutValue =[]
        rowData = data_frame.iloc[row_index,colFrom:colTo]
        print("rowData in cols <getnumcols is and optionSymbol :",rowData,optSymbol)

        outPutValue = parseURowData(rowData)
        for item in range(0,len(outPutValue)):
            if(outPutValue[item] == 'NU'):
                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optionSymbol)
                addDataoFile = 0
                    
        if(addDataoFile == 1):
            colItem = []
            rowItem =[]
            totalBlankColsData = getNumberColsData - countCols +1                                            

            for i in range(totalBlankColsData):
                value = 0
                rowItem.append(value)                                            
            
            rowData = [(optionSymbol)+(rowItem)+(outPutValue)]            
            print(" rowDatas outPutValue.............. is :",rowData)
            writeOIrOVtolocalCSV(oCSVOIJumpFile,rowData)

