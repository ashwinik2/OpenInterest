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

todayDate = []

ofilepath = './output/'
ifilepath = './input/'
ifilename = ofilepath+'OVPerJump_400'
ofilename = ofilepath+'OVChartInput'


def getInputFile():       
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ifilename+'_'+today+'.csv'
    return stockCsvfilename
        
def extract(string, start=':'):
        return string[string.index(start)+1]
    
def createOIJumpFile():
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+today+'.csv'
    return stockCsvfilename

def mainloop():

    header_list =[]
    
    ocsvOIJumpFile = createOIJumpFile()
    ofile = ocsvOIJumpFile
    if os.path.exists(ofile):
        print("file exists:",ofile)
        os.remove(ofile)
        print("File Removed!")
    if os.path.exists(ofile):
        print("file exists:",ofile)
    
    else:

        icsvFileName = getInputFile()        
        ifile = icsvFileName
        if os.path.exists(ifile):
            print("File Exists:",ifile)
            data_frame = pd.read_csv(ifile, index_col = False)
            countCols = data_frame.shape[1]
            print("countCols is :",countCols)
            header_list = data_frame.columns.tolist()
            colFrom = 1 
            colTo = countCols
            header_list_2 = ['Symbol']+header_list[colFrom:colTo]

            header_list = [header_list]
            print("len of header_list and header_list is :",len(header_list),header_list)
            
            header_list_2 = [header_list_2]
            print("header_list_2 is :",header_list_2)
            with open(ofile, 'w',) as myfile:
                writer = csv.writer(myfile)
                for row in header_list_2:
                    writer.writerow(row)
                    
    icsvFileName = getInputFile()
    ifile = icsvFileName
    
    if os.path.exists(ifile):
        print("File Exists:",ifile)
        data_frame = pd.read_csv(ifile, index_col = False)
        data_frame = data_frame.fillna(0)
        countCols = data_frame.shape[1]
        countRows = data_frame.shape[0]
        print("number of rows:",countRows)
        print("number of cols:",countCols)

        optionSymbol =[]
        colFrom = 1
        colTo = countCols
        row_index = 0
        j =0
        with open(icsvFileName, 'rU') as readFile:
            readCSV = csv.reader(readFile)
            fields = next(readCSV)
            for row in readCSV:
                optionSymbol = [str(row[0])]
                doProcess = 1
                
                print("colTo,colFrom,row_index, doProcess is :",colTo,colFrom,row_index,doProcess) 
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
                    
                    print("optSymbol = optionSymbol..... is :",optSymbol)  
                    outPutValue =[]
                    fillzeros = []
                    rowData =data_frame.iloc[row_index,colFrom:colTo]
                    
                    for item in range(0,len(rowData)):
                        rowFindU  = str(rowData[item]).split(":")
                        fillzeros = rowFindU
                        print("rowFindU is :",rowFindU)
                        result = (str(rowFindU).find('U'))
                        print("result is :",result)
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
                            
                        print("outPutValue is :",outPutValue)
                    for item in range(0,len(outPutValue)):
                        if(outPutValue[item] == 'NU'):
                            print("No operation row[j],j,optionSymbol: ",pastColsDat[j],j,optionSymbol)
                            addDataoFile = 0
                            
                    if(addDataoFile == 1):                          
                        rowsData = [(optSymbol)+(outPutValue)]
                        ofile = ocsvOIJumpFile
                        print(" rowData is :",rowData)
                        if os.path.exists(ofile):
                            with open(ofile, 'a',) as csvfile:
                                wr = csv.writer(csvfile,lineterminator='\r')
                                for row in rowsData:
                                    wr.writerow(row)
                        else:
                            with open(ofile, 'w',) as myfile:
                                writer = csv.writer(myfile)
                                writer.writerow(['Symbol','YestOI','TodayOI','%Jump'])
                        #addDataoFile = 0
                    doProcess = 0 
                row_index += 1
                        
        
    else:
        print("File Does not Exists:",ifile)
        
    
mainloop() 
                    
print('done')
