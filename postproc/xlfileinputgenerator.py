import csv
import time
import os
import pandas as pd
from pandas import DataFrame
from datetime import date
from datetime import datetime
import datetime as DT
import time
import os
import os.path
import datetime
from os import path
import xlchartgenerator
import Commonapi

ofilepath = './output/'
ifilepath = './input/'
ifilename = 0

#convert list into dict
    #input - rowdata
        #rowdata - row cell data 10:250:200000:2.3:200
    #output - dict {{OI:10,SP:250,SV:200000,OP:2.3,OV:200}

def createDict(rowdata):
    if(Commonapi.info == 1):
        logging.info('createDict Started')
    if(Commonapi.debug == 1):
        logging.debug('$s %s','createDict(rowdata) is',rowdata)

    zipbObj = zip(Commonapi.listOfStr, rowdata) 
    dictOfWords = dict(zipbObj)
    if(Commonapi.info == 1):
        logging.info('createDict Ended')
    return dictOfWords

#format row cell data which is unavailavle  to required format
    #output - colData list with formated data OI:0:SP:0:SV:0:OP:0:OV:0

def formatRowDataU():
    colData = []
    stringOI = 'OI'
    stringOI = str(stringOI)+Commonapi.data_seperator+str('0')
    colData.append(stringOI)
    
    stringSP = 'SP'
    stringSP = str(stringSP)+Commonapi.data_seperator+str('0')
    colData.append(stringSP)

    stringSV = 'SV'
    stringSV = str(stringSV)+Commonapi.data_seperator+str('0')
    colData.append(stringSV)
    
    stringOP = 'OP'
    stringOP = str(stringOP)+Commonapi.data_seperator+str('0')
    colData.append(stringOP)

    stringOV = 'OV'
    stringOV = str(stringOV)+Commonapi.data_seperator+str('0')
    colData.append(stringOV)    
    
    colData = ':'.join(str(v) for v in colData)
    return colData

#formatRowDataU format the row cell data which is not in with required length ex:OI:10:SP:250:SV:120000
#  to OI:10:SP:250:SV:120000:OP:0:OV:0
    #input - length,fillzeros
    #output - formated required length of the colData list 

def formatRowDataU(length,fillzeros):
    colData = []
    length1 = len(Commonapi.listOfStr)-length 
    for i in range(length1):
        string = str(Commonapi.listOfStr[i])+':'+str(fillzeros[i])
        colData.append(string)        
 
    for i in range(length1 ,length+1):
        string = str(Commonapi.listOfStr[i])+':'+str('0')
        colData.append(string)
            
    colData = ':'.join(str(v) for v in colData)
    return colData

#generateInputFormatForXLChartMain generates required format for row cell of the unavailable trading day column
    # input - ifname,ochartfilename,ichartfilename
        # ifame - input file could be OI,OV PerJump_AllStocks
    #output
        #ichartfilename - input file could be OI,OV ChartInput_AllStocks 
        #ochartfilename - output file could be OI,OV XLChart_AllStocks
def generateInputFormatForXLChartMain(ifname,ochartfilename,ichartfilename):

    if(Commonapi.info == 1):
        logging.info('generateInputFormatForXLChartMain Started')
    global ifilename
    global ofilename
    ifilename = ifname
    ofilename = ichartfilename
    header_list =[]
    
    oCSVfile = Commonapi.createOutputOIJumpFile(ofilename)
    if os.path.exists(oCSVfile):
        os.remove(oCSVfile)
        logging.warning('File Removed!')
    if os.path.exists(oCSVfile):
        logging.warning('%s %s', 'file exists', oCSVfile)
    
    else:
        iCSVfile = Commonapi.getInputFile(ifilename)       
        if os.path.exists(iCSVfile):
            logging.warning('%s %s', 'file exists', iCSVfile)
            data_frame = pd.read_csv(iCSVfile, index_col = False)
            countCols = data_frame.shape[1]
            header_list = data_frame.columns.tolist()
            colFrom = 1 
            colTo = countCols
            header_list_2 = ['Symbol']+header_list[colFrom:colTo]
            header_list = [header_list]
            header_list_2 = [header_list_2]
            with open(oCSVfile, 'w',) as myfile:
                writer = csv.writer(myfile)
                for row in header_list_2:
                    writer.writerow(row)
                    
    iCSVfile = Commonapi.getInputFile(ifilename)
    
    if os.path.exists(iCSVfile):
        #print("File Exists:",iCSVfile)
        data_frame = pd.read_csv(iCSVfile, index_col = False)
        countCols = data_frame.shape[1]
        countRows = data_frame.shape[0]
        optionSymbol =[]
        colFrom = 1
        colTo = countCols
        row_index = 0
        j =0
        with open(iCSVfile, 'rU') as readFile:
            readCSV = csv.reader(readFile)
            fields = next(readCSV)
            for row in readCSV:
                optionSymbol = [str(row[0])]
                doProcess = 1
                pastColsDat =[]
                pastColsDat =data_frame.iloc[row_index,colFrom:colTo]
                
                colItem =[]
    ### Dd process if columns does not contain 'U'
                for j in range(0,len(pastColsDat)):
                    if(pastColsDat[j] == 'U'):
                        print("No operation row[j],j,optionSymbol: ",pastColsDat[j],j,optionSymbol)
                        doProcess = 1
                                                                    
                if(doProcess == 1):
                    optSymbol = optionSymbol
                    addDataoFile = 1

                    outPutValue =[]
                    fillzeros = []
                    rowData =data_frame.iloc[row_index,colFrom:colTo]
                    
                    for item in range(0,len(rowData)):
                        rowFindU  = str(rowData[item]).split(":")
                        fillzeros = rowFindU
                        result = (str(rowFindU).find('U'))
                        if(result == -1):
                            if(rowFindU == 0):
                                rowData[item]= formatRowDataU()
                                outPutValue.append(rowData[item]) 
                            elif(len(fillzeros) <= 5):
                                length = 5-len(fillzeros)
                                fillzeros= formatRowDataU(length,fillzeros)
                                outPutValue.append(fillzeros)
                            else:
                                outPutValue.append(rowData[item])                        
                        else:
                            outPutValue.append(rowData[item])                                                
                            
                    for item in range(0,len(outPutValue)):
                        if(outPutValue[item] == 'NU'):
                            print("No operation row[j],j,optionSymbol: ",pastColsDat[j],j,optionSymbol)
                            addDataoFile = 0
                            
                    if(addDataoFile == 1):                          
                        rowsData = [(optSymbol)+(outPutValue)]
                        Commonapi.writeOIrOVtolocalCSV(oCSVfile,rowsData)
                        
                    doProcess = 0 
                row_index += 1        
    else:
        logging.error('%s %s', 'File Does not Exists:', iCSVfile)

    if(Commonapi.info == 1):
        logging.info('generateInputFormatForXLChartMain Ended')
        
    #if call_error success from generateInputFormatForXLChartMain call geneateOXLChartMain 
    logging.warning('calling xlchartgenerator')
    xlchartgenerator.geneateOXLChartMain(oCSVfile,ochartfilename) 
                    
