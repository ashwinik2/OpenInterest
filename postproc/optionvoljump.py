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

stockSymbol = []
stockExpDate = []
stockStrikeprice = []
todayDate = []
stockSymbolList  = [] 
stockExpDatesList  = []  

global totalStocks
global csvSymbolList
global stockprice
global loadopenInterest  

thresold = 50
OIthresold = 50
getNumberColsData = 20
CHART_HEADER_COUNT = 5
Percentage_Above = 400
Diff_Percentage_Above = 200

contractType =['CALL','PUT']   
date_format = '%m/%d/%Y'

ifilepath = './../datacolls/output/'
ifilestocklist = './../datacolls/input/'+'StockList.csv'

ofilepath = './output/'
ofilename = ofilepath+'OVPerJump_400'

def generateTotalStockList():
    global totalStocks
    with open(ifilestocklist) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        fields = next(readCSV)
        for row in readCSV:
            stocksymbol = row[0]
            stockexpdate = row[1]

            stockSymbol.append(stocksymbol)
            stockExpDate.append(stockexpdate)
            
        print(stockSymbol)
        print(stockExpDate)
        totalStocks = len(stockSymbol)
        print("Number of Stocks in OptionChainList is  : % 2d" %(totalStocks))


def getStockCSVFiles(index,stockIndex):       
    stockCsvfilename = ifilepath+stockSymbol[stockIndex]+'_'+contractType[index]+'.csv'
    return stockCsvfilename

def createOutputOIJumpFile():
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+today+'.csv'
    return stockCsvfilename

def getDataOI(dataOI):
    dataOI = dataOI.replace("[",'')
    dataOI = dataOI.replace("]",'')
    DataOI  = str(dataOI).split(":")

    DataOIRef = DataOI
    #DataOIRef=[DataOIRef]
#    print("DataOIRef is :",DataOIRef)
#    print("DataOIRef is :",len(DataOIRef))
    if(len(DataOIRef) == 0): 
        if(DataOI[0] == ''):
            DataOI[0] =(int)(0)
            
        else:
            DataOI[0] =(int)(0)
    
    if(DataOI[0] == '' or DataOI[0] == 'U'):
        DataOI[0] =(int)(0) 
            
    if(((DataOI[0]) == 0)):
        return 0

    elif((DataOI[0]) == 'U'):
        return 0
    else:
        return DataOI[0]

def getDataOV(dataOV):
    dataOV = dataOV.replace("[",'')
    dataOV = dataOV.replace("]",'')
    DataOV  = str(dataOV).split(":")
#    print("DataOV is :",DataOV)
    DataOVRef = DataOV

    if(len(DataOVRef) == 0): 
        if(DataOV[0] == ''):            
            DataOV[0] = (int)(0)
            return 0
        else:
            DataOV[0] =(int)(0)
            return 0

    if(len(DataOVRef) == 1): 
        if(DataOV[0] == '' or 'U'):            
            DataOV[0] = (int)(0)
            return 0
        else:
            DataOV[0] =(int)(0)
            return 0

    if(len(DataOVRef) > 1):  
        if(DataOV[4] == '' or DataOV[4] == 'U'):
            DataOV[4] =(int)(0) 
            
        if(((DataOV[4]) == 0)):
            return 0
        else:
#            print("DataOV[4]:",DataOV[4])
            return DataOV[4]

def getDiff(TodayOV,TodayOI):
    if((int)(TodayOV)>(int)(OIthresold) and (int)(TodayOI)>(int)(OIthresold)):
        if((int)(TodayOV)>(int)(TodayOI)):
            value = ((((int)(TodayOV) - (int)(TodayOI))/(int)(TodayOI))*100)
            if(value > Diff_Percentage_Above):
                print("getDiff(TodayOV,TodayOI) :",value)
                return 1
            else:
                return 0
        return 0
    return 0

def jumpinOV(todayOI,yestOI):
    global thresold
    
    doProcessOV = 0
    TodayOI = getDataOI(todayOI)
    YestOI = getDataOI(yestOI)
#    print("todayOI,yestOI is :",todayOI,yestOI)
    if((int)(TodayOI) != 0 and (int)(YestOI) !=0):
        if((int)(TodayOI)>(int)(OIthresold) and (int)(YestOI)>(int)(OIthresold)):
            if((int)(TodayOI) == (int)(YestOI)):
              doProcessOV = 1  
            elif((int)(TodayOI)>(int)(YestOI)):
                value = ((((int)(TodayOI) - (int)(YestOI))/(int)(YestOI))*100)
                if(value > OIthresold):
#                    print("value is value2 !=0 and value1 !=0 is :",value)
                    doProcessOV = 0
                else:
#                    print("value is value2 !=0 and value1 !=0 is else:",value)
                    doProcessOV = 1
            elif((int)(TodayOI)<(int)(YestOI)):
                #value = ((((int)(TodayOI) - (int)(YestOI))/(int)(YestOI))*100)
                value = ((((int)(YestOI) - (int)(TodayOI))/(int)(TodayOI))*100)
                if(value > OIthresold):
#                    print("(int)(TodayOI)<(int)(YestOI)value > is :",value)
                    doProcessOV = 0
                else:
#                    print("(int)(TodayOI)<(int)(YestOI)value < is :",value)
                    doProcessOV = 1

    TodayOV = getDataOV(todayOI)
    YestOV = getDataOV(yestOI)
    print("TodayOV and YestOV and TodayOI is :",TodayOV,YestOV,TodayOI)
    
            
    if((TodayOV == 0) and (YestOV == 0)):
#        print("(int)(YestOV) ==0) and ((int)(TodayOV)==0 ")
        return 0

    elif(((int)(YestOV) ==0) and ((int)(TodayOV) !=0)):
        if((int)(TodayOV)>(int)(OIthresold)):
            if(doProcessOV == 1):
                if((int)(TodayOV) > (int)(thresold)):
                    value = (((int)(TodayOV)/100)*100)
#                    print("(int)(YestOV) ==0) and ((int)(TodayOV)! =0  value is :",value)
                    if(value > thresold):
                        Process = getDiff(TodayOV,TodayOI)
                        if(Process == 1):
                            return value
                        else:
                            return 0
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    
    elif((int)(TodayOV)!=0 and (int)(YestOV)!=0):
        if((int)(TodayOV)>(int)(OIthresold) and (int)(YestOV)>(int)(OIthresold)):
            if(doProcessOV == 1):
                if((int)(TodayOV) == (int)(YestOV)):
                    value = 0
                    return value
                elif((int)(TodayOV)>(int)(YestOV)):
                    value = ((((int)(TodayOV) - (int)(YestOV))/(int)(YestOV))*100)
                    if(value > thresold):
                        print("(int)(TodayOV)>(int)(YestOV) is :",value)
                        Process = getDiff(TodayOV,TodayOI)
                        if(Process == 1):
                            print("(int)(TodayOV)>(int)(YestOV) is :",value)
                            return value
                        else:
                            return 0
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
            return 0
        
    else:
        return 0
    

def mainloop():
    global csvSymbolList
    global totalStocks
    global totalCols
    global thresold
    header_list =[]
    
    generateTotalStockList()
    oCSVOIJumpFile = createOutputOIJumpFile()
    ofile = oCSVOIJumpFile
    
    if os.path.exists(ofile):
        print("file exists:",ofile)
        os.remove(ofile)
        print("file removed")
        
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            oCSVOIJumpFile = createOutputOIJumpFile()
            ofile = oCSVOIJumpFile
            
            if os.path.exists(ofile):
                print("file exists:",ofile)
            else:                
                if(index == 0):
                    iCSVFileName = getStockCSVFiles(contracttype,0)
                    print("file doesnot exists:",ofile)
                    ifile = iCSVFileName 
                    if os.path.exists(ifile):
                        print("File Exists:",ifile)
                        data_frame = pd.read_csv(ifile, index_col = False)
                        countCols = data_frame.shape[1]
                        print("countCols is :",countCols)
                        #header_list = data_frame.columns.tolist()
                        if(countCols > getNumberColsData):
                            oColumns = getNumberColsData
                        else:
                            oColumns = countCols

                        today = date.today()
                        dateListHeader = []
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
                    
            iCSVFileName = getStockCSVFiles(contracttype,index)
            ifile = iCSVFileName
            
            if os.path.exists(ifile):
                print("File Exists:",ifile)
                data_frame = pd.read_csv(ifile, index_col = False)
                countCols = data_frame.shape[1]
                countRows = data_frame.shape[0]
                print("number of rows:",countRows)
                print("number of cols:",countCols)
                todayOI = countCols-1
                yestOI = countCols-2
                
                optionSymbol =[]
                openInterest_today =[]               
                oFrow_index =0
                row_index = 0
                j=0
                
                with open(iCSVFileName, 'r') as readFile:
                    readCSV = csv.reader(readFile)
                    fields = next(readCSV)
                    for row in readCSV:
                        optionSymbol = [str(row[0])]
                        doProcess = 1
    #                    print("row[todayOI],row[yestOI] is :",row[todayOI],row[yestOI])
                        value = jumpinOV(row[todayOI],row[yestOI])
                        if(value !=0):
                            print("value in main :",value)
                            if(value > Percentage_Above):
                                openInterest_today = [str(value)]
                                outPutValue = []
                                rowData =[]
                                pastColsDat =[]

                                if(countCols == getNumberColsData):
                                    colFrom =0
                                    colTo =0
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
                                    print("rowData in cols == getnumcols is and symbol optionSymbol :",pastColsDat,optionSymbol)

                                    ### Dd process if columns does not contain 'U'
                                    for j in range(0,len(pastColsDat)):
                                        if(pastColsDat[j] == 'U'):
#                                            print("No operation row[j],j,optionSymbol: ",pastColsDat[j],j,optionSymbol)
                                            doProcess = 1
                                        
                                    if(doProcess == 1):
                                        optSymbol = optionSymbol
                                        addDataoFile = 1
                                        outPutValue =[]
                                        rowData = data_frame.iloc[row_index,colFrom:colTo]
                                        for item in range(0,len(rowData)):
                                            rowData[item] = rowData[item].replace('[','')
                                            rowFindU  = str(rowData[item]).split(":")
                                            result = str(rowFindU).find('U')
                                            if(result == -1):
                                                outPutValue.append(rowData[item])
                                            else:
                                                rowData[item] = 0
                                                outPutValue.append(rowData[item])
                                        
                                            
#                                        print("outPutValue.... is :",outPutValue)
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
                                            
                                            rowDatas = [(optionSymbol)+(rowItem)+(outPutValue)]
                                            
                                            if os.path.exists(ofile):
                                                with open(ofile, 'a') as ocsvfile:
                                                    wr = csv.writer(ocsvfile,lineterminator='\r')
                                                    for row in rowDatas:
                                                        wr.writerow(row)
                                            else:
                                                with open(ofile, 'w') as ocsvfile:
                                                    writer = csv.writer(ocsvfile)
                                                    writer.writerow(['Symbol','YestOI','TodayOI','%Jump'])
                                        
                                elif(countCols > getNumberColsData and countCols != getNumberColsData ):
                                    ("hello from if(countCols > getNumberColsData and countCols != getNumberColsData )")
                                    colFrom =0
                                    colTo =0
                                    outPutValue = []
                                    rowData =[]
                                    pastColsDat =[]
                                    colFrom = countCols-getNumberColsData
                                    colTo = countCols                                    
                                    pastColsDat =data_frame.iloc[row_index,colFrom:colTo]
                                     
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
                                        for item in range(0,len(rowData)):
                                            rowData[item] = rowData[item].replace('[','')
                                            rowFindU  = str(rowData[item]).split(":")
                                            result = str(rowFindU).find('U')
                                            if(result == -1):
                                                outPutValue.append(rowData[item])
                                            else:
                                                rowData[item] = 0
                                                outPutValue.append(rowData[item])
                                        
                                            
                                        print("outPutValue.............. is :",outPutValue)
                                        for item in range(0,len(outPutValue)):
                                            if(outPutValue[item] == 'NU'):
                                                print("No operation row[j],j,optionSymbol: ",outPutValue[item],item,optionSymbol)
                                                addDataoFile = 0
                                                    
                                        if(addDataoFile == 1):
                                            print(" rowData is :",rowData)
                                            rowData = [(optionSymbol)+(outPutValue)]
                                            
                                            
                                            if os.path.exists(ofile):
                                                with open(ofile, 'a') as ocsvfile:
                                                    wr = csv.writer(ocsvfile,lineterminator='\r')
                                                    for row in rowData:
                                                        wr.writerow(row)
                                            else:
                                                with open(ofile, 'w') as ocsvfile:
                                                    writer = csv.writer(ocsvfile)
                                                    writer.writerow(['Symbol','YestOI','TodayOI','%Jump'])
                                                        
                                else:
                                    #if(countCols < getNumberColsData):
                                    print("Hello from countCols < getNumberCols")
                                    colFrom =0
                                    colTo =0
                                    outPutValue = []
                                    rowData =[]
                                    pastColsDat =[]
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
                                            #print("No operation row[j],j,optionSymbol: ",pastColsDat[j],j,optionSymbol)
                                            doProcess = 1
                                            
                                    if(doProcess == 1):
                                        optSymbol = optionSymbol
                                        addDataoFile = 1
                                        outPutValue =[]
                                        rowData = data_frame.iloc[row_index,colFrom:colTo]
                                        print("rowData in cols <getnumcols is and optionSymbol :",rowData,optSymbol)

                                        for item in range(0,len(rowData)):
                                            rowData[item] = rowData[item].replace('[','')
                                            rowFindU  = str(rowData[item]).split(":")
                                            result = str(rowFindU).find('U')
                                            if(result == -1):
                                                outPutValue.append(rowData[item])
                                            else:
                                                rowData[item] = 0
                                                outPutValue.append(rowData[item])
                                        
                                            
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
                                            
                                            rowDatas = [(optionSymbol)+(rowItem)+(outPutValue)]
                                            
                                            print(" rowDatas outPutValue.............. is :",rowDatas)
                                            if os.path.exists(ofile):
                                                with open(ofile, 'a') as ocsvfile:
                                                    wr = csv.writer(ocsvfile,lineterminator='\r')
                                                    for row in rowDatas:
                                                        wr.writerow(row)
                                            else:
                                                with open(ofile, 'w') as ocsvfile:
                                                    writer = csv.writer(ocsvfile)
                                                    writer.writerow(['Symbol','YestOI','TodayOI','%Jump'])
                                    
                        row_index += 1
                        #print("row index is :",row_index)
                        
                
            else:
                print("File Does not Exists:",ifile)
        
    
mainloop() 
                    
print('done')

