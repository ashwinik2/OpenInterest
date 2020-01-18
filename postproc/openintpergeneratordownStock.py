
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

ofilepath = './output/'
ofilename = ofilepath+'OIPerDown'

ochartfilename = ofilepath+'OIDownXLChart'
ichartfilename = ofilepath+'OIDownChartInput'

#openIntPerCalculatorDownMain calls downOIStock which is in dataapi.py which calculates the down in OI of  a stocks
    # input - getNumberColsData,Percentage_OI_Down,thresold,money_margin,stocklist
        # Percentage_OI_Down - Percentage in down in open interest from today to yest open interest
        #thresold - minimum number of open interest
        #money_margin - minimum money invested in open interest
        #getNumberColsData - the numbers of trading days
        #stocklist - stock symbol
    # output - call_error

def processopenintpergeneratordownStock(getNumberColsData,Percentage_OI_Down,thresold,money_margin,stockList):
    if(globalheader.info == 1):
        globalheader.logging.info('processopenintpergeneratordownStock Started')

    global ofilename
    global ochartfilename
    global ichartfilename
    totalStocks = len(stockList)
    stockSymbol = stockList[0]
    ofilename = ofilename+'_'+stockSymbol
    ochartfilename = ochartfilename+'_'+stockSymbol
    ichartfilename = ichartfilename +'_'+stockSymbol
    call_error = dataapi.downOIAllstocks(totalStocks,stockList,ofilename,getNumberColsData,Percentage_OI_Down,thresold,money_margin)
    if(globalheader.info == 1):
        globalheader.logging.info('processopenintpergeneratordownStock Ended')
    return call_error


if __name__ == "__main__":

    if(globalheader.info == 1):
        globalheader.logging.info('openintpergeneratordownStock Main Started')
    #stockList =['AAPL']
    symbol = raw_input("Enter symbol :") 
    print(symbol)
    stockList = []
    stockList.append(symbol)
    getNumberColsData = 40
    Percentage_OI_Down = 100
    money_margin = 20000
    thresold = 50
    call_error = processopenintpergeneratordownStock(getNumberColsData,Percentage_OI_Down,thresold,money_margin,stockList)
    if(globalheader.info == 1):
        globalheader.logging.info('openintpergeneratordownStock Main Ended')

    #if success from openIntPerCalculatorDownMain call generateInputFormatForXLChartMain
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'processopenintpergeneratordownStock Success', call_error)
        xlfileinputgenerator.generateInputFormatForXLChartMain(ofilename,ochartfilename,ichartfilename)
    else:
        globalheader.logging.error('%s %d', 'processopenintpergeneratordownStock Failed', call_error)
                    
    print('done')                 



