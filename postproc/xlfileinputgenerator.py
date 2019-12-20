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
import commonapi

todayDate = []

ofilepath = './output/'
ifilepath = './input/'
ifilename = 0

# Format the row data if any characters present 'U' to proper data to OI:SP:SV:OP:OV 
def mainloop(ifname,ochartfilename,ichartfilename):
    global ifilename
    global ofilename
    ifilename = ifname
    ofilename = ichartfilename
    header_list =[]
    
    oCSVfile = commonapi.createOutputOIJumpFile(ofilename)
    if os.path.exists(oCSVfile):
        os.remove(oCSVfile)
        print("File Removed!")
    if os.path.exists(oCSVfile):
        print("file exists:",oCSVfile)
    
    else:
        iCSVfile = commonapi.getInputFile(ifilename)       
        if os.path.exists(iCSVfile):
            print("File Exists:",iCSVfile)
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
                    
    iCSVfile = commonapi.getInputFile(ifilename)
    
    if os.path.exists(iCSVfile):
        #print("File Exists:",iCSVfile)
        data_frame = pd.read_csv(iCSVfile, index_col = False)
        data_frame = data_frame.fillna(0)
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
                            if(rowFindU == 0  ):
                                value = []
                                for i in range(0,5):
                                    count = 0
                                    value.append(count)
                                value = ':'.join(str(v) for v in value)
                                rowData[item]= value
                                outPutValue.append(rowData[item]) 
                            elif(len(fillzeros) != 5):                            
                                length = 5 - len(fillzeros)
                                value = []
                                for i in range(length):
                                    count = 0
                                    value.append(count)
                                    fillzeros.append(count)
                                fillzeros = ':'.join(str(v) for v in fillzeros)
                                outPutValue.append(fillzeros)
                            else:
                                outPutValue.append(rowData[item])                        
                        else:
                            value = []
                            for i in range(0,5):
                                count = 0
                                value.append(count)
                            value = ':'.join(str(v) for v in value)
                            rowData[item]= value
                            outPutValue.append(rowData[item])                                                
                            
                    for item in range(0,len(outPutValue)):
                        if(outPutValue[item] == 'NU'):
                            print("No operation row[j],j,optionSymbol: ",pastColsDat[j],j,optionSymbol)
                            addDataoFile = 0
                            
                    if(addDataoFile == 1):                          
                        rowsData = [(optSymbol)+(outPutValue)]
                        commonapi.writeOIrOVtolocalCSV(oCSVfile,rowsData)
                        
                    doProcess = 0 
                row_index += 1
                        
        
    else:
        print("File Does not Exists:",iCSVfile)

    print("calling xlchartgenerator")            
    xlchartgenerator.mainloop(oCSVfile,ochartfilename) 
                    
