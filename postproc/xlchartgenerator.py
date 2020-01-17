import csv
import pandas as pd
from pandas import DataFrame
from datetime import date
from datetime import datetime
import datetime as DT
import time
import os
import os.path
import datetime
import xlsxwriter
from os import path
import Commonapi

ofilepath = './output/'
ifilepath ='./input/'
ofilename = 0
ifilename = 0


#geneateOXLChartMain - generate Output XL CHArt of OI,OV jump or down
    # input - ifname,ofname
        # ifame - input file could be OI,OV ChartInput_AllStocks
    #output
        #ofname - output file could be OI,OV XLChart_AllStocks
    
def geneateOXLChartMain(ifname,ofname):
    if(Commonapi.info == 1):
        logging.info('geneateOXLChartMain Started')
    global ifilename
    global ofilename
    ifilename = ifname
    ofilename = ofname
    #############################################################################################################
    #initialization and configuration
    row_index = 0
    sheet_count = 0
    header = ["Date", "OI", "SP", "SV (100K Units)", "OP", "OV","TotalMoney"]
    num_headers = 5
    line_value = ["!$A$2:$A$", "!$B$2:$B$", "!$C$2:$C$", "!$D$2:$D$", "!$E$2:$E$", "!$F$2:$F$"]
    iFileName = Commonapi.getInputfile(ifilename)
    #############################################################################################################
    
    oFileName = Commonapi.createoxlFile(ofilename)
    if os.path.exists(oFileName):
        logging.warning('%s %s', 'file exists', oFileName)
        os.remove(oFileName)
        logging.warning('File Removed')    
        
    if os.path.exists(iFileName):
            logging.warning('%s %s', 'file exists', iFileName)
            data_frame = pd.read_csv(iFileName, index_col = False)
            iFileCountCols = data_frame.shape[1]
            iFileCountRows = data_frame.shape[0]

            with open(iFileName, 'rU') as readFile:
                readCSV = csv.reader(readFile)
                dateRow = next(readCSV)

                #create xlsfile
                outWorkBook = xlsxwriter.Workbook(oFileName)

                for row in readCSV:
                    optionSymbol = str(row[0])
                    
                    sheet_count =  sheet_count + 1
                    sheet_name = str(sheet_count) + str(optionSymbol)
                    outSheet = outWorkBook.add_worksheet(sheet_name)

                    #copy the first row header for the new file
                    for colIndex in range(0, 6):
                        outSheet.write(0, colIndex, header[colIndex])
                    
                    #copy the date dfrom first row into first column of new .xlsx file (like matrix transpose)
                    for iFileColIndex in range(1, iFileCountCols):
                        outSheet.write(iFileColIndex, 0, dateRow[iFileColIndex])

                    #copy each row elements remaining split across ":" delimeter into a separate row
                    for iFileColIndex in range(1, iFileCountCols):
                        iFileRowDataArray  = str(row[iFileColIndex]).split(":")
                        for i in range(len(Commonapi.listOfStr)):
                            if Commonapi.listOfStr[i] in iFileRowDataArray:
                                rowdata = Commonapi.ConvertLst_Dict(iFileRowDataArray)                           
                                if Commonapi.listOfStr[i] == 'SV':
                                #devide by 100k if stock volume to harmnanize the easy viewing all lines in the graph
                                #because stock volume is relatively large compared to other parameters in the chart
                                    outSheet.write(iFileColIndex, i+1, float(float(rowdata[Commonapi.listOfStr[i]])/100000))
                                else:
                                    outSheet.write(iFileColIndex, i+1, float(rowdata[Commonapi.listOfStr[i]]))
                            else:
                                if i == 2:
                                #devide by 100k if stock volume to harmnanize the easy viewing all lines in the graph
                                #because stock volume is relatively large compared to other parameters in the chart
                                    outSheet.write(iFileColIndex, i+1, float(float(iFileRowDataArray[i])/100000))
                                else:
                                    outSheet.write(iFileColIndex, i+1, float(iFileRowDataArray[i]))


                    #outSheet.write_array_formula('G2:G'+str(iFileCountCols) , '{=PRODUCT($B*$E'+'*100)}')
                    outSheet.write(0, 6, header[6])
                    for rowIndex in range(2,iFileCountCols+1):
                        outSheet.write_array_formula('$G'+str(rowIndex) , '{=PRODUCT($B'+str(rowIndex)+',$E'+str(rowIndex)+',100)}')

                    #chart creation 1`
                    chartLinesList = [0, 2, 3, 4]
                    chart = outWorkBook.add_chart({"type":"line"});
                    chart.set_x_axis({'name': 'Date'})
                    chart.add_series({"categories": sheet_name + "!$A$2:$A$" +str(iFileCountCols+1), "values": sheet_name + "!$A$2:$A$" + str(iFileCountCols+1)})

                    for ofile_row_index in range(0, num_headers+1):
                        #print("iFileCountCols is :",iFileCountCols)
                        if ofile_row_index in chartLinesList:
                            chart.add_series({"values": sheet_name + line_value[ofile_row_index] +str(iFileCountCols+1), "name": header[ofile_row_index]})
                                         
                    outSheet.insert_chart("I1", chart)
                    
                    #chard creation 2
                    chartLinesList = [1, 5]
                    chart = outWorkBook.add_chart({"type":"line"});
                    chart.set_x_axis({'name': 'Date'})
                    chart.add_series({"categories": sheet_name + "!$A$2:$A$" +str(iFileCountCols+1), "values": sheet_name + "!$A$2:$A$" + str(iFileCountCols+1)})

                    for ofile_row_index in range(0, num_headers+1):
                        #print("iFileCountCols is :",iFileCountCols)
                        if ofile_row_index in chartLinesList:
                            chart.add_series({"values": sheet_name + line_value[ofile_row_index] +str(iFileCountCols+1), "name": header[ofile_row_index]})
                                         
                    outSheet.insert_chart("I15", chart)
                                     


                outWorkBook.close()
    else:
        logging.error('%s %s','File Does not Exists:',iFileName)
                            
    if(Commonapi.info == 1):
        logging.info('geneateOXLChartMain Ended')
