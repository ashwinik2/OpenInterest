
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

ifilepath = './../datacolls/output/'
ifilestocklist = './../datacolls/input/'+'StockList.csv'

ofilepath = './output/'
ofilename = ofilepath+'OIPerJump_AllStocks'

ochartfilename = ofilepath+'OIUPXLChart_AllStocks'
ichartfilename = ofilepath+'OIUPChartInput_AllStocks'

#calculateJumpOI - calls jumpOIAllstocks in dataapi.py which calculates jump in OI of all stocks 
    # input - Percentage_OI_Jump,thresold,money_margin,getNumberColsData
        # Percentage_OI_Jump - Percentage in jump in open interest from today to yest open interest
        #thresold - minimum number of open interest
        #money_margin - minimum money invested in open interest
        #getNumberColsData - the numbers of trading days

    # output - call_error

def processopenintpergeneratorJumpAllstocks(Percentage_OI_Jump,thresold,money_margin,getNumberColsData):
    if(globalheader.info == 1):
        globalheader.logging.info('processopenintpergeneratorJumpAllstocks Started')
    
    totalStocks,stockSymbol,stockExpDate = dataapi.generateTotalStockList(ifilestocklist)
    call_error = dataapi.jumpOIAllstocks(totalStocks,stockSymbol,ofilename,thresold,Percentage_OI_Jump,money_margin,getNumberColsData)
    if(globalheader.info == 1):
        globalheader.logging.info('processopenintpergeneratorJumpAllstocks Ended')
    return call_error
        
if __name__ == "__main__":

    if(globalheader.info == 1):
        globalheader.logging.info('openintpergeneratorJUmpAllstocks Started')

    getNumberColsData = 40
    Percentage_OI_Jump = 400
    thresold = 50
    money_margin = 20000
    call_error = processopenintpergeneratorJumpAllstocks(Percentage_OI_Jump,thresold,money_margin,getNumberColsData)
    if(globalheader.info == 1):
        globalheader.logging.info('openintpergeneratorJUmpAllstocks Ended')

    #if call_error success from calculateJumpOI call generateInputFormatForXLChartMain 
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'processopenintpergeneratorJumpAllstocks Success', call_error)
        xlfileinputgenerator.generateInputFormatForXLChartMain(ofilename,ochartfilename,ichartfilename)
    else:
        globalheader.logging.error('%s %d', 'processopenintpergeneratorJumpAllstocks Failed', call_error)
                    
    globalheader.logging.warning('done')

