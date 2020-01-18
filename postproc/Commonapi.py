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
import enum
import globalheader
import dataapi
import sys

csv.field_size_limit(sys.maxsize)
contractType =['CALL','PUT']
listOfStr = ["OI", "SP" , "SV" , "OP" , "OV"]
data_seperator =':'
name_seperator = ':'

csvDataFilePath = './../datacolls/output/'
#
#declare enums for CALL,PUT
class Contracttype(enum.Enum):
    CALL = 0
    PUT = 1
# createoFile(symbol,ofilename) return the output xlxs file name by combining today date with sysmbol   
    #input
        #symbol - name of the stock
        #ofilename - output file name
    #output
        #output xlsx file name
def createoFile(symbol,ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    oxlsxfilename = ofilename+'_'+symbol+'_'+today+'.xlsx'
    return oxlsxfilename

# getoFile(symbol,ofilename) return the output xlxs file name by combining today date with sysmbol   
    #input
        #symbol - name of the stock
        #ofilename - output file name
    #output
        #output xlsx file name 
def getoFile(symbol,ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    oxlsxfilename = ofilename+'_'+symbol+'_'+today+'.xlsx'
    return oxlsxfilename

#getOptExpDateFromCSV(optionSymbol) return the extracted exp date '011720' from option symbol 'AAPL_011720C250'  
    #input
        #optionSymbol - optionSymbol
    #output
        #expdate        
def getOptExpDateFromCSV(optionSymbol):
    symbol,date = optionSymbol.split('_')
    date = list(str(date))
    length = len(date)
    expdate = date[4]+date[5]+date[0]+date[1]+date[2]+date[3]
    return expdate

#getDateList(iCSVFile,getNumberColsData) return stocks number of trading days date header list  
    #input
        #iCSVFile - stock csv file name
        #getNumberColsData - number of trading days
    #output
        #stock number of trading days date header list
def getDateList(iCSVFile,getNumberColsData):
    data_frame = pd.read_csv(iCSVFile, index_col = False)
    csvDateHeaderlist = []
    countCols = data_frame.shape[1]
    if(countCols > getNumberColsData):
        getNumberColsData = getNumberColsData
    elif(countCols < getNumberColsData):
        getNumberColsData = countCols -1
    else:
        getNumberColsData = countCols -1
    colFrom = countCols-getNumberColsData
    colTo = countCols -1
    csvDateHeaderlist = data_frame.columns.tolist()
    return csvDateHeaderlist

#getSymbol(Symbol,date,contracttype,strikeprice) return string concatenated of symbol,expdate,optiontype and strikeprice
    #input
        #symbol - stock symbol
        #date - exp date(011720 - MMDDYY)
        #option type - 'C' or 'P' which means call or put
        #strikeprice - strike price of the stock
    #output
        #call_error - Success or OPT_EXP_DATE_IS_INCORRECT
        #string - 'AAPL_011720C250' or 'AAPL01720P250'  
def getSymbol(Symbol,date,contracttype,strikeprice):
    optiontype = 0
    expdate = []
    if(contracttype == Contracttype.CALL.value):
        optiontype = 'C'
    else:
       optiontype = 'P'

    expdate = []
    if(len(date) == 6):
        expdate = date[2]+date[3]+date[4]+date[5]+date[0]+date[1]        
        string = str(Symbol)+'_'+str(expdate)+str(optiontype)+str(strikeprice)
#        print("string is :",string)
        call_error = globalheader.Success
        return call_error,string
    else:
        call_error = globalheader.OPT_EXP_DATE_IS_INCORRECT
        return call_error,0

#return removed duplicates item from list
def removeDuplicateItems(list): 
    final_list = [] 
    for num in list: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list

#getOptionStrikePrice(optionSymbol) return strikeprice extracted from option symbol
    #input
        #optionSymbol - stock option symbol
    #output
        #strikeprice
def getOptionStrikePrice(optionSymbol):
    n = 7
    symbol,strikeprice = optionSymbol.split('_')
    strikeprice  = list(str(strikeprice ))
    length = len(strikeprice )
    strikeprice= strikeprice[n:]
    strikeprice =''.join(strikeprice)
    return strikeprice

#getInputFile(ifilename) return concatenated csv ifilename with today date
    #input
        #ifilename - input filename
    #output
        #stockCsvfilename - "AAPL_01_17_2020.csv"
def getInputFile(ifilename):       
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ifilename+'_'+today+'.csv'
    return stockCsvfilename


def getInputfile(ifilename):       
    stockCsvfilename = ifilename
    return stockCsvfilename

#extract(string, start=':') return extracted sepearator from string
    #input
        #string - 'OI:200'
    #output
        #string -'OI,200'       
def extract(string, start=':'):
        return string[string.index(start)+1]

#createoxlFile(ofilename) return concatenated ofilename with today date of xlsx file
    #input
        #ofilename -"OIXLChart"
    #output
        #oxlfilename -"OIXLChart_01_17_2020.xlsx"
def createoxlFile(ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    oxlfilename = ofilename+'_'+today+'.xlsx'
    return oxlfilename

#createOutputOIJumpFile(ofilename) return concatenated ofilename with today date of csv file
    #input
        #ofilename -"OIPer_Jump"
    #output
        #oxlfilename -"OIPer_Jump_01_17_2020.csv"
def createOutputOIJumpFile(ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    ocsvfilename = ofilename+'_'+today+'.csv'
    return ocsvfilename

# generateDateList(ofile,getNumberColsData) geneates the dates and  write num of trading days dates requested to the existing ofile
    #input
        #ofile -output local csv file
    #output
        #call_error - Success 
def generateDateList(ofile,getNumberColsData):
    today = date.today()
    header_list =[]
    dateListHeader = []
    prev_days = [today - timedelta(days=i) for i in range(getNumberColsData*2)]
    prev_days = [d for d in prev_days if d.weekday() < 5]       
    for dateItems in prev_days[:getNumberColsData]:                                     
        dates = datetime.datetime.strftime((dateItems), '%Y%m%d')
        dateListHeader.append(dates)
    dateListHeader = sorted(dateListHeader)    
    header_list = ['Symbol']+dateListHeader
    header_list = [header_list]
    
    with open(ofile, 'w') as myfile:
        writer = csv.writer(myfile)
        for row in header_list:
            writer.writerow(row)
    call_error = globalheader.Success
    return call_error

#  writeOIrOVtolocalCSV(ofile,rowData) write column row cell data to the existing output file 
    #input
        #ofile -jumpOI/jumpOV output csv file
        #rowdata - col row cell data
    #output - call_error = globalheader.Success 
    
def writeOIrOVtolocalCSV(ofile,rowData):
    if os.path.exists(ofile):
        with open(ofile, 'a') as ocsvfile:
            wr = csv.writer(ocsvfile,lineterminator='\r')
            for row in rowData:
                wr.writerow(row)
        call_error = globalheader.Success
        return call_error 
    else:
        with open(ofile, 'w') as ocsvfile:
            writer = csv.writer(ocsvfile)
            writer.writerow(['Symbol','YestOI','TodayOI','%Jump'])
        call_error = globalheader.Success
        return call_error

#parseURowData(rowData) parse column row cell data if 'U' present and insert '0' to the existing jumpin OI or OV output csv file 
    #input
        #rowdata - col row cell data
    #output - parsed row data
def parseURowData(rowData):
    outPutValue = []
    for item in range(0,len(rowData)):
        rowData[item] = rowData[item].replace('[','')
        rowFindU  = str(rowData[item]).split(name_seperator)
        result = str(rowFindU).find('U')
        if(result == -1):
            outPutValue.append(rowData[item])
        else:
            rowData[item] = 0
            outPutValue.append(rowData[item])

    return outPutValue

#getopenInterest(OI) return extract open interest from row cell data  
    #input
        #OI - col row cell data list
    #output - ,OI
        #openInterest_error - Success or STOCK_OPEN_INT_UNAVAILABLE
        #OI - open interest value
def getopenInterest(OI):
    OIRef = OI
    if(len(OIRef) == 0 ):
        if(OI[0] == '' or OI[0] == 'U' or OI[0] == '.' or OI[0] == "'"):            
            OI[0] = (int)(0)
            openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
            return openInterest_error,OI[0] 
    if(len(OIRef) == 1):
        if(OI[0] == '' or OI[0] == 'U' or OI[0] == '.' or OI[0] == "'"):
            OI[0] = (int)(0)          
            openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
            return openInterest_error,OI[0] 

    if(len(OIRef) > 1):
        if(OI[0] == '' or OI[0] == 'U' or OI[0] == '.' or OI[0] == "'"):
            OI[0] =(int)(0)            
        if(OI[0] == 0):
            openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
            return openInterest_error,OI[0] 
        else:
            sep = ','
            OI[0] = OI[0].split(sep, 1)[0]
            openInterest_error = globalheader.Success
            return openInterest_error,(float)(OI[0])
            
#getoptionPrice(OP) return extract option price from row cell data  
    #input
        #OP - col row cell data list
    #output 
        #optionPrice_error - Success or STOCK_OPT_PRICE_UNAVAILABLE
        #OI - otion price value        
def getoptionPrice(OP):
    OPRef = OP
    if(len(OPRef) == 0 ): 
        if(OP[0] == '' or OP[0] == 'U' or OP[0] == '.' or OP[0] == "'"):            
            OP[0] = (int)(0)
            optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
            return optionPrice_error,OP[0] 
    if(len(OPRef) == 1): 
        if(OP[0] == '' or OP[0] == 'U' or OP[0] == '.' or OP[0] == "'"):            
            OP[0] = (int)(0)          
            optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
            return optionPrice_error,OP[0]
        
    if(len(OPRef) < 4):          
        optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
        return optionPrice_error,0
    
    if(len(OPRef) > 3):  
        if(OP[3] == '' or OP[3] == 'U' or OP[3] == '.'or OP[3] == "'"):
            OP[3] =(int)(0)
            
        if(OP[3] == 0):
            optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
            return optionPrice_error,OP[0]
        else:
            sep = ','
            OP[3] = OP[3].split(sep, 1)[0]
            optionPrice_Success = globalheader.Success
            return optionPrice_Success,(float)(OP[3])

#getoptionVolume(OV) return extract option volume from row cell data  
    #input
        #OV - col row cell data list
    #output 
        #optionVolume_error - Success or STOCK_OPT_VOLUME_UNAVAILABLE
        #OV - otion volume value  
def getoptionVolume(OV):
    OVRef = OV
    if(len(OVRef) == 0 ):
        OV[0] = (int)(0)
        optionVolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
        return optionVolume_error,OV[0]
    if(len(OVRef) == 1):
        OV[0] = (int)(0)
        optionVolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
        return optionVolume_error,OV[0]

    if(len(OVRef) < 5):
        OV[0] = (int)(0)
        optionVolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
        return optionVolume_error,OV[0]
    if(len(OVRef) > 4):  
        if(OV[4] == '' or OV[4] == 'U' or OV[4] == '.' or OV[4] == "'"):
            OV[4] =(int)(0)            
        if(OV[4] == 0):
            optionVolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
            return optionVolume_error,OV[4]
        else:
            sep = ','
            OV[4] = OV[4].split(sep, 1)[0]
            optionVolume_Success = globalheader.Success
            return optionVolume_Success,(float)(OV[4])

#getstockVolume(SV) return extract stock volume from row cell data  
    #input
        #SV - col row cell data list
    #output 
        #stockVolume_error - Success or STOCK_VOL_UNAVAILABLE
        #SV - stock volume value
def getstockVolume(SV):
    SVRef = SV
    if(len(SVRef) == 0 ): 
        stockVolume_error = globalheader.STOCK_VOL_UNAVAILABLE
        SV[0] = (int)(0)
        return stockVolume_error,SV[0]
    if(len(SVRef) == 1):          
        stockVolume_error = globalheader.STOCK_VOL_UNAVAILABLE
        SV[0] = (int)(0)
        return stockVolume_error,SV[0]

    if(len(SVRef) < 3):          
        stockVolume_error = globalheader.STOCK_VOL_UNAVAILABLE
        SV[0] = (int)(0)
        return stockVolume_error,SV[2]
    if(len(SVRef) > 3):  
        if(SV[2] == '' or SV[2] == 'U' or SV[2] == '.' or SV[2] == "'"):
            SV[2] =(int)(0)            
        if(SV[2] == 0):
            stockVolume_error = globalheader.STOCK_VOL_UNAVAILABLE
            return stockVolume_error,SV[2]
        else:
            sep = ','
            SV[2] = SV[2].split(sep, 1)[0]
            stockVolume_Success = globalheader.Success
            return stockVolume_Success,(float)(SV[2])

#getstockPrice(SP) return extract stock price from row cell data  
    #input
        #SP - col row cell data list
    #output 
        #stockPrice_error - Success or STOCK_PRICE_UNAVAILABLE
        #SP - stock price value
def getstockPrice(SP):
    SPRef = SP
    if(len(SPRef) == 0 ): 
        if(SP[0] == '' or SP[0] == 'U' or SP[0] == '.' or SP[0] == "'"):            
            SP[0] = (int)(0)
            stockPrice_error = globalheader.STOCK_PRICE_UNAVAILABLE
            return stockPrice_error,SP[0]
        
    if(len(SPRef) == 1): 
        if(SP[0] == '' or SP[0] == 'U' or SP[0] == '.' or SP[0] == "'"):            
            SP[0] = (int)(0)          
            stockPrice_error = globalheader.STOCK_PRICE_UNAVAILABLE
            return stockPrice_error,SP[0]
    
    if(len(SPRef) > 1):  
        if(SP[1] == '' or SP[1] == 'U' or SP[1] == '.' or SP[1] == "'"):
            SP[1] =(int)(0)
            
        if(SP[1] == 0):
            stockPrice_error = globalheader.STOCK_PRICE_UNAVAILABLE
            return optionPrice_error,SP[1]
        else:
            sep = ','
            SP[1] = SP[1].split(sep, 1)[0]
            stockPrice_Success = globalheader.Success
            return stockPrice_Success,(float)(SP[1])

#ConvertLst_Dict(lst) return converted list to dict
    #input - list
    #output - dict
def ConvertLst_Dict(lst):
    it = iter(lst) 
    res_dct = dict(zip(it, it))
    return res_dct

#getOpenInterest(Symbol,exp_date,strikeprice,date,contracttype) return extract open interestfrom row cell data  
    #input
        #symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #strike price - option strike price
        #date - trading date
        #contracttype - call or put
    #output 
        #openInterest_error - Success or STOCK_OPEN_INT_UNAVAILABLE
        #OI - open interest value           
def getOpenInterest(Symbol,exp_date,strikeprice,date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getOpenInterest Started')
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    OI_dict=OrderedDict()
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'Commonapi.dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                openinterest = [] 
                openinterest = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                openInterest = str(openinterest).split(data_seperator)
                if listOfStr[0] in openInterest:
                    openInterest = ConvertLst_Dict(openInterest)
                    OI = openInterest['OI']
                    OI = str(OI)
                    OI = OI.split(',')
                    openInterest['OI'] = OI[0]
                    if(openInterest['OI'] == 'U' or openInterest['OI'] == '' or openInterest['OI'] == ',' or openInterest['OI'] == "'" or openInterest['OI'] == ''):
                        openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOpenInterest Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getOpenInterest Error', openInterest_error)
                        return openInterest_error,OI_dict
                    else:
                        openInterest_error = globalheader.Success
                        OI = openInterest['OI']
##                        zipbObj = zip([date],[OI])
##                        dictofOI = dict(zipbObj)
##                        OI_dict[symbol]= dictofOI
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOpenInterest Ended')
                        return openInterest_error, OI
                else:
                    openInterest_error, OI =getopenInterest(openInterest)
                    if(openInterest_error == globalheader.Success):
##                        zipbObj = zip([date],[OI])
##                        dictofOI = dict(zipbObj)
##                        OI_dict[symbol]= dictofOI
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOpenInterest Ended')
                        return openInterest_error, OI
                    else:
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOpenInterest Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getOpenInterest Error', openInterest_error)
                        return openInterest_error, OI                      
                
    else:
        globalheader.logging.error('%s %d', 'dataapi.getdataframedata Error', call_error)
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOpenInterest Ended')
        return call_error,0
    
#getOptionVolume(Symbol,exp_date,strikeprice,date,contracttype) return extract option volume from row cell data  
    #input
        #symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #strike price - option strike price
        #date - trading date
        #contracttype - call or put
    #output 
        #optionVolume_error - Success or STOCK_OPT_VOLUME_UNAVAILABLE
        #OV - option volume value
def getOptionVolume(Symbol,exp_date,strikeprice,date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getOptionVolume Started')
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    OV_dict =OrderedDict()
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionVolume = [] 
                optionVolume = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                optionVolume = str(optionVolume).split(data_seperator)
                if listOfStr[4] in optionVolume:
                    optionVolume = ConvertLst_Dict(optionVolume)
                    OV = optionVolume['OV']
                    OV = str(OV)
                    OV = OV.split(',')
                    optionVolume['OV'] = OV[0]
                    if(optionVolume['OV'] == 'U' or optionVolume['OV'] == ',' or optionVolume['OV'] == '.' or optionVolume['OV'] == "'" or optionVolume['OV'] == ''):
                        optionVolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOptionVolume Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getoptionVolume Error', optionVolume_error)
                        return optionVolume_error,OV_dict
                    else:
                        optionVolume_error = globalheader.Success
                        OV = optionVolume['OV']
##                        zipbObj = zip([date],[OV])
##                        dictofOV = dict(zipbObj)
##                        OV_dict[symbol]= dictofOV
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOptionVolume Ended')
                        return optionVolume_error,OV
                else:
                    optionVolume_error, OV =getoptionVolume(optionVolume)
                    if(optionVolume_error == globalheader.Success):
##                        zipbObj = zip([date],[OV])
##                        dictofOV = dict(zipbObj)
##                        OV_dict[symbol]= dictofOV
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOptionVolume Ended')
                        return optionVolume_error,OV
                    else:
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOptionVolume Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getoptionVolume Error', optionVolume_error)
                        return optionVolume_error, OV       
    else:
        globalheader.logging.error('%s %d', 'dataapi.getdataframedata Error', call_error)
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOptionVolume Ended')
        return call_error,0


    
#getOptionPrice(Symbol,exp_date,strikeprice,date,contracttype) return extract option price from row cell data  
    #input
        #symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #strike price - option strike price
        #date - trading date
        #contracttype - call or put
    #output 
        #OptionPrice_error - Success or STOCK_OPT_PRICE_UNAVAILABLE
        #OP - Option Price value
def getOptionPrice(Symbol,exp_date,strikeprice,date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getOptionPrice Started')
    OP_dict = OrderedDict()
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionPrice = [] 
                optionPrice = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                optionPrice = str(optionPrice).split(data_seperator)
                if listOfStr[3] in optionPrice:
                    optionPrice = ConvertLst_Dict(optionPrice)
                    OP = optionPrice['OP']
                    OP = str(OP)
                    OP = OP.split(',')
                    optionPrice['OP'] = OP[0]
                    if(optionPrice['OP'] == 'U' or optionPrice['OP'] == '.' or optionPrice['OP'] == ',' or optionPrice['OP'] == "'" or optionPrice['OP'] == ''):
                        optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOptionPrice Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getOptionPrice Error', optionPrice_error)
                        return optionPrice_error,0
                    else:
                        optionPrice_error = globalheader.Success
                        OP = optionPrice['OP']
##                        zipbObj = zip([date],[OP])
##                        dictofOP = dict(zipbObj)
##                        OP_dict[symbol]= dictofOP
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOptionPrice Ended')
                        return optionPrice_error,OP
                else:
                    optionPrice_error, OP =getoptionPrice(optionPrice)
                    if(optionPrice_error == globalheader.Success):
##                        zipbObj = zip([date],[OP])
##                        dictofOP = dict(zipbObj)
##                        OP_dict[symbol]= dictofOP
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOptionPrice Ended')
                        return optionPrice_error,OP
                    else:
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOptionPrice Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getOptionPrice Error', optionPrice_error)
                        return optionPrice_error, OP         
    else:
        globalheader.logging.error('%s %d', 'dataapi.getdataframedata Error', call_error)
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOptionPrice Ended')
        return call_error,0


#getStockPrice(Symbol,exp_date,strikeprice,date,contracttype) return extract Stock Price from row cell data  
    #input
        #symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #strike price - option strike price
        #date - trading date
        #contracttype - call or put
    #output 
        #stockPrice_error - Success or STOCK_PRICE_UNAVAILABLE
        #SP - StockPrice value
def getStockPrice(Symbol,exp_date,strikeprice,date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getStockPrice Started')
    SP_dict = OrderedDict()
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockPrice = [] 
                stockPrice = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                stockPrice = str(stockPrice).split(data_seperator)
                if listOfStr[1] in stockPrice:
                    stockPrice = ConvertLst_Dict(stockPrice)
                    SP = stockPrice['SP']
                    SP = str(SP)
                    SP = OP.split(',')
                    stockPrice['SP'] = SP[0]
                    if(stockPrice['SP'] == 'U' or stockPrice['SP'] == '.' or stockPrice['SP'] == ',' or stockPrice['SP'] == "'" or stockPrice['SP'] == ''):
                        stockPrice_error = globalheader.STOCK_PRICE_UNAVAILABLE
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getStockPrice Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getStockPrice Error', stockPrice_error)
                        return stockPrice_error,0
                    else:
                        stockPrice_error = globalheader.Success
                        SP = stockPrice['SP']
##                        zipbObj = zip([date],[SP])
##                        dictofSP = dict(zipbObj)
##                        SP_dict[symbol]= dictofSP
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getStockPrice Ended')
                        return stockPrice_error,SP
                else:
                    stockPrice_error, SP =getstockPrice(stockPrice)
                    if(stockPrice_error == globalheader.Success):
##                        zipbObj = zip([date],[SP])
##                        dictofSP = dict(zipbObj)
##                        SP_dict[symbol]= dictofSP
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getStockPrice Ended')
                        return stockPrice_error,SP
                    else:
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getOptionVolume Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getoptionVolume Error', stockPrice_error)
                        return stockPrice_error, SP           
    else:
        
        globalheader.logging.error('%s %d', 'dataapi.getdataframedata Error', call_error)
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getStockPrice Ended')
        return call_error,0


#getStockVolume(Symbol,exp_date,strikeprice,date,contracttype) return extract stock volume from row cell data  
    #input
        #symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #strike price - option strike price
        #date - trading date
        #contracttype - call or put
    #output 
        #optionVolume_error - Success or STOCK_VOL_UNAVAILABLE
        #SV - stock volume value
def getStockVolume(Symbol,exp_date,strikeprice,date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getStockVolume Started')
    SV_dict = OrderedDict()
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockVolume = [] 
                stockVolume = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                stockVolume = str(stockVolume).split(data_seperator)
                if listOfStr[1] in stockVolume:
                    stockVolume = ConvertLst_Dict(stockVolume)
                    SV = stockVolume['SV']
                    SV = str(SV)
                    SV = SV.split(',')
                    stockVolume['SV'] = SV[0]
                    if(stockVolume['SV'] == 'U' or stockVolume['SV'] == '.' or stockVolume['SV'] == ',' or stockVolume['SV'] == "'" or stockVolume['SV'] == ''):
                        stockVolume_error = globalheader.STOCK_VOL_UNAVAILABLE
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getStockVolume Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getStockVolume Error', stockVolume_error)
                        return stockVolume_error,0
                    else:
                        stockVolume_error = globalheader.Success
                        SV = stockVolume['SV']
##                        zipbObj = zip([date],[SV])
##                        dictofSV = dict(zipbObj)
##                        SV_dict[symbol]= dictofSV
                        return stockVolume_error,SV
                else:
                    stockVolume_error, SV =getstockVolume(stockVolume)
                    if(stockVolume_error == globalheader.Success):
##                        zipbObj = zip([date],[SV])
##                        dictofSV = dict(zipbObj)
##                        SV_dict[symbol]= dictofSV
                        return stockVolume_error,SV
                    else:
                        if(globalheader.info == 1):
                            globalheader.logging.info('Commonapi.getStockVolume Ended')
                        globalheader.logging.error('%s %d', 'Commonapi.getStockVolume Error', stockVolume_error)
                        return stockVolume_error, SV           
    else:
        globalheader.logging.error('%s %d', 'dataapi.getdataframedata Error', call_error)

        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getStockVolume Ended')
        return call_error,0

#processdatawrite_ocsv(oCSVOIJumpFile,getNumberColsData,Sym_bol,exp_date,strikePrice,contracttype,date) writes the num of trading days column data to local output jump in OI or OV csv file  
    #input
        #Sym_bol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #strike price - option strike price
        #date - trading date
        #contracttype - call or put
        #getNumberColsData - num of trading days
        #oCSVOIJumpFile - local output csv file
    #output 
        #call_error - Success or standard header error
def processdatawrite_ocsv(oCSVOIJumpFile,getNumberColsData,Sym_bol,exp_date,strikePrice,contracttype,date):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.processdatawrite_ocsv Started')
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Sym_bol,exp_date,strikePrice,date,contracttype)
    globalheader.logging.error('%s %d', 'dataapi.getdataframedata Success', call_error)
    if(call_error == globalheader.Success):
        Symbol =[]
        Symbol = [str(symbol)]
        for row_index in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[row_index]):
                if(countCols == getNumberColsData):
                    dataapi.processColEqual(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol)
                    if(globalheader.info == 1):
                        globalheader.logging.info('Commonapi.processdatawrite_ocsv Ended')
                    return call_error
                elif(countCols > getNumberColsData and countCols != getNumberColsData ):
                    dataapi.processColGreater(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol)
                    if(globalheader.info == 1):
                        globalheader.logging.info('Commonapi.processdatawrite_ocsv Ended')
                    return call_error
                else:
                    dataapi.processColLess(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol)
                    if(globalheader.info == 1):
                        globalheader.logging.info('Commonapi.processdatawrite_ocsv Ended')
                    return call_error 
    else:
        globalheader.logging.error('%s %d', 'dataapi.getdataframedata Error', call_error)
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.processdatawrite_ocsv Ended')
        return call_error

#getmoneyinv(Symbol,exp_date,contracttype) is a wrapper function which calls dataapi.getmoneyInv which return  2d dict of money investment of call or put of stock option exp date   
    #input
        #Sym_bol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 2d dict of money investment of a option exp date of call or put
def getmoneyinv(Symbol,exp_date,contracttype):
    call_error, moneyinv_dict = dataapi.getmoneyInv(Symbol,exp_date,contracttype)
    return call_error,moneyinv_dict

#getAllmoneyinv(Symbol,contracttype) is a wrapper function which calls dataapi.getAllmoneyInv which return  3d dict of money investment of call or put of stock all option exp date of a stock  
    #input
        #Symbol - stock symbol
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 3d dict of money investment of all option exp date of call or put of a stock
def getAllmoneyinv(Symbol,contracttype):
    call_error, moneyinv_dict = dataapi.getAllmoneyInv(Symbol,contracttype)
    return call_error,moneyinv_dict

# getAllMaxPain(Symbol,contracttype) is a wrapper function which calls dataapi.getAllMaxPain which return  3d dict of max pain of call or put of stock all option exp date of a stock  
    #input
        #Symbol - stock symbol
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #maxpain_dict - 3d dict of max pain of all option exp date of call or put of a stock       
def getAllMaxPain(Symbol,contracttype):
    call_error, maxpain_dict = dataapi.getAllMaxPain(Symbol,contracttype)
    return call_error,maxpain_dict

# getMaxPain(Symbol,exp_date,contracttype) is a wrapper function which calls dataapi.getMaxPain which return  2d dict of max pain of call or put of stock a option exp date of a stock  
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #maxpain_dict - 2d dict of max pain of a option exp date of call or put of a stock    
def getMaxPain(Symbol,exp_date,contracttype):
    call_error, maxpain_dict = dataapi.getMaxPain(Symbol,exp_date,contracttype)
    return call_error,maxpain_dict

#getmoneyInvExpDateAllData(Symbol,exp_date,contracttype) is a wrapper function which calls dataapi.getmoneyInvExpDateAllData which return  2d dict of money investment,2d dict of total money,in-the-money,out-of-the-money open interest
#in-the-money,out-of-the-money total money of call or put of stock option exp date   
    #input
        #Sym_bol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 2d dict of money investment of a option exp date of call or put
        #OTM_dict - 2d dict of in-the-money,out-of-the-money investment of a option exp date of call or put
        #OTMIO_dict - 2d dict of in-the-money,out-of-the-money open interest of a option exp date of call or put
        #TM_dict - 2d dict of total money investment of a option exp date of call or put
def getmoneyInvExpDateAllData(Symbol,exp_date,contracttype):
    call_error,moneyinv_dict,OITM_dict,OTMOI_dict,TM_dict = dataapi.getmoneyInvExpDateAllData(Symbol,exp_date,contracttype)
    return call_error,moneyinv_dict,OITM_dict,OTMOI_dict,TM_dict

#getmoneyInvExpDateAllData(Symbol,exp_date,contracttype) is a wrapper function which calls dataapi.getmoneyInvExpDateAllData which return  3d dict of money investment,2d dict of total money,in-the-money,out-of-the-money open interest
#in-the-money,out-of-the-money total money of call or put of all stock option exp date   
    #input
        #Sym_bol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
    #output 
        #call_error - Success or standard header error
        #moneyinv_dict - 3d dict of money investment of a option exp date of call or put
        #OITM_dict - 3d dict of in-the-money,out-of-the-money investment of all option exp date of call or put
        #OTMOI_dict - 3d dict of in-the-money,out-of-the-money open interest of all option exp date of call or put
        #TM_dict - 3d dict of total money investment of all option exp date of call or put
def getmoneyInvAllExpDateAllData(Symbol,contracttype):
    call_error,moneyinv_dict,OITM_dict,OTMOI_dict,TM_dict = dataapi.getmoneyInvAllExpDateAllData(Symbol,contracttype)
    return call_error,moneyinv_dict,OITM_dict,OTMOI_dict,TM_dict


#getOpenInterestData(Symbol,exp_date,date,contracttype) returns open interest dict of all strike price present in requested exp date in existing trading day of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
    #output 
        #call_error - Success or standard header error
        #OI_dict - 2d dict of all open interest of a option exp date of call or put of a trading date
        
def getOpenInterestData(Symbol,exp_date,date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getOpenInterestData Started')
    iCSVFilename = dataapi.getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if os.path.exists(iCSVFilename):
        stockExpDateList  =[]                
        stockExpDateList = dataapi.getExpDatesListFromCSV(iCSVFilename)
        if exp_date in stockExpDateList:
            index = stockExpDateList.index(exp_date)
            expdate = stockExpDateList[index]
            strikePriceList = []
            strikePriceList = dataapi.strikePricesFromCSV(expdate,iCSVFilename)
            call_error,OI = dataapi.getOIdata(Symbol,exp_date,date,contracttype,strikePriceList)
            if(call_error == globalheader.Success):
                OI_dict=OrderedDict()
                zipbObj = zip(strikePriceList,OI)
                dictofOI = OrderedDict(zipbObj)
                OI_dict[date]= dictofOI
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getOpenInterestData Ended')
                return call_error,OI_dict                            
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getOpenInterestData Ended')
        
                return call_error,0
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOpenInterestData Ended')
        globalheader.logging.error('%s %d', 'dataapi.getOpenInterestData Error', call_error)

        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0


#getgetOptionVolumeData(Symbol,exp_date,date,contracttype) returns option volume dict of all strike price present in requested exp date in existing trading day of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
    #output 
        #call_error - Success or standard header error
        #OV_dict - 2d dict of all option volume of a option exp date of call or put of a trading date
    
def getOptionVolumeData(Symbol,exp_date,date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getOptionVolumeData Started')
    iCSVFilename = dataapi.getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if os.path.exists(iCSVFilename):
        stockExpDateList  =[]                
        stockExpDateList = dataapi.getExpDatesListFromCSV(iCSVFilename)
        if exp_date in stockExpDateList:
            index = stockExpDateList.index(exp_date)
            expdate = stockExpDateList[index]
            strikePriceList = []
            strikePriceList = dataapi.strikePricesFromCSV(expdate,iCSVFilename)
            call_error,OV = dataapi.getOVdata(Symbol,exp_date,date,contracttype,strikePriceList)
            if(call_error == globalheader.Success):
                OV_dict=OrderedDict()
                zipbObj = zip(strikePriceList,OV)
                dictofOV = OrderedDict(zipbObj)
                OV_dict[date]= dictofOV
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getOptionVolumeData Ended')
                return call_error,OV_dict                
            
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getOptionVolumeData Ended')
                return call_error,0
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOptionVolumeData Ended')
        globalheader.logging.error('%s %d', 'dataapi.getOptionVolumeData Error', call_error)

        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0


#getOptionPriceData(Symbol,exp_date,date,contracttype) returns option PRICE dict of all strike price present in requested exp date in existing trading day of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
    #output 
        #call_error - Success or standard header error
        #OV_dict - 2d dict of all option PRICE of a option exp date of call or put of a trading date
    
def getOptionPriceData(Symbol,exp_date,date,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOptionPriceData Started')
    iCSVFilename = dataapi.getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if os.path.exists(iCSVFilename):
        stockExpDateList  =[]                
        stockExpDateList = dataapi.getExpDatesListFromCSV(iCSVFilename)
        if exp_date in stockExpDateList:
            index = stockExpDateList.index(exp_date)
            expdate = stockExpDateList[index]
            strikePriceList = []
            strikePriceList = dataapi.strikePricesFromCSV(expdate,iCSVFilename)
            call_error,OP = dataapi.getOPdata(Symbol,exp_date,date,contracttype,strikePriceList)
            if(call_error == globalheader.Success):
                OP_dict=OrderedDict()
                zipbObj = zip(strikePriceList,OP)
                dictofOP = OrderedDict(zipbObj)
                OP_dict[date]= dictofOP
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getOptionPriceData Ended')
                return call_error,OP_dict                
            
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getOptionPriceData Ended')
                return call_error,0
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOptionPriceData Ended')
        globalheader.logging.error('%s %d', 'dataapi.getOptionPriceData Error', call_error)

        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0


#getstockPriceData(Symbol,exp_date,date,contracttype) returns stock PRICE dict of all strike price present in requested exp date in existing trading day of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
    #output 
        #call_error - Success or standard header error
        #SP_dict - 2d dict of all stock PRICE of a option exp date of call or put of a trading date
def getstockPriceData(Symbol,exp_date,date,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getstockPriceData Started')
    iCSVFilename = dataapi.getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if os.path.exists(iCSVFilename):
        stockExpDateList  =[]                
        stockExpDateList = dataapi.getExpDatesListFromCSV(iCSVFilename)
        if exp_date in stockExpDateList:
            index = stockExpDateList.index(exp_date)
            expdate = stockExpDateList[index]
            strikePriceList = []
            strikePriceList = dataapi.strikePricesFromCSV(expdate,iCSVFilename)
            call_error,SP = dataapi.getSPdata(Symbol,exp_date,date,contracttype,strikePriceList)
            if(call_error == globalheader.Success):
                SP_dict=OrderedDict()
                zipbObj = zip(strikePriceList,SP)
                dictofSP = OrderedDict(zipbObj)
                SP_dict[date]= dictofSP
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getstockPriceData Ended')
                return call_error,SP_dict                
            
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getstockPriceData Ended')
                return call_error,0
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getstockPriceData Ended')
        globalheader.logging.error('%s %d', 'dataapi.getstockPriceData Error', call_error)

        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0

#getstockVolumeData(Symbol,exp_date,date,contracttype) returns stock volume dict of all strike price present in requested exp date in existing trading day of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
    #output 
        #call_error - Success or standard header error
        #SV_dict - 2d dict of all stock volume of a option exp date of call or put of a trading date
def getstockVolumeData(Symbol,exp_date,date,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getstockVolumeData Started')
    iCSVFilename = dataapi.getStockCSVFile(contracttype,Symbol,csvDataFilePath)
    if os.path.exists(iCSVFilename):
        stockExpDateList  =[]                
        stockExpDateList = dataapi.getExpDatesListFromCSV(iCSVFilename)
        if exp_date in stockExpDateList:
            index = stockExpDateList.index(exp_date)
            expdate = stockExpDateList[index]
            strikePriceList = []
            strikePriceList = dataapi.strikePricesFromCSV(expdate,iCSVFilename)
            call_error,SV = dataapi.getSVdata(Symbol,exp_date,date,contracttype,strikePriceList)
            if(call_error == globalheader.Success):
                SV_dict=OrderedDict()
                zipbObj = zip(strikePriceList,SV)
                dictofSV = OrderedDict(zipbObj)
                SV_dict[date]= dictofSV
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getstockVolumeData Ended')
                return call_error,SV_dict                
            
            else:
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getstockVolumeData Ended')
                return call_error,0
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getstockVolumeData Ended')
        globalheader.logging.error('%s %d', 'dataapi.getstockVolumeData Error', call_error)
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0

#getOpenInterestDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype) returns open interest dict of a strike price present in requested exp date in requested trading day range of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
        #duration_range - number of trading days
    #output 
        #call_error - Success or standard header error
        #OI_dict - 2d dict of all open interest of a option exp date of call or put of trading date range
def getOpenInterestDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getOpenInterestDataRange Started')
    OI_dict=OrderedDict()
    dateheader = []
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    len_of_cols = len(csvDateHeaderlist)
    col = len_of_cols - duration_range -1
    if(col > duration_range):
        if(countcols > duration_range):
            duration_range = duration_range
        else:
            duration_range = countcols
    else:
        duration_range = col
        
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                openinterest_list = []                               
                for j in range(0,duration_range):
                    openinterest = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    openInterest = str(openinterest).split(data_seperator)
                    dateheader.append(csvDateHeaderlist[countcols])
                    if listOfStr[0] in openInterest:
                        openInterest = ConvertLst_Dict(openInterest)
                        OI = openInterest['OI']
                        OI = str(OI)
                        OI = OI.split(',')
                        openInterest['OI'] = OI[0]
                        if(openInterest['OI'] == 'U' or openInterest['OI'] == '' or openInterest['OI'] == ',' or openInterest['OI'] == "'" or openInterest['OI'] == ''):
                            value = (int)(0)
                            openinterest_list.append(openInterest['OI'])
                        else:
                            openinterest_list.append(openInterest['OI'])            
                    else:
                        call_error, OI =getopenInterest(openInterest)
                        if(call_error == globalheader.STOCK_OPEN_INT_UNAVAILABLE):
                            value = (int)(0)
                            OI = value
                            openinterest_list.append(OI)
                            call_error = globalheader.Success
                        else:
                            openinterest_list.append(OI)
                            call_error = globalheader.Success
                    countcols -= 1
                zipbObj = zip(dateheader,openinterest_list)
                dictofOI = OrderedDict()(zipbObj)
                OI_dict[symbol]= dictofOI
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getOpenInterestDataRange Ended')
                return call_error,OI_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOpenInterestDataRange Ended')
        globalheader.logging.error('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0

#getOptionVolumeDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype) returns option volume dict of a strike price present in requested exp date in requested trading day range of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
        #duration_range - number of trading days
    #output 
        #call_error - Success or standard header error
        #OV_dict - 2d dict of all option volume of a option exp date of call or put of a trading date
def getOptionVolumeDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    if(globalheader.info == 1):
        globalheader.logging.info('Commonapi.getOptionVolumeDataRange Started')
    OV_dict=OrderedDict()
    dateheader = []
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    len_of_cols = len(csvDateHeaderlist)
    col = len_of_cols - duration_range -1
    if(col > duration_range):
        if(countcols > duration_range):
            duration_range = duration_range
        else:
            duration_range = countcols
    else:
        duration_range = col
        
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)

        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionVolume_list = []
                        
                for j in range(0,duration_range):
                    optionVolume = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[countcols])
                    optionVolume = str(optionVolume).split(data_seperator)
                    if listOfStr[4] in optionVolume:
                        optionVolume = ConvertLst_Dict(optionVolume)
                        OV = optionVolume['OV']
                        OV = str(OV)
                        OV = OV.split(',')
                        optionVolume['OV'] = OV[0]
                        if(optionVolume['OV'] == 'U' or optionVolume['OV'] == ',' or optionVolume['OV'] == '.' or optionVolume['OV'] == "'" or optionVolume['OV'] == ''):
                            value = (int)(0)
                            optionVolume_list.append(value)
                        else:
                            optionVolume_list.append(optionVolume['OV'])            
                    else:
                        call_error, OV =getoptionVolume(optionVolume)
                        if(call_error == globalheader.STOCK_OPTION_VOLUME_UNAVAILABLE):
                            value = (int)(0)
                            OV = value
                            optionVolume_list.append(OV)
                            call_error = globalheader.Success
                        else:
                            optionVolume_list.append(OV)
                            call_error = globalheader.Success
                    countcols -= 1
                zipbObj = zip(dateheader,optionVolume_list)
                dictofOI = OrderedDict(zipbObj)
                OV_dict[symbol]= dictofOV
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getOptionVolumeDataRange Ended')   
                return call_error,OV_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOptionVolumeDataRange Ended')
        globalheader.logging.info('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0

#getOptionPriceDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype) returns option price dict of a strike price present in requested exp date in requested trading day range of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
        #duration_range - number of trading days
    #output 
        #call_error - Success or standard header error
        #OP_dict - 2d dict of all option price of a option exp date of call or put of trading date range
    
def getOptionPriceDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getOptionPriceDataRange Started')
    OP_dict=OrderedDict()
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    len_of_cols = len(csvDateHeaderlist)
    col = len_of_cols - duration_range -1
    if(col > duration_range):
        if(countcols > duration_range):
            duration_range = duration_range
        else:
            duration_range = countcols
    else:
        duration_range = col
        
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionPrice_list = []
                
                for j in range(0,duration_range):
                    optionPrice = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[countcols])
                    optionPrice = str(optionPrice).split(data_seperator)
                    if listOfStr[3] in optionPrice:
                        optionPrice = ConvertLst_Dict(optionPrice)
                        OP = optionPrice['OP']
                        OP = str(OP)
                        OP = OP.split(',')
                        optionPrice['OP'] = OP[0]
                        if(optionPrice['OP'] == 'U' or optionPrice['OP'] == '.' or optionPrice['OP'] == ',' or optionPrice['OP'] == "'" or optionPrice['OP'] == ''):
                            value = (int)(0)
                            optionPrice_list.append(value)
                        else:
                            optionPrice_list.append(optionPrice['OP'])            
                    else:
                        call_error, OP =getoptionPrice(optionPrice)
                        if(call_error == globalheader.STOCK_OPTION_PRICE_UNAVAILABLE):
                            value = (int)(0)
                            OV = value
                            optionPrice_list.append(OP)
                            call_error = globalheader.Success
                        else:
                            optionPrice_list.append(OP)
                            call_error = globalheader.Success
                    countcols -= 1

                zipbObj = zip(dateheader,optionPrice_list)
                dictofOP = OrderedDict(zipbObj)
                OP_dict[symbol]= dictofOP
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getOptionVolumeDataRange Ended')
                return call_error,OP_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.OptionPriceDataRange Ended')
        globalheader.logging.info('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0

#stockPriceDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype) returns open interest dict of a strike price present in requested exp date in requested trading day range of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
        #duration_range - number of trading days
    #output 
        #call_error - Success or standard header error
        #SP_dict - 2d dict of all open interest of a option exp date of call or put of trading date range
# return AllstockPriceData of particular exp date
def getstockPriceDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getstockPriceDataRange Started')
    SP_dict=OrderedDict()
    dateheader = []
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    len_of_cols = len(csvDateHeaderlist)
    col = len_of_cols - duration_range -1
    if(col > duration_range):
        if(countcols > duration_range):
            duration_range = duration_range
        else:
            duration_range = countcols
    else:
        duration_range = col
        
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockPrice_list = []
                
                for j in range(0,duration_range):
                    stockPrice = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[countcols])
                    stockPrice = str(stockPrice).split(data_seperator)
                    if listOfStr[1] in stockPrice:
                        stockPrice = ConvertLst_Dict(stockPrice)
                        SP = stockPrice['SP']
                        SP = str(SP)
                        SP = OP.split(',')
                        stockPrice['SP'] = SP[0]
                        if(stockPrice['SP'] == 'U' or stockPrice['SP'] == '.' or stockPrice['SP'] == ',' or stockPrice['SP'] == "'" or stockPrice['SP'] == ''):
                            value = (int)(0)
                            stockPrice_list.append(stockPrice['SP'])
                        else:
                            stockPrice_list.append(stockPrice['SP'])            
                    else:
                        call_error, SP =getoptionPrice(stockPrice)
                        if(call_error == globalheader.STOCK_PRICE_UNAVAILABLE):
                            value = (int)(0)
                            SP = value
                            stockPrice_list.append(SP)
                            call_error = globalheader.Success
                        else:
                            stockPrice_list.append(SP)
                            call_error = globalheader.Success
                    countcols -= 1

                zipbObj = zip(dateheader,stockPrice_list)
                dictofSP = OrderedDict(zipbObj)
                SP_dict[symbol]= dictofSP
                if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getstockPriceDataRange Ended')
                return call_error,SP_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getstockPriceDataRange Ended')
        globalheader.logging.info('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0


#getstockVolumeDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype) returns open interest dict of a strike price present in requested exp date in requested trading day range of a stock symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #date - trading day
        #duration_range - number of trading days
    #output 
        #call_error - Success or standard header error
        #SV_dict - 2d dict of all open interest of a option exp date of call or put of trading date range
def getstockVolumeDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getstockVolumeDataRange Started')
    SV_dict=OrderedDict()
    dateheader = []
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    len_of_cols = len(csvDateHeaderlist)
    col = len_of_cols - duration_range -1
    if(col > duration_range):
        if(countcols > duration_range):
            duration_range = duration_range
        else:
            duration_range = countcols
    else:
        duration_range = col
        
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockVolume_list = []
                
                for j in range(0,duration_range):
                    stockVolume = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[countcols])
                    stockVolume = str(stockVolume).split(data_seperator)
                    if listOfStr[2] in stockVolume:
                        stockVolume = ConvertLst_Dict(stockVolume)
                        SV = stockVolume['SV']
                        SV = str(SV)
                        SV = SV.split(',')
                        stockVolume['SV'] = SV[0]
                        if(stockVolume['SV'] == 'U' or stockVolume['SV'] == '.' or stockVolume['SV'] == ',' or stockVolume['SV'] == "'" or stockVolume['SV'] == ''):
                            value = (int)(0)
                            stockVolume_list.append(value)
                        else:
                            stockVolume_list.append(stockVolume['SV'])
            
                    else:
                        call_error, SV =getstockVolume(stockVolume)
                        stockVolume_list.append(SV)
                        if(call_error == globalheader.STOCK_VOL_UNAVAILABLE):
                            value = (int)(0)
                            SV = value
                            stockVolume_list.append(SV)
                            call_error = globalheader.Success
                        else:
                            stockVolume_list.append(SV)
                            call_error = globalheader.Success
                    countcols -= 1

                zipbObj = zip(dateheader,stockVolume_list)
                dictofSP = OrderedDict(zipbObj)
                SV_dict[symbol]= dictofSV
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getstockVolumeDataRange Ended')
                return call_error,SV_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getstockVolumeDataRange Ended')
        globalheader.logging.info('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0

#getAllOpenInterestData(Symbol, exp_date, strikeprice,contracttype) returns open interest dict of a strike price of requested exp date in all existingtrading day  of a stock option symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #strike price  - option strike price
    #output 
        #call_error - Success or standard header error
        #OI_dict - 2d dict of all open interest of a option exp date of call or put of existing trading dates
def getAllOpenInterestData(Symbol, exp_date, strikeprice,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllOpenInterestData Started')
    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    OI_dict=OrderedDict()

    dateheader =[]
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                openinterest_list = []
                cols = totalcols
                for j in range(0,totalcols):
                    dateheader.append(csvDateHeaderlist[cols])                    
                    openinterest = dataapi.getrowdata(i,cols,Symbol,contracttype)
                    openInterest = str(openinterest).split(data_seperator)
                    if listOfStr[0] in openInterest:
                        openInterest = ConvertLst_Dict(openInterest)
                        OI = openInterest['OI']
                        OI = str(OI)
                        OI = OI.split(',')
                        openInterest['OI'] = OI[0]
                        if(openInterest['OI'] == 'U' or openInterest['OI'] == '' or openInterest['OI'] == ',' or openInterest['OI'] == "'" or openInterest['OI'] == ''):
                            value = (int)(0)
                            openinterest_list.append(value)
                        else:
                            openinterest_list.append(openInterest['OI'])
            
                    else:
                        call_error, OI =getopenInterest(openInterest)
                        if(call_error == globalheader.STOCK_OPEN_INT_UNAVAILABLE):
                            value = (int)(0)
                            OI = value
                            openinterest_list.append(OI)
                            call_error = globalheader.Success
                        else:
                            openinterest_list.append(OI)
                            call_error = globalheader.Success
                            
                    cols -= 1
                zipbObj = zip(dateheader,openinterest_list)
                dictofOI = OrderedDict(zipbObj)
                OI_dict[strikeprice]= dictofOI
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getAllOpenInterestData Ended')
                return call_error,OI_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllOpenInterestData Ended')
        globalheader.logging.info('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0

#getAllOptionVolumeData(Symbol, exp_date, strikeprice,contracttype) returns option volume dict of a strike price of requested exp date in all existingtrading day  of a stock option symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #strike price  - option strike price
    #output 
        #call_error - Success or standard header error
        #OV_dict - 2d dict of all option volumeof a option exp date of call or put of existing trading dates
def getAllOptionVolumeData(Symbol, exp_date, strikeprice,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllOptionVolumeData Started')
    OV_dict=OrderedDict()
    
    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    dateheader =[]
    
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionVolume_list = []
                cols = totalscols
                for j in range(0,totalcols):
                    optionVolume = dataapi.getrowdata(i,cols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[cols])                    
                    optionVolume = str(optionVolume).split(data_seperator)
                    if listOfStr[4] in optionVolume:
                        optionolume = ConvertLst_Dict(optionVolume)
                        OV = optionVolume['OV']
                        OV = str(OV)
                        OV = OV.split(',')
                        optionVolume['OV'] = OV[0]
                        if(optionVolume['OV'] == 'U' or optionVolume['OV'] == ',' or optionVolume['OV'] == '.' or optionVolume['OV'] == "'" or optionVolume['OV'] == ''):
                            value = (int)(0)
                            optionVolume_list.append(value)
                        else:
                            optionVolume_list.append(optionVolume['OV'])
            
                    else:
                        call_error, OV =getoptionVolume(optionVolume)
                        if(call_error == globalheader.STOCK_OPTION_VOLUME_UNAVAILABLE):
                            value = (int)(0)
                            OV = value
                            optionVolume_list.append(OV)
                            call_error = globalheader.Success
                        else:
                            call_error = globalheader.Success
                            optionVolume_list.append(OV)
                    cols -= 1
                zipbObj = zip(dateheader,optionVolume_list)
                dictofOI = OrderedDict(zipbObj)
                OV_dict[symbol]= dictofOV
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getAllOptionVolumeData Ended')    
                return call_error,OV_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllOptionVolumeData Ended')
        globalheader.logging.info('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0

    
#getAllOptionPriceData(Symbol, exp_date, strikeprice,contracttype) returns open interest dict of a strike price of requested exp date in all existingtrading day  of a stock option symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #strike price  - option strike price
    #output 
        #call_error - Success or standard header error
        #OP_dict - 2d dict of alloption price of a option exp date of call or put of existing trading dates
    
def getAllOptionPriceData(Symbol, exp_date, strikeprice,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllOptionPriceData Started')
    OP_dict=OrderedDict()

    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    dateheader =[]
            
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionPrice_list = []
                cols = totalscols
                for i in range(1,totalcols):
                    optionPrice = dataapi.getrowdata(i,cols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[cols])                    
                    optionPrice = str(optionPrice).split(data_seperator)
                    if listOfStr[3] in optionPrice:
                        optionPrice = ConvertLst_Dict(optionPrice)
                        OP = optionPrice['OP']
                        OP = str(OP)
                        OP = OP.split(',')
                        optionPrice['OP'] = OP[0]
                        if(optionPrice['OP'] == 'U' or optionPrice['OP'] == '.' or optionPrice['OP'] == ',' or optionPrice['OP'] == "'" or optionPrice['OP'] == ''):
                            value = (int)(0)
                            optionPrice_list.append(value)
                        else:
                            optionPrice_list.append(optionPrice['OP'])
            
                    else:
                        call_error, OP =getoptionPrice(optionPrice)
                        if(call_error == globalheader.STOCK_OPTION_PRICE_UNAVAILABLE):
                            value = (int)(0)
                            OP = value
                            optionPrice_list.append(OP)
                            call_error = globalheader.Success
                        else:
                            call_error = globalheader.Success
                            optionPrice_list.append(OP)
                    cols -= 1
                zipbObj = zip(dateheader,optionPrice_list)
                dictofOP = OrderedDict(zipbObj)
                OP_dict[symbol]= dictofOP
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getAllOptionPriceData Ended')
                return call_error,OP_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllOptionPriceData Ended')
        globalheader.logging.info('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0

    
#getAllstockPriceData(Symbol, exp_date, strikeprice,contracttype) returns open interest dict of a strike price of requested exp date in all existingtrading day  of a stock option symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #strike price - option strike price
    #output 
        #call_error - Success or standard header error
        #SP_dict - 2d dict of stock price of a option exp date of call or put of existing trading date
    
def getAllstockPriceData(Symbol, exp_date, strikeprice,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllstockPriceData Started')
    SP_dict=OrderedDict()

    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    dateheader =[]
        
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockPrice_list = []
                cols = totalscols
                for i in range(0,totalcols):
                    stockPrice = dataapi.getrowdata(i,cols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[cols])                    
                    stockPrice = str(stockPrice).split(data_seperator)
                    if listOfStr[1] in stockPrice:
                        stockPrice = ConvertLst_Dict(stockPrice)
                        SP = stockPrice['SP']
                        SP = str(SP)
                        SP = OP.split(',')
                        stockPrice['SP'] = SP[0]
                        if(stockPrice['SP'] == 'U' or stockPrice['SP'] == '.' or stockPrice['SP'] == ',' or stockPrice['SP'] == "'" or stockPrice['SP'] == ''):
                            value = (int)(0)
                            stockPrice_list.append(value)
                        else:
                            stockPrice_list.append(stockPrice['SP'])
            
                    else:
                        call_error, SP =getoptionPrice(stockPrice)
                        if(call_error == globalheader.STOCK_PRICE_UNAVAILABLE):
                            value = (int)(0)
                            SP = value
                            optionPrice_list.append(SP)
                            call_error = globalheader.Success
                        else:
                            call_error = globalheader.Success
                            stockPrice_list.append(SP)
                cols -= 1
                zipbObj = zip(dateheader,stockPrice_list)
                dictofSP = OrderedDict(zipbObj)
                SP_dict[symbol]= dictofSP
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getAllstockPriceData Ended')
                return call_error,SP_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllstockPriceData Ended')
        globalheader.logging.info('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0

#getAllstockVolumeData(Symbol, exp_date, strikeprice,contracttype) returns stock volume dict of a strike price present in requested exp date in all existingtrading day  of a stock option symbol 
    #input
        #Symbol - stock symbol
        #exp_date - 'O11720'(MMDDYY)
        #contracttype - call or put
        #strikeprice - option strike price
    #output 
        #call_error - Success or standard header error
        #SV_dict - 2d dict of all stock volume of a option exp date of call or put of existing trading date 

def getAllstockVolumeData(Symbol, exp_date, strikeprice,contracttype):
    if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllstockVolumeData Started')
    SV_dict=OrderedDict()
    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    dateheader =[]
            
    if(call_error == globalheader.Success):
        if(globalheader.info == 1):
            globalheader.logging.info('%s %d', 'dataapi.getdataframedata Success', call_error)
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockVolume_list = []
                cols = totalscols
                for i in range(0,totalcols):
                    stockVolume = dataapi.getrowdata(i,cols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[cols])                    
                    stockVolume = str(stockVolume).split(data_seperator)
                    if listOfStr[2] in stockVolume:
                        stockVolume = ConvertLst_Dict(stockVolume)
                        SV = stockVolume['SV']
                        SV = str(SV)
                        SV = SV.split(',')
                        stockVolume['SV'] = SV[0]
                        if(stockVolume['SV'] == 'U' or stockVolume['SV'] == '.' or stockVolume['SV'] == ',' or stockVolume['SV'] == "'" or stockVolume['SV'] == ''):
                            value = (int)(0)
                            stockVolume_list.append(value)
                        else:
                            stockVolume_list.append(stockVolume['SV'])
            
                    else:
                        call_error, SV =getstockVolume(stockVolume)
                        if(call_error == globalheader.STOCK_VOL_UNAVAILABLE):
                            value = (int)(0)
                            SV = value
                            stockVolume_list.append(SV)
                            call_error = globalheader.Success
                        else:
                            call_error = globalheader.Success
                            stockVolume_list.append(SV)
                    cols -= 1
                zipbObj = zip(dateheader,stockVolume_list)
                dictofSP = OrderedDict(zipbObj)
                SV_dict[symbol]= dictofSV
                if(globalheader.info == 1):
                    globalheader.logging.info('Commonapi.getAllstockVolumeData Ended')
                return call_error,SV_dict
    else:
        if(globalheader.info == 1):
            globalheader.logging.info('Commonapi.getAllstockVolumeData Ended')
        globalheader.logging.info('%s %d', 'dataapi.getdataframedata Error', call_error)

        return call_error,0
