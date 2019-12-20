### openinterestpergeneratorprice.py does calculates the open interest
### jump from yest to today open interest more 400%

import csv
import time
import os
import os.path
import datetime
from os import path
import pandas as pd
from pandas import DataFrame
from datetime import date
from datetime import datetime
from datetime import timedelta
import commonapi
import xlfileinputgenerator

stockSymbol = []
stockExpDate = []
todayDate = []   

global totalStocks
global csvSymbolList

thresold = 50
getNumberColsData = 20
Percentage_Above = 400
money_margin = 20000

contractType =['CALL','PUT']   
date_format = '%m/%d/%Y'

ifilepath = './../datacolls/output/'
ifilestocklist = './../datacolls/input/'+'StockList.csv'

ofilepath = './output/'
ofilename = ofilepath+'OIPerJump'

ochartfilename = ofilepath+'OIUPXLChart'
ichartfilename = ofilepath+'OIChartInput'



#compares OI today and yest send result if greater than percentage jump thresold
def jumpinOI(todayrowData,yestrowData):
    global thresold

    TodayOI,YestOI = commonapi.getDataOI(todayrowData,yestrowData)

    TodayOP,YestOP = commonapi.getDataOP(todayrowData,yestrowData)
  
    if(((int)(YestOI) ==0) and ((int)(TodayOI) ==0)):
        return 0
    
    elif(((int)(YestOI) ==0) and ((int)(TodayOI) !=0)):
        if((int)(TodayOI) > (int)(thresold)):
            value = (((int)(TodayOI)/100)*100)
            if(value > thresold):
                moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                if(moneyinv > money_margin):
                    print("(int)(TodayOI)>(int)(YestOI) is :",value)
                    return value
                else:
                    return 0
                return value
            else:
                return 0
        else:
            return 0
    
    elif((int)(TodayOI)!=0 and (int)(YestOI)!=0):
        if((int)(TodayOI)>(int)(thresold) and (int)(YestOI)>(int)(thresold)):
            if((int)(TodayOI) == (int)(YestOI)):
                value = 0
                return value
            elif((int)(TodayOI)>(int)(YestOI)):
                value = ((((int)(TodayOI) - (int)(YestOI))/(int)(YestOI))*100)
                if(value > thresold):
                    moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                    if(moneyinv > money_margin):
                        print("(int)(TodayOI)>(int)(YestOI) is :",value)
                        return value
                    else:
                        return 0
                else:
                    return 0
            elif((int)(TodayOI)<(int)(YestOI)):
                value = ((((int)(YestOI) - (int)(TodayOI))/(int)(TodayOI))*100)
                if(value > thresold):
                    moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                    if(moneyinv > money_margin):
                        print("(int)(TodayOI)>(int)(YestOI) is :",value)
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


def mainloop():
    global csvSymbolList
    global totalStocks
    global totalCols
    global thresold
    
    totalStocks,stockSymbol,stockExpDate = commonapi.generateTotalStockList(ifilestocklist)
    oCSVOIJumpFile = commonapi.createOutputOIJumpFile(ofilename)
    
    if os.path.exists(oCSVOIJumpFile):
        print("file exists:",oCSVOIJumpFile)
        os.remove(oCSVOIJumpFile)
        print("file removed")
        
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            oCSVOIJumpFile = commonapi.createOutputOIJumpFile(ofilename)
            print("oCSVOIJumpFile= oCSVOIJumpFile is :",oCSVOIJumpFile)
            data_frame = 0
            if os.path.exists(oCSVOIJumpFile):
                print("file exists:",oCSVOIJumpFile)
            else:
                print("file doesnot exists:",oCSVOIJumpFile)
                if(index == 0):
                    commonapi.generateDateList(oCSVOIJumpFile,getNumberColsData)                        
                    
            iCSVFile = commonapi.getStockCSVFiles(contracttype,stockSymbol[index],ifilepath)
            
            if os.path.exists(iCSVFile):
                print("File Exists:",iCSVFile)
                data_frame = pd.read_csv(iCSVFile, index_col = False)
                countCols = data_frame.shape[1]
                countRows = data_frame.shape[0]
                todayrowData = countCols-1
                yestrowData = countCols-2
                
                optionSymbol =[]
                row_index = 0
                
                with open(iCSVFile, 'r') as readFile:
                    readCSV = csv.reader(readFile)
                    fields = next(readCSV)
                    for row in readCSV:
                        optionSymbol = [str(row[0])]
                        doProcess = 1
                        
                        OI = jumpinOI(row[todayrowData],row[yestrowData])                        
                        if(OI !=0):
                            if(OI > Percentage_Above):
                                
                                if(countCols == getNumberColsData):
                                    commonapi.processColEqual(oCSVOIJumpFile,data_frame,optionSymbol,row_index,getNumberColsData)                                                                        
                                elif(countCols > getNumberColsData and countCols != getNumberColsData ):
                                    commonapi.processColGreater(oCSVOIJumpFile,data_frame,optionSymbol,row_index,getNumberColsData)                                                        
                                else:
                                    commonapi.processColLess(oCSVOIJumpFile,data_frame,optionSymbol,row_index,getNumberColsData)
                                    
                        row_index += 1
            else:
                print("File Does not Exists:",iCSVFile)
            
mainloop()
xlfileinputgenerator.mainloop(ofilename,ochartfilename,ichartfilename)
                    
print('done')

