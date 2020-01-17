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
import Commonapi
import dataapi
import globalheader

ifilepath = './../datacolls/output/'
ifilestocklist = './../datacolls/input/'+'StockList.csv'

ofilepath = './output/'
ofilename = ofilepath+'OVPerJump_AllStocks'
ochartfilename = ofilepath+'OVUPXLChart_AllStocks'
ichartfilename = ofilepath+'OVChartInput_AllStocks'

#processOptionVolumeJumpMain calls the jumpOVAllstocks in dataapi which calculates jump in ov of all stock list
    # input - getNumberColsData,Percentage_OV_Jump,thresold,money_margin,Diff_IN_OI_OV_Percentage_Above
        # Percentage_OI_Jump - Percentage in jump in open interest from today to yest open interest
        #thresold - minimum number of open interest
        #money_margin - minimum money invested in open interest
        #getNumberColsData - the numbers of trading days
        #Diff_IN_OI_OV_Percentage_Above - diff in percentage in open interest and option vol    
    # output - call_error

def processoptionvoljumpAllStocks(getNumberColsData,Percentage_OV_Jump,thresold,money_margin,Diff_IN_OI_OV_Percentage_Above):

     if(Commonapi.info == 1):
        logging.info('processOptionVolumeJumpMain started')
    
    totalStocks,stockSymbol,stockExpDate = dataapi.generateTotalStockList(ifilestocklist)
    call_error = dataapi.jumpOVAllstocks(totalStocks,stockSymbol,ofilename,thresold,Percentage_OV_Jump,money_margin,getNumberColsData,Diff_IN_OI_OV_Percentage_Above)
     if(Commonapi.info == 1):
        logging.info('processOptionVolumeJumpMain Ended')
    return call_error

if __name__ == "__main__":

     if(Commonapi.info == 1):
        logging.info('optionvoljumpAllStocks Started')

    getNumberColsData = 40
    Percentage_OV_Jump = 200
    thresold = 50
    money_margin = 20000
    Diff_IN_OI_OV_Percentage_Above = 200

    #calls local function processOptionVolumeJumpMain
    call_error = processoptionvoljumpAllStocks(getNumberColsData,Percentage_OV_Jump,thresold,money_margin,Diff_IN_OI_OV_Percentage_Above)
    if(Commonapi.info == 1):
        logging.info('optionvoljumpAllStocks Ended')

    #if call_error success from processOptionVolumeJumpMain call generateInputFormatForXLChartMain 
    
    if(call_error == globalheader.Success):
        if(Commonapi.info == 1):
            logging.info('%s %d', 'processoptionvoljumpAllStocks Success', call_error)
        xlfileinputgenerator.generateInputFormatForXLChartMain(ofilename,ochartfilename,ichartfilename)
    else:
        logging.error('%s %d', 'processoptionvoljumpAllStocks Failed', call_error)
                    
    logging.warning('done')                


