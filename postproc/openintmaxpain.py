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
import xlsxwriter
import openpyxl
from datetime import timedelta

global CSVOptionSymbolList
import sys

endpoint = r"https://api.tdameritrade.com/v1/marketdata/chains"
stockSymbol = []
stockOptionType = []
stockCsvFiles = []
todayDate = []
expDate = []
getNumberColsData = 20



csv.field_size_limit(sys.maxsize)

contractType =['CALL','PUT']
ifilepath = './../datacolls/output/'
ifilestocklist = './../datacolls/input/'+'StockList.csv'

ofilepath = './output/'
ifile = ofilepath
ofilename = ofilepath+'OImax_pain_mp'

header = ["CallMP", "PutMP","TotalMP"]
expdate_chart_col_loc =['2','71','141','241','321','401','500']
num_headers = 4
debug = 0
OI_INDEX = 0
SP_INDEX = 1


symbol = raw_input("Enter symbol :") 
print(symbol) 
num_expiration = raw_input("Enter number of expiration dates data you want : ") 
print(num_expiration) 

totalStocks = 1

def getStockCSVFiles(index,stockIndex):       
    stockCsvfilename = ifilepath + symbol+'_'+contractType[index]+'.csv'
    return stockCsvfilename

def createoFile():
    today = datetime.date.today()
    today= datetime.datetime.strftime((today), '%m_%d_%Y')
    stockCsvfilename = ofilename+'_'+symbol+'_'+today+'.xlsx'
    return stockCsvfilename

def getOptExpDateFromCSV(optionSymbol):
    symbol,date = optionSymbol.split('_')
    date = list(str(date))
    length = len(date)
    expdate = '20'+date[4]+date[5]+date[0]+date[1]+date[2]+date[3]
    #print("expdate is :",expdate)
    return expdate


def removeDuplicateDates(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list

def getOptionStrikePrice(optionSymbol):
    n = 7
    symbol,strikeprice = optionSymbol.split('_')
    strikeprice  = list(str(strikeprice ))
    length = len(strikeprice )
    strikeprice= strikeprice[n:]
    strikeprice =''.join(strikeprice)
#       print("strikeprice is.................. :",strikeprice)
    return strikeprice


def mainloop():

    global CSVOptionSymbolList
    global totalStocks
    sheet_count = 0


    ofile = createoFile()
    if os.path.exists(ofile):
        print("file exists:",ofile)
        os.remove(ofile)
        print("File Removed!")

    wb_obj = openpyxl.Workbook()
    
    for index in range(totalStocks):
        Index = index
        rows = []        

        for contracttype in range(0,1):
            ifile =  getStockCSVFiles(contracttype,Index)
            if os.path.exists(ifile):
                print("File Exists:",ifile)                                    
            else:
                print("File does not Exists:",ifile)
                 
            if os.path.exists(ifile):
                print("File Exists")
                data_frame = pd.read_csv(ifile, index_col = False)
                countRows = data_frame.shape[0]
                countCols = data_frame.shape[1]
                
                CSVOptionSymbolList= data_frame.Symbol.tolist()
                if(debug == 1):
                    print("CSVOptionSymbolList  and length is  :",CSVOptionSymbolList,len(CSVOptionSymbolList))
                
                expDateList =[]
                for index in range(0,len(CSVOptionSymbolList)):
                    expdatelist = getOptExpDateFromCSV(CSVOptionSymbolList[index])
                    expDateList.append(expdatelist)                
                    
                finalOptionExpDateList=[]
                finalOptionExpDateList = removeDuplicateDates(expDateList)
                finalOptionExpDateList= sorted(finalOptionExpDateList)

                print("finalOptionExpDateList is :",finalOptionExpDateList)
                
                
                finalOptionExpDateList1 =[]
                for i in range(0,(int)(num_expiration)):
                    finalOptionExpDateList1.append(finalOptionExpDateList[i])

                print("finalOptionExpDateList1 and len(finalOptionExpDateList1 ) is :",finalOptionExpDateList1,len(finalOptionExpDateList1))

            depth = [[]]
            for i in range(0,len(contractType)):
                depth.append([])
            for expdate in range(0,len(finalOptionExpDateList1)):
                print("finalOptionExpDateList1 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:",finalOptionExpDateList1[item1])
                colCount = 0
                rowCount = 0
                colFrom = 0
                strikeprices = []
                strike_max_pain = []
                col=[]
                del depth[0][:]
                del depth[1][:]
                for contracttype in range(len(contractType)):
                    del strikeprices[:]
                    del strike_max_pain[:]
                    m_col_call = 0
                    m_col_put =0
                    m_row_call = 0
                    m_row_put =0
                    
                    if(contracttype == 0):
                        colCount = 0
                        rowCount = 0
    
                        sheet_name =  str(symbol)+finalOptionExpDateList1[expdate]
                        wb_obj.create_sheet(index = expdate , title = sheet_name)
                        sheets = wb_obj.sheetnames
                        sheet_obj = wb_obj[sheets[expdate]]

                    ifile =  getStockCSVFiles(contracttype,Index)
                    if os.path.exists(ifile):
                        print("File Exists:",ifile)                                    
                    else:
                        print("File does not Exists:",ifile)
                 
                    if os.path.exists(ifile):
                        print("File Exists")
                        data_frame = pd.read_csv(ifile, index_col = False)
                        countRows = data_frame.shape[0]
                        countCols = data_frame.shape[1]
                        
                
                        CSVOptionSymbolList= data_frame.Symbol.tolist()
                        if(debug == 1):
                            print("CSVOptionSymbolList  and length is  :",CSVOptionSymbolList,len(CSVOptionSymbolList))
                        length = len(CSVOptionSymbolList)
                        
                        strikepriceList =[]
                        for index in range(0,len(CSVOptionSymbolList)):                                    
                            symbolexpdate1 = getOptExpDateFromCSV(CSVOptionSymbolList[index])
                            if(symbolexpdate1 == finalOptionExpDateList1[expdate]):
                                strikeprice = getOptionStrikePrice(CSVOptionSymbolList[index])
                                strikepriceList.append(strikeprice)
                        strikepriceList = removeDuplicateDates(strikepriceList)
                        strikepriceList = sorted(strikepriceList)
                        print("strikepriceList = sorted(strikepriceList) is :",strikepriceList )
                        
                        data =[]
                        
                        columnList= data_frame.columns.tolist()
                        colFrom = countCols-getNumberColsData
                        colTo = countCols

                #Looping csv file and calculating max pain for each strike price of each expiration
                        for i in range(0,getNumberColsData):
                            del strikeprices[:]
                            del strike_max_pain[:]
                            
                            for stockprice in range(0,len(strikepriceList)):
                                ent = 0
                                max_pain = 0                                
                                for row in range(0,len(CSVOptionSymbolList)):
                                    strikeexpdate = (float)(getOptionStrikePrice(CSVOptionSymbolList[row]))
                                    strikeprice = (getOptExpDateFromCSV(CSVOptionSymbolList[row]))
                                    strikeprice = (float)(strikeprice)
                                    if((strikeexpdate == finalOptionExpDateList1[expdate])):
                                        ent +=1
                                        if(ent == 1):
                                            strikeprices.append(strikeprice)
                                        data_frame = pd.read_csv(ifile, index_col = False)
                                        countRows = data_frame.shape[0]
                                        countCols = data_frame.shape[1]                                        
                                        rowData = data_frame.iloc[row,colFrom]
                                        if(rowData == 'U'):
 #                                           print("colFrom is :",colFrom)
                                            OI =0
                                            SP =0
                                            stockPrice = (float)(0)
                                            strikePrice = (float)(0)
                                        else:                                            
                                            rowData = str(rowData).replace('[','')
                                            rowData = str(rowData).replace(']','')
                                            rowData = str(rowData).split(':')
                                            OI = rowData[OI_INDEX]
                                            if((OI == 'U') or (OI == '') or (OI == '.')):
                                                OI = (int)(0)
                                            else:
                                                OI =(float)(rowData[OI_INDEX])
                                            SP = rowData[SP_INDEX]
                                            if((SP == 'U') or (SP == '') or (SP == '.')):
                                                SP = (int)(0)
                                            else:
                                                SP =(float)(rowData[SP_INDEX])
                                            strikePrice = getOptionStrikePrice(CSVOptionSymbolList[row])
                                            stockPrice = strikeprice
                                            stockPrice = (float)(stockPrice)
                                            strikePrice = (float)(strikePrice)
                                        if(contracttype == 0):
                                            if(stockPrice > strikePrice):                                           
                                               maxpain = abs(stockPrice-strikePrice)
                                               max_pain +=maxpain*OI
                                            elif(stockPrice < strikePrice):
                                               max_pain += 0
                                            else:
                                               if(stockPrice == strikePrice):
                                                    max_pain += 0
                                               else:
                                                    max_pain += 0
    

                                        if(contracttype == 1):
                                            if(stockPrice < strikePrice):
                                               maxpain = abs(stockPrice-strikePrice)
                                               max_pain += maxpain*OI
                                            elif(stockPrice > strikePrice):
                                               max_pain += 0 
                                            else:
                                                if(stockPrice == strikePrice):
                                                    max_pain += 0
                                                else:
                                                    max_pain += 0
                                strike_max_pain.append(max_pain)
                                depth[contracttype].append(max_pain)
                                
             #### Adding call max pain of individual strikeprice to excel sheet
                                                              
                            if(contracttype == 0):
                                m_col = (int)(expdate_chart_col_loc[0])-1
                                print(sheet_obj.max_column)
                                if(i == 0):
                                    cellref=sheet_obj.cell(row=1, column=m_col)
                                    cellref.value=header[0]
                                    col = strikeprices
                                    for item in range(len(strikeprices)):
                                        cellref=sheet_obj.cell(row = 1, column=m_col+item)
                                        cellref.value=strikeprices[item]
                                        
                                m_row_call += 1
                                cellref=sheet_obj.cell(row = m_row_call+1, column=1)
                                cellref.value=columnList[colFrom]
                                col_index = (int)(expdate_chart_col_loc[0])
                                for item3 in range(0,len(strike_max_pain)):                            
                                    cellref=sheet_obj.cell(row = m_row_call+1, column=item3+col_index)
                                    cellref.value=strike_max_pain[item3]
                                    
            #### Adding put max pain of individual strikeprice to excel sheet

                            if(contracttype == 1):
                                m_col= (int)(expdate_chart_col_loc[1])-1                             
                                print(sheet_obj.max_column)
                                if(i == 0):
                                    cellref=sheet_obj.cell(row=1, column=m_col)
                                    cellref.value=header[1]
                                    m_col_put += 1
                                    for item in range(len(strikeprices)):
                                        cellref=sheet_obj.cell(row = 1, column=m_col+item+1)
                                        cellref.value=strikeprices[item]
                                                                        
                                m_row_put += 1
                                cellref=sheet_obj.cell(row = m_row_put+1, column=m_col)
                                cellref.value=columnList[colFrom]
                                col_index = (int)(expdate_chart_col_loc[1]) 
                                for item3 in range(0,len(strike_max_pain)):                            
                                    cellref=sheet_obj.cell(row = m_row_put+1, column = col_index+item3)
                                    cellref.value=strike_max_pain[item3]
                            colFrom += 1


    #### Calculating Total Max Pain and adding to excel sheet
                m_rows = sheet_obj.max_row            
                m_col = (int)(expdate_chart_col_loc[2])
                cellref=sheet_obj.cell(row=1, column=m_col-1)
                cellref.value=header[2]

                for item in range(len(strikeprices)):
                    cellref=sheet_obj.cell(row = 1, column=m_col+item)
                    cellref.value=strikeprices[item]

                for i in range(2, m_rows+1):
                    cellref=sheet_obj.cell(row = i, column=1)
                    value = cellref.value
                    cellref=sheet_obj.cell(row = i, column=m_col-1)
                    cellref.value=value
                    callmpvalue = []
                    putmpvalue = []
                    col_index = (int)(expdate_chart_col_loc[0])
                    for item in range(len(strikeprices)):
                    cellref=sheet_obj.cell(row = m_rows, column=col_index+item)
                    value = cellref.value
                    print("callmpvalue is :",callmpvalue)
                    callmpvalue.append(value)
                    col_index = (int)(expdate_chart_col_loc[1])   
                    for item in range(len(strikeprices)):
                        cellref=sheet_obj.cell(row = m_rows, column=col_index+item)
                        value = cellref.value
                        print("putmpvalue is :",putmpvalue)
                        putmpvalue.append(value)
                
                    for i in range(len(strikeprices)):
                        cellref=sheet_obj.cell(row = m_rows, column=m_col+i)
                        print("callmpvalue and value 2  :",callmpvalue[i],putmpvalue[i]) 
                        total = callmpvalue[i]+putmpvalue[i]
                        cellref.value=total 


                        
    wb_obj.save(ofile)
mainloop() 
                    
print('done')
