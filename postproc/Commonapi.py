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

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

csv.field_size_limit(sys.maxsize)
contractType =['CALL','PUT']
listOfStr = ["OI", "SP" , "SV" , "OP" , "OV"]
debug = 0
info = 0
data_seperator =':'
name_seperator = ':'

csvDataFilePath = './../datacolls/output/'


#declare enums for CALL,PUT
class Contracttype(enum.Enum):
    CALL = 0
    PUT = 1

#return output stockCsvfile
def createoFile(symbol,ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+symbol+'_'+today+'.xlsx'
    return stockCsvfilename

#return output stockCsvfilename
def getoFile(symbol,ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+symbol+'_'+today+'.xlsx'
    return stockCsvfilename

#return extracted Expdate from row data
def getOptExpDateFromCSV(optionSymbol):
    symbol,date = optionSymbol.split('_')
    date = list(str(date))
    length = len(date)
    expdate = date[4]+date[5]+date[0]+date[1]+date[2]+date[3]
    return expdate

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
    
def getSymbol(Symbol,date,contracttype,strikeprice):
    optiontype = 0
    #print("Symbol in getsymbol,strikeprice,date  :",Symbol,strikeprice,date)
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
def removeDuplicateItems(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list

#return extracted strikeprice from row data
def getOptionStrikePrice(optionSymbol):
    n = 7
    symbol,strikeprice = optionSymbol.split('_')
    strikeprice  = list(str(strikeprice ))
    length = len(strikeprice )
    strikeprice= strikeprice[n:]
    strikeprice =''.join(strikeprice)
    return strikeprice

#return input stock csv file
def getInputFile(ifilename):       
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ifilename+'_'+today+'.csv'
    return stockCsvfilename

#return input stock csv file
def getInputfile(ifilename):       
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ifilename
    return stockCsvfilename
        
def extract(string, start=':'):
        return string[string.index(start)+1]


#return outout xl file 
def createoxlFile(ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+today+'.xlsx'
    return stockCsvfilename

#return outout OI jump csv file
def createOutputOIJumpFile(ofilename):
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+today+'.csv'
    return stockCsvfilename

#return generated datelist for jumpoi output csv file
def generateDateList(ofile,getNumberColsData):
    print("generateDateList(ofile,getNumberColsData):")
    today = date.today()
    dateListHeader = []
    header_list =[]
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
    print("generateDateList(ofile,getNumberColsData) success:")
    return dateListHeader


#write row datas to jumpOI/jumpOV output csv file        
def writeOIrOVtolocalCSV(ofile,rowData):
    if os.path.exists(ofile):
        with open(ofile, 'a') as ocsvfile:
            wr = csv.writer(ocsvfile,lineterminator='\r')
            for row in rowData:
                wr.writerow(row)
    else:
        with open(ofile, 'w') as ocsvfile:
            writer = csv.writer(ocsvfile)
            writer.writerow(['Symbol','YestOI','TodayOI','%Jump'])

#parse the row data
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
            
        
#return parsed option price from row data
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

#return parsed optionVolume from row data
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

#return parsed stock price from row data
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

#return parsed stock price from row data
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

#return converted list to dict        
def ConvertLst_Dict(lst):
    it = iter(lst) 
    res_dct = dict(zip(it, it))
    return res_dct
           
#return parsed option interest from row data
def getOpenInterest(Symbol,exp_date,strikeprice,date,contracttype):    
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    OI_dict=dict()
    if(call_error == globalheader.Success):
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                openinterest = [] 
                openinterest = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                #print("getOpenInterest openinterest is :",openinterest)
                openInterest = str(openinterest).split(data_seperator)
                if listOfStr[0] in openInterest:
                    openInterest = ConvertLst_Dict(openInterest)
                    if(openInterest['OI'] == 'U'):
                        openInterest_error = globalheader.STOCK_OPEN_INT_UNAVAILABLE
                        return openInterest_error,OI_dict
                    else:
                        openInterest_error = globalheader.Success
                        OI = openInterest['OI']
                        zipbObj = zip([date],[OI])
                        dictofOI = dict(zipbObj)
                        OI_dict[symbol]= dictofOI
                        return openInterest_error, OI
                else:
                    openInterest_error, OI =getopenInterest(openInterest)
                    if(openInterest_error == globalheader.Success):
                        zipbObj = zip([date],[OI])
                        dictofOI = dict(zipbObj)
                        OI_dict[symbol]= dictofOI
                        return openInterest_error, OI
                    else:
                       return openInterest_error, OI                      
                
    else: 
        return call_error,0
    

#return parsed option volume from row data
def getOptionVolume(Symbol,exp_date,strikeprice,date,contracttype):
    print("getOpenInterest date and strikeprice  is :",date,strikeprice)
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    OV_dict =dict()
    if(call_error == globalheader.Success):
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionVolume = [] 
                optionVolume = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                print("getOpenInterest openinterest is :",optionVolume)
                optionVolume = str(optionVolume).split(data_seperator)
                if listOfStr[4] in optionVolume:
                    optionVolume = ConvertLst_Dict(optionVolume)
                    if(optionVolume['OV'] == 'U'):
                        optionVolume_error = globalheader.STOCK_OPT_VOLUME_UNAVAILABLE
                        return optionVolume_error,OV_dict
                    else:
                        optionVolume_error = globalheader.Success
                        OV = optionVolume['OV']
                        zipbObj = zip([date],[OV])
                        dictofOV = dict(zipbObj)
                        OV_dict[symbol]= dictofOV
                        return optionVolume_error,OV
                else:
                    optionVolume_error, OV =getoptionVolume(optionVolume)
                    if(optionVolume_error == globalheader.Success):
                        zipbObj = zip([date],[OV])
                        dictofOV = dict(zipbObj)
                        OV_dict[symbol]= dictofOV
                        return optionVolume_error,OV
                    else:
                        return optionVolume_error, OV       
    else:
         return call_error,0


    
#return parsed option volume from row data
def getOptionPrice(Symbol,exp_date,strikeprice,date,contracttype):
    OP_dict = dict()
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    if(call_error == globalheader.Success):
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionPrice = [] 
                optionPrice = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                optionPrice = str(optionPrice).split(data_seperator)
                if listOfStr[3] in optionPrice:
                    optionPrice = ConvertLst_Dict(optionPrice)
                    if(optionPrice['OP'] == 'U'):
                        optionPrice_error = globalheader.STOCK_OPT_PRICE_UNAVAILABLE
                        return optionPrice_error,0
                    else:
                        optionPrice_error = globalheader.Success
                        OP = optionPrice['OP']
                        zipbObj = zip([date],[OP])
                        dictofOP = dict(zipbObj)
                        OP_dict[symbol]= dictofOP
                        return optionPrice_error,OP
                else:
                    optionPrice_error, OP =getoptionPrice(optionPrice)
                    if(optionPrice_error == globalheader.Success):
                        zipbObj = zip([date],[OP])
                        dictofOP = dict(zipbObj)
                        OP_dict[symbol]= dictofOP
                        return optionPrice_error,OP
                    else:
                        return optionPrice_error, OP         
    else:        
        return call_error,0

def getStockPrice(Symbol,exp_date,strikeprice,date,contracttype):
    SP_dict = dict()
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    if(call_error == globalheader.Success):
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockPrice = [] 
                stockPrice = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                stockPrice = str(stockPrice).split(data_seperator)
                if listOfStr[1] in stockPrice:
                    stockPrice = ConvertLst_Dict(stockPrice)
                    if(stockPrice['SP'] == 'U'):
                        stockPrice_error = globalheader.STOCK_PRICE_UNAVAILABLE
                        return stockPrice_error,0
                    else:
                        stockPrice_error = globalheader.Success
                        SP = stockPrice['SP']
##                        zipbObj = zip([date],[SP])
##                        dictofSP = dict(zipbObj)
##                        SP_dict[symbol]= dictofSP
                        return stockPrice_error,SP
                else:
                    stockPrice_error, SP =getstockPrice(stockPrice)
                    if(stockPrice_error == globalheader.Success):
##                        zipbObj = zip([date],[SP])
##                        dictofSP = dict(zipbObj)
##                        SP_dict[symbol]= dictofSP
                        return stockPrice_error,SP
                    else:
                        return stockPrice_error, SP           
    else:        
        return call_error,0

def getStockVolume(Symbol,exp_date,strikeprice,date,contracttype):
    SV_dict = dict()
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Symbol,exp_date,strikeprice,date,contracttype)
    if(call_error == globalheader.Success):
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockVolume = [] 
                stockVolume = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                stockVolume = str(stockVolume).split(data_seperator)
                if listOfStr[1] in stockVolume:
                    stockVolume = ConvertLst_Dict(stockVolume)
                    if(stockVolume['SV'] == 'U'):
                        stockVolume_error = globalheader.STOCK_VOL_UNAVAILABLE
                        return stockVolume_error,0
                    else:
                        stockVolume_error = globalheader.Success
                        SV = stockVolume['SV']
                        zipbObj = zip([date],[SV])
                        dictofSV = dict(zipbObj)
                        SV_dict[symbol]= dictofSV
                        return stockVolume_error,SV
                else:
                    stockVolume_error, SV =getstockVolume(stockVolume)
                    if(stockVolume_error == globalheader.Success):
                        zipbObj = zip([date],[SV])
                        dictofSV = dict(zipbObj)
                        SV_dict[symbol]= dictofSV
                        return stockVolume_error,SV
                    else:
                        return stockVolume_error, SV           
    else:        
        return call_error,0


def processdatawrite_ocsv(oCSVOIJumpFile,getNumberColsData,Sym_bol,exp_date,strikePrice,contracttype,date):
    call_error,CSVOptionSymbolList,symbol,countcols,csvDateHeaderlist,countCols = dataapi.getdataframedata(Sym_bol,exp_date,strikePrice,date,contracttype)
    if(call_error == globalheader.Success):
        Symbol =[]
        Symbol = [str(symbol)]
        for row_index in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[row_index]):
                if(countCols == getNumberColsData):
                    dataapi.processColEqual(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol)
                    return call_error
                elif(countCols > getNumberColsData and countCols != getNumberColsData ):
                    dataapi.processColGreater(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol)
                    return call_error
                else:
                    dataapi.processColLess(oCSVOIJumpFile,Symbol,row_index,getNumberColsData,contracttype,Sym_bol)
                    return call_error 
    else:
        return call_error
    
#money inv  of an EXP date of an symbol of optiontype    
def getmoneyinv(Symbol,exp_date,contracttype):
    call_error, moneyinv_dict = dataapi.getmoneyInv(Symbol,exp_date,contracttype)
    return call_error,moneyinv_dict

#money inv  of all EXP date of an symbol of optiontype    
def getAllmoneyinv(Symbol,contracttype):
    call_error, moneyinv_dict = dataapi.getAllmoneyInv(Symbol,contracttype)
    return call_error,moneyinv_dict
       
#max_pain of a ALL EXP date of an symbol of optiontype    
def getAllMaxPain(Symbol,contracttype):
    call_error, maxpain_dict = dataapi.getAllMaxPain(Symbol,contracttype)
    return call_error,maxpain_dict

#max_pain of a an EXP date of an symbol of optiontype    
def getMaxPain(Symbol,exp_date,contracttype):
    call_error, maxpain_dict = dataapi.getMaxPain(Symbol,exp_date,contracttype)
    return call_error,maxpain_dict       
        
def getAllOI(Symbol,contracttype):
    call_error, OI_dict = dataapi.getAllOI(Symbol,contracttype)
    return call_error,OI_dict

#money inv  of an EXP date of an symbol of optiontype
def getmoneyInvExpDateAllData(Symbol,exp_date,contracttype):
    call_error,moneyinv_dict,OTM_dict,OTMIO_dict,TM_dict = dataapi.getmoneyInvExpDateAllData(Symbol,exp_date,contracttype)
    return call_error,moneyinv_dict,OTM_dict,OTMIO_dict,TM_dict

#money inv  of all EXP date of an symbol of optiontype
def getmoneyInvAllExpDateAllData(Symbol,contracttype):
    call_error,moneyinv_dict,OTM_dict,OTMIO_dict,TM_dict = dataapi.getmoneyInvAllExpDateAllData(Symbol,contracttype)
    return call_error,moneyinv_dict,OTM_dict,OTMIO_dict,TM_dict

#returns dictioary of all OI data for a a particular date
def getOpenInterestData(Symbol,exp_date,date,contracttype):
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
                OI_dict=dict()
                zipbObj = zip(strikePriceList,OI)
                dictofOI = dict(zipbObj)
                OI_dict[date]= dictofOI
                return call_error,OI_dict                            
            else:
                return call_error,0
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0

def getOptionVolumeData(Symbol,exp_date,date,contracttype):
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
                OV_dict=dict()
                zipbObj = zip(strikePriceList,OV)
                dictofOV = dict(zipbObj)
                OV_dict[date]= dictofOV
                return call_error,OV_dict                
            
            else:
                return call_error,0
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0

def getOptionPriceData(Symbol,exp_date,date,contracttype):
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
                OP_dict=dict()
                zipbObj = zip(strikePriceList,OP)
                dictofOP = dict(zipbObj)
                OP_dict[date]= dictofOP
                return call_error,OP_dict                
            
            else:
                return call_error,0
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0

def getstockPriceData(Symbol,exp_date,date,contracttype):
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
                SP_dict=dict()
                zipbObj = zip(strikePriceList,SP)
                dictofSP = dict(zipbObj)
                SP_dict[date]= dictofSP
                return call_error,SP_dict                
            
            else:
                return call_error,0
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0

def getstockVolumeData(Symbol,exp_date,date,contracttype):
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
                SV_dict=dict()
                zipbObj = zip(strikePriceList,SV)
                dictofSV = dict(zipbObj)
                SV_dict[date]= dictofSV
                return call_error,SV_dict                
            
            else:
                return call_error,0
    else:
        call_error = globalheader.STOCK_CSV_DBASE_FILE_NOT_EXIST 
        return call_error,0

#  returns dictioary of all OI data for a particular date range
def getOpenInterestDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    OI_dict=dict()
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
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                openinterest_list = []                               
                for j in range(0,duration_range):
                    openinterest = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    openInterest = str(openinterest).split(data_seperator)
                    dateheader.append(csvDateHeaderlist[countcols])
                    if listOfStr[0] in openInterest:
                        openInterest = ConvertLst_Dict(openInterest)
                        if(openInterest['OI'] == 'U'):
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
                dictofOI = dict(zipbObj)
                OI_dict[symbol]= dictofOI

                return call_error,OI_dict
    else: 
        return call_error,0

# return AllOptionVolumeData of particular exp date
def getOptionVolumeDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    OV_dict=dict()
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
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionVolume_list = []
                        
                for j in range(0,duration_range):
                    optionVolume = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[countcols])
                    optionVolume = str(optionVolume).split(data_seperator)
                    if listOfStr[4] in optionVolume:
                        optionVolume = ConvertLst_Dict(optionVolume)
                        if(optionVolume['OV'] == 'U'):
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
                dictofOI = dict(zipbObj)
                OV_dict[symbol]= dictofOV
                    
                return call_error,OV_dict
    else: 
        return call_error,0

# return AllOptionPriceData of particular exp date
def getOptionPriceDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    OP_dict=dict()
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
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                optionPrice_list = []
                
                for j in range(0,duration_range):
                    optionPrice = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[countcols])
                    optionPrice = str(optionPrice).split(data_seperator)
                    if listOfStr[3] in optionPrice:
                        optionPrice = ConvertLst_Dict(optionPrice)
                        if(optionPrice['OP'] == 'U'):
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
                dictofOP = dict(zipbObj)
                OP_dict[symbol]= dictofOP

                return call_error,OP_dict
    else: 
        return call_error,0

# return AllstockPriceData of particular exp date
def getstockPriceDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    SP_dict=dict()
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
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockPrice_list = []
                
                for j in range(0,duration_range):
                    stockPrice = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[countcols])
                    stockPrice = str(stockPrice).split(data_seperator)
                    if listOfStr[1] in stockPrice:
                        stockPrice = ConvertLst_Dict(stockPrice)
                        if(stockPrice['SP'] == 'U'):
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
                dictofSP = dict(zipbObj)
                SP_dict[symbol]= dictofSP

                return call_error,SP_dict
    else: 
        return call_error,0

def getstockVolumeDataRange(Symbol, exp_date, strikeprice, date, duration_range,contracttype):
    SV_dict=dict()
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
        for i in range(len(CSVOptionSymbolList)):
            if(symbol == CSVOptionSymbolList[i]):
                stockVolume_list = []
                
                for j in range(0,duration_range):
                    stockVolume = dataapi.getrowdata(i,countcols,Symbol,contracttype)
                    dateheader.append(csvDateHeaderlist[countcols])
                    stockVolume = str(stockVolume).split(data_seperator)
                    if listOfStr[2] in stockVolume:
                        stockVolume = ConvertLst_Dict(stockVolume)
                        if(stockVolume['SV'] == 'U'):
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
                dictofSP = dict(zipbObj)
                SV_dict[symbol]= dictofSV

                return call_error,SV_dict
    else: 
        return call_error,0

# <- returns dictioary of all OI data of all trading days of an exp_date
def getAllOpenInterestData(Symbol, exp_date, strikeprice,contracttype):
    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    OI_dict=dict()

    dateheader =[]
    if(call_error == globalheader.Success):
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
                        if(openInterest['OI'] == 'U'):
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
                dictofOI = dict(zipbObj)
                OI_dict[strikeprice]= dictofOI

                return call_error,OI_dict
    else: 
        return call_error,0

# returns dictioary of all OV data of all trading days of an exp_date
def getAllOptionVolumeData(Symbol, exp_date, strikeprice,contracttype):
    OV_dict=dict()
    
    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    dateheader =[]
    
    if(call_error == globalheader.Success):
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
                        if(optionVolume['OV'] == 'U'):
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
                dictofOI = dict(zipbObj)
                OV_dict[symbol]= dictofOV
                    
                return call_error,OV_dict
    else: 
        return call_error,0

# returns dictioary of all OP data of all trading days of an exp_date
def getAllOptionPriceData(Symbol, exp_date, strikeprice,contracttype):
    OP_dict=dict()

    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    dateheader =[]
            
    if(call_error == globalheader.Success):
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
                        if(optionPrice['OP'] == 'U'):
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
                dictofOP = dict(zipbObj)
                OP_dict[symbol]= dictofOP

                return call_error,OP_dict
    else: 
        return call_error,0

# returns dictioary of all SP data of all trading days of an exp_date
def getAllstockPriceData(Symbol, exp_date, strikeprice,contracttype):
    SP_dict=dict()

    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    dateheader =[]
        
    if(call_error == globalheader.Success):
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
                        if(stockPrice['SP'] == 'U'):
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
                dictofSP = dict(zipbObj)
                SP_dict[symbol]= dictofSP

                return call_error,SP_dict
    else: 
        return call_error,0

# returns dictioary of all SV data of all trading days of an exp_date
def getAllstockVolumeData(Symbol, exp_date, strikeprice,contracttype):
    SV_dict=dict()
    call_error,CSVOptionSymbolList,symbol,csvDateHeaderlist,countCols = dataapi.getdataframeData(Symbol,exp_date,strikeprice,contracttype)
    totalcols = len(csvDateHeaderlist)-1
    dateheader =[]
            
    if(call_error == globalheader.Success):
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
                        if(stockVolume['SV'] == 'U'):
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
                dictofSP = dict(zipbObj)
                SV_dict[symbol]= dictofSV

                return call_error,SV_dict
    else: 
        return call_error,0
