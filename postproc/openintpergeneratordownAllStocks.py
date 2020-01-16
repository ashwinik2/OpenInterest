
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
import dataapi
import globalheader

ifilepath = './../datacolls/output/'
ifilestocklist = './../datacolls/input/'+'StockList.csv'

ofilepath = './output/'
ofilename = ofilepath+'OIPerDown_AllStocks'

ochartfilename = ofilepath+'OIDownXLChart_AllStocks'
ichartfilename = ofilepath+'OIDownChartInput_AllStocks'

#openIntPerCalculatorDownMain calls downOIAllstocks which is in dataapi.py which calculates the down in OI of all stocks
    # input - getNumberColsData,Percentage_OI_Down,thresold,money_margin
        # Percentage_OI_Down - Percentage in down in open interest from today to yest open interest
        #thresold - minimum number of open interest
        #money_margin - minimum money invested in open interest
        #getNumberColsData - the numbers of trading days
    # output - call_error

def openIntPerCalculatorDownMain(getNumberColsData,Percentage_OI_Down,thresold,money_margin):
    
    if(Commonapi.debug == 1):
        Print("openIntPerCalculatorDownMain started")
    totalStocks,stockSymbol,stockExpDate = dataapi.generateTotalStockList(ifilestocklist)
    call_error = dataapi.downOIAllstocks(totalStocks,stockSymbol,ofilename,getNumberColsData,Percentage_OI_Down,thresold,money_margin)
    if(Commonapi.debug == 1):
        Print("openIntPerCalculatorDownMain ended")
    return call_error


if __name__ == "__main__":

    if(Commonapi.debug == 1):
        Print("openintpergeneratordownAllStocks Main started")

    getNumberColsData = 40
    Percentage_OI_Down = 200
    money_margin = 20000
    thresold = 50
    call_error = openIntPerCalculatorDownMain(getNumberColsData,Percentage_OI_Down,thresold,money_margin)
    if(Commonapi.debug == 1):
        Print("openintpergeneratordownAllStocks Main started")
    if(call_error == globalheader.Success):
        xlfileinputgenerator.generateInputFormatForXLChartMain(ofilename,ochartfilename,ichartfilename)
    else:
        print("openIntPerCalculatorUpMain is failed:",call_error)
                    
    print('done')                 
