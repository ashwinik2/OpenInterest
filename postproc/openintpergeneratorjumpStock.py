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
import Commonapi
import xlfileinputgenerator
import globalheader
import dataapi


ofilepath = './output/'
ofilename = ofilepath+'OIPerJump'

ochartfilename = ofilepath+'OIUPXLChart'
ichartfilename = ofilepath+'OIUPChartInput'

#openIntPerCalculatorUpMain - calls jumpOIAllstocks which calculates OI jump of a stock
    # input - Percentage_OI_Jump,thresold,money_margin,getNumberColsData,stockList
        # Percentage_OI_Jump - Percentage in jump in open interest from today to yest open interest
        #thresold - minimum number of open interest
        #money_margin - minimum money invested in open interest
        #getNumberColsData - the numbers of trading days
        #stockLIst - name of the stock symbol

    # output - call_error
 
def openIntPerCalculatorUpMain(getNumberColsData,Percentage_OI_Jump,thresold,money_margin,stockList):

    if(Commonapi.debug == 1):
        print("openIntPerCalculatorUpMain started")
    global ofilename
    global ochartfilename
    global ichartfilename
    totalStocks = len(stockList)
    stockSymbol = stockList[0]
    ofilename = ofilename+'_'+stockSymbol
    ochartfilename = ochartfilename+'_'+stockSymbol
    ichartfilename = ichartfilename +'_'+stockSymbol
    oCSVOIJumpFile = Commonapi.createOutputOIJumpFile(ofilename)    
    call_error = dataapi.jumpOIAllstocks(totalStocks,stockList,ofilename,thresold,Percentage_OI_Jump,money_margin,getNumberColsData)
    if(Commonapi.debug == 1):
        print("openIntPerCalculatorUpMain ended")
    return call_error
        
if __name__ == "__main__":

    if(Commonapi.debug == 1):
        print("openintpergeneratorjumpStock started")

    stockList =['AAPL']
    getNumberColsData = 30
    Percentage_OI_Jump = 200
    thresold = 50
    money_margin = 20000
    call_error = openIntPerCalculatorUpMain(getNumberColsData,Percentage_OI_Jump,thresold,money_margin,stockList)
    if(Commonapi.debug == 1):
        print("openintpergeneratorStock started")
        
    #if call_error success from openIntPerCalculatorUpMain call generateInputFormatForXLChartMain 
    
    if(call_error == globalheader.Success):
        xlfileinputgenerator.generateInputFormatForXLChartMain(ofilename,ochartfilename,ichartfilename)
    else:
        print("openIntPerCalculatorUpMain is failed:",call_error)
                    
    print('done')


