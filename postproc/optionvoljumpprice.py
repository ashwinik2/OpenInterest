### optionvoljumpprice.py does calculates the option volume
### jump from yest to today option volume more 400%

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
import xlfileinputgenerator
import commonapi


thresold = 50
OIthresold = 50
Diff_Percentage_Above = 200
money_margin = 20000

contractType =['CALL','PUT']   
date_format = '%m/%d/%Y'

ifilepath = './../datacolls/output/'
ifilestocklist = './../datacolls/input/'+'StockList.csv'

ofilepath = './output/'
ofilename = ofilepath+'OVPerJump_400'
ochartfilename = ofilepath+'OVUPXLChart'
ichartfilename = ofilepath+'OVChartInput'


# process the diff between Today OI and Today OV
def getPercentage(TodayOV,TodayOI):
    if((int)(TodayOV)>(int)(OIthresold) and (int)(TodayOI)>(int)(OIthresold)):
        if((int)(TodayOV)>(int)(TodayOI)):
            value = ((((int)(TodayOV) - (int)(TodayOI))/(int)(TodayOI))*100)
            if(value >= Diff_Percentage_Above):
                print("getDiff(TodayOV,TodayOI) :",value)
                return 1
            else:
                return 0
        return 0
    return 0

#calculate the jump in today OV and yest OV and return value
def jumpinOV(todayrowData,yestrowData):
    global thresold    
    doProcessOV = 0
    
    TodayOI,YestOI = commonapi.getDataOI(todayrowData,yestrowData)    
    TodayOV,YestOV = commonapi.getDataOV(todayrowData,yestrowData)    
    TodayOP,YestOP = commonapi.getDataOP(todayrowData,yestrowData)
     
    if((int)(TodayOI) != 0 and (int)(YestOI) !=0):
        if((int)(TodayOI)>(int)(OIthresold)):
            if((int)(TodayOI) == (int)(YestOI)):
              doProcessOV = 1  
            elif((int)(TodayOI)>(int)(YestOI)):
                value = ((((int)(TodayOI) - (int)(YestOI))/(int)(YestOI))*100)
                if(value > OIthresold):
                    doProcessOV = 0
                else:
                    doProcessOV = 1
            else:
                value = ((((int)(YestOI) - (int)(TodayOI))/(int)(TodayOI))*100)
                if(value > OIthresold):
                    doProcessOV = 0
                else:
                    doProcessOV = 1
    
            
    if((TodayOV == 0) and (YestOV == 0)):
        return 0

    elif(((int)(YestOV) ==0) and ((int)(TodayOV) !=0)):
        if((int)(TodayOV)>(int)(OIthresold)):
            if(doProcessOV == 1):
                if((int)(TodayOV) > (int)(thresold)):
                    value = (((int)(TodayOV)/100)*100)
                    if(value > thresold):
                        Process = getPercentage(TodayOV,TodayOI)
                        if(Process == 1):
                            moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                            if(moneyinv > money_margin):
                                print("moneyinv > money_margin 0")
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
    
    elif((int)(TodayOV)!=0 and (int)(YestOV)!=0):
        if((int)(TodayOV)>(int)(OIthresold) ):
            if(doProcessOV == 1):
                if((int)(TodayOV) == (int)(YestOV)):
                    value = 0
                    return value
                elif((int)(TodayOV)>(int)(YestOV)):
                    value = ((((int)(TodayOV) - (int)(YestOV))/(int)(YestOV))*100)
                    if(value > thresold):
                        Process = getPercentage(TodayOV,TodayOI)
                        if(Process == 1):
                            moneyinv = (int)((float)(TodayOI)*(float)(TodayOP)*100)
                            if(moneyinv > money_margin):
                                print("(int)(TodayOV)>(int)(YestOV) is :",value)
                                print("moneyinv > money_margin !0")
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
        
    else:
        return 0
    


#main loop
def processOptionVolumeJumpMain(getNumberColsData,Percentage_OV_Jump):
    
    totalStocks,stockSymbol,stockExpDate = commonapi.generateTotalStockList(ifilestocklist)
    oCSVOIJumpFile = commonapi.createOutputOIJumpFile(ofilename)
    oCSVOIJumpFile = oCSVOIJumpFile
    
    if os.path.exists(oCSVOIJumpFile):
        print("file exists:",oCSVOIJumpFile)
        os.remove(oCSVOIJumpFile)
        print("file removed")
        
    for index in range(totalStocks): 
        for contracttype in range(len(contractType)):
            oCSVOIJumpFile = commonapi.createOutputOIJumpFile(ofilename)
            oCSVOIJumpFile = oCSVOIJumpFile
            print("ofile = oCSVOIJumpFile is :",oCSVOIJumpFile)
            data_frame = 0
            if os.path.exists(oCSVOIJumpFile):
                print("file exists:",oCSVOIJumpFile)
            else:
                print("file doesnot exists:",oCSVOIJumpFile)
                if(index == 0):
                    commonapi.generateDateList(oCSVOIJumpFile,getNumberColsData)                        
                    
            iCSVFile = commonapi.getStockCSVFile(contracttype,stockSymbol[index],ifilepath)
            
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
                        
                        OV = jumpinOV(row[todayrowData],row[yestrowData])
                        
                        if(OV != 0):                            
                            if(OV >= Percentage_OV_Jump):
                                if(countCols == getNumberColsData):
                                    commonapi.processColEqual(oCSVOIJumpFile,data_frame,optionSymbol,row_index,getNumberColsData)                                                                        
                                elif(countCols > getNumberColsData and countCols != getNumberColsData ):
                                    commonapi.processColGreater(oCSVOIJumpFile,data_frame,optionSymbol,row_index,getNumberColsData)                                                        
                                else:
                                    commonapi.processColLess(oCSVOIJumpFile,data_frame,optionSymbol,row_index,getNumberColsData)
                                    
                        row_index += 1
            else:
                print("File Does not Exists:",iCSVFile)
                
if __name__ == "__main__":

    getNumberColsData = 20
    Percentage_OV_Jump = 400
##    getNumberColsData = raw_input("Enter number of days data you want : ") 
##    print(getNumberColsData)
##    getNumberColsData = (int)(getNumberColsData)
##    Percentage_OV_Jump = raw_input("Enter what percentage jump in open interest : ")
##    Percentage_OV_Jump = (int)(Percentage_OV_Jump)
    processOptionVolumeJumpMain(getNumberColsData,Percentage_OV_Jump)
    xlfileinputgenerator.generateInputFormatForXLChartMain(ofilename,ochartfilename,ichartfilename)
             
    print('done')

