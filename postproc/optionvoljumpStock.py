
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
import Commonapi
import dataapi
import globalheader

ifilepath = './../datacolls/output/'

ofilepath = './output/'
ofilename = ofilepath+'OVPerJump'
ochartfilename = ofilepath+'OVUPXLChart'
ichartfilename = ofilepath+'OVChartInput'

#processOptionVolumeJumpMain - calls jumpOVAllstocks in dataapi.py which calculates option volume jump of a stock
    # input - getNumberColsData,Percentage_OV_Jump,thresold,money_margin,Diff_IN_OI_OV_Percentage_Above,stockList
        # Percentage_OI_Jump - Percentage in jump in open interest from today to yest open interest
        #thresold - minimum number of open interest
        #money_margin - minimum money invested in open interest
        #getNumberColsData - the numbers of trading days
        #Diff_IN_OI_OV_Percentage_Above - diff in percentage in open interest and option vol
        #stockList - name of the stock symbol    
    # output - call_error

def processOptionVolumeJumpMain(getNumberColsData,Percentage_OV_Jump,thresold,money_margin,Diff_IN_OI_OV_Percentage_Above,stockList):
    if(Commonapi.debug == 1):
        print("processOptionVolumeJumpMain started")
    
    global ofilename
    global ochartfilename
    global ichartfilename
    totalStocks = len(stockList)
    stockSymbol = stockList[0]
    ofilename = ofilename+'_'+stockSymbol
    ochartfilename = ochartfilename+'_'+stockSymbol
    ichartfilename = ichartfilename +'_'+stockSymbol
    
    call_error = dataapi.jumpOVAllstocks(totalStocks,stockList,ofilename,thresold,Percentage_OV_Jump,money_margin,getNumberColsData,Diff_IN_OI_OV_Percentage_Above)
    if(Commonapi.debug == 1):
            print("processOptionVolumeJumpMain ended")
    return call_error
                
if __name__ == "__main__":

    if(Commonapi.debug == 1):
        print("optionvoljumpStock started")
    stockList =['AAPL']
    getNumberColsData = 40
    Percentage_OV_Jump = 100
    thresold = 50
    money_margin = 20000
    Diff_IN_OI_OV_Percentage_Above = 200
    call_error = processOptionVolumeJumpMain(getNumberColsData,Percentage_OV_Jump,thresold,money_margin,Diff_IN_OI_OV_Percentage_Above,stockList)
    if(Commonapi.debug == 1):
        print("optionvoljumpStock ended")
        
    #if call_error success from processOptionVolumeJumpMain call generateInputFormatForXLChartMain 
    
    if(call_error == globalheader.Success):
        xlfileinputgenerator.generateInputFormatForXLChartMain(ofilename,ochartfilename,ichartfilename)
    else:
        print("openIntPerCalculatorUpMain is failed:",call_error)             
    print('done')

