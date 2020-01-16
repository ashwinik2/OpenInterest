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
import openpyxl
from datetime import timedelta
from openpyxl.chart import BarChart,Reference,Series,LineChart
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.label import DataLabel
import Commonapi


final_OTM_chart_y_axis =['CPIOTM x K']
# insertLineChart insert the line chart to the output xl file
#insertLineChart(sheet_obj,strikeprices,symbol,finalOptionExpDate,expdate_chart_y_axis,expdate_chart_col_loc,expdate_chart_insert_pos,num_of_chart_per_sheet):
    #sheet_obj - xl file sheet obj
    #strikeprices - list of strikeprices to be insereted as column header
    #symbol - stock symbol
    #finalOptionExpDate-  stock exp date
    #expdate_chart_y_axis - string 
    #expdate_chart_col_loc - column data loc of the sheet obj
    #expdate_chart_insert_pos - position where chart to be inserted
    #num_of_chart_per_sheet - number of chart to be inserted for call -1 and put -1
    
def insertLineChart(sheet_obj,strikeprices,symbol,finalOptionExpDate,expdate_chart_y_axis,expdate_chart_col_loc,expdate_chart_insert_pos,num_of_chart_per_sheet):
    for j in range(0,(int)(num_of_chart_per_sheet)):
        min_cols = (int)(expdate_chart_col_loc[j])
        max_cols = len(strikeprices)+min_cols
        m_rows = sheet_obj.max_row

        chart = LineChart()
        chart.type = "line"
        chart.title = symbol+'_'+finalOptionExpDate
        chart.y_axis.title = expdate_chart_y_axis[j]
        chart.x_axis.title = 'Dates'
        data = Reference(sheet_obj, min_col=min_cols, min_row=1, max_row=m_rows, max_col=max_cols)
        #data = Reference(sheet_obj, min_col=min_cols, min_row=2, max_row=m_rows, max_col=max_cols)
        cats = Reference(sheet_obj, min_col=(int)(expdate_chart_col_loc[j])-1, min_row=2, max_row=m_rows)
        chart.add_data(data, titles_from_data=True)

        chart.set_categories(cats)
        sheet_obj.add_chart(chart, expdate_chart_insert_pos[j])
        title = symbol+'_'+finalOptionExpDate
        print("Line chart :",title)

# insertTotalMoneyCPChart insert the bar chart to the output xl file of total money invested of call and put of total num of expiration dates
#insertTotalMoneyCPChart(sheet_obj,num_of_exp,symbol,finalOptionExpDate,final_chart_col_loc,final_chart_insert_pos,getNumberColsData)
    #sheet_obj - xl file sheet obj
    #num_of_exp - num of stock expiration dates
    #symbol - stock symbol
    #finalOptionExpDate-  stock exp date
    #expdate_chart_y_axis - string 
    #expdate_chart_col_loc - column data loc of the sheet obj
    #expdate_chart_insert_pos - position where chart to be inserted
    #getNumberColsData - number of trading days nothing but total rows
        
def insertTotalMoneyCPChart(sheet_obj,num_of_exp,symbol,finalOptionExpDate,final_chart_col_loc,final_chart_insert_pos,getNumberColsData):
    if(Commonapi.debug == 1):
        print("insertTotalMoneyCPChart started")
    for i in range(0,(int)(num_of_exp)):
        min_cols = (int)(final_chart_col_loc[i])
        max_cols =min_cols+1
        m_rows = min_cols+getNumberColsData
        print("m_rows min_cols is :",m_rows,min_cols)
        chart = BarChart()
        chart.type = "col"
        chart.grouping = "stacked"
        chart.overlap = 100
        chart.title = symbol+'_'+finalOptionExpDate[i]
        chart.y_axis.title = 'TOTAL_CALL_PUT_TM x K'
        chart.x_axis.title = 'Dates'
        data = Reference(sheet_obj, min_col=min_cols, min_row=1, max_row=m_rows, max_col=max_cols)
        cats = Reference(sheet_obj, min_col=1, min_row=2, max_row=m_rows)
        chart.add_data(data, titles_from_data=True)
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showVal = True
        chart.set_categories(cats)
        sheet_obj.add_chart(chart, final_chart_insert_pos[i])
        title = symbol+'_'+finalOptionExpDate[i]
        print("Bar chart :",title)
    if(Commonapi.debug == 1):
        print("insertTotalMoneyCPChart ended")

# insertCPIOMchartToCPMISheet insert the bar chart to the output xl file of total money invested of call and put of total num of expiration dates
#insertCPIOMchartToCPMISheet(sheet_obj,symbol,finalOptionExpDate,num_of_exp,final_OTM_chart_insert_pos,iotm_data_col_loc,getNumberColsData,iotm_row_loc):
    #sheet_obj - xl file sheet obj
    #num_of_exp - num of stock expiration dates
    #symbol - stock symbol
    #finalOptionExpDate-  stock exp date
    #expdate_chart_y_axis - string 
    #expdate_chart_col_loc - column data loc of the sheet obj
    #expdate_chart_insert_pos - position where chart to be inserted
    #getNumberColsData - number of trading days nothing but total rows
    #final_OTM_chart_insert_pos - where in-the-money, out-of-money chart insert pos of call or put
    #iotm_col_loc - where in-the-money, out-of-money data loc(row position) of call or put
    #iotm_data_col_loc - where in-the-money, out-of-money data loc(col position) of call or put

def insertCPIOMchartToCPMISheet(sheet_obj,symbol,finalOptionExpDate,num_of_exp,final_OTM_chart_insert_pos,chart_col_loc,getNumberColsData,iotm_row_loc):
    if(Commonapi.debug == 1):
        print("insertCPIOMchartToCPMISheet started")
    for i in range(0,num_of_exp):
        min_rows = (int)(iotm_row_loc[0])
        min_cols = (int)(iotm_data_col_loc)
        max_cols =min_cols+3
        max_rows = min_rows+getNumberColsData
        chart = BarChart()
        chart.type = "col"
        chart.grouping = "stacked"
        chart.overlap = 100
        chart.title = symbol+'_'+finalOptionExpDate[i]
        chart.y_axis.title = final_OTM_chart_y_axis[0]
        chart.x_axis.title = 'Dates'
        data = Reference(sheet_obj, min_col=min_cols, min_row=min_rows, max_row=max_rows, max_col=max_cols)
        cats = Reference(sheet_obj, min_col=1, min_row=min_rows+1, max_row=max_rows)
        chart.add_data(data, titles_from_data=True)
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showVal = True
        chart.set_categories(cats)
        sheet_obj.add_chart(chart, final_OTM_chart_insert_pos[i])
        title = symbol+'_'+finalOptionExpDate[i]
        print("Bar chart :",title)
    if(Commonapi.debug == 1):
        print("insertCPIOMchartToCPMISheet ended")

# insertCPIOMOIchartToCPMISheet insert the bar chart to the output xl file of where in-the-money, out-of-money open interest  of call and put of total num of expiration dates
#insertCPIOMOIchartToCPMISheet(sheet_obj,symbol,finalOptionExpDate,num_of_exp,final_OTMOI_chart_insert_pos,chart_col_loc,getNumberColsData,iotmio_col_loc):
    #sheet_obj - xl file sheet obj
    #num_of_exp - num of stock expiration dates
    #symbol - stock symbol
    #finalOptionExpDate-  stock exp date
    #expdate_chart_y_axis - string 
    #expdate_chart_col_loc - column data loc of the sheet obj
    #expdate_chart_insert_pos - position where chart to be inserted
    #getNumberColsData - number of trading days nothing but total rows
    #final_OTM_chart_insert_pos - where in-the-money, out-of-money chart insert pos of call or put of open interest
    #iotmio_col_loc - where in-the-money, out-of-money data loc(row position) of call or put of open interest
    #iotmio_data_col_loc - where in-the-money, out-of-money data loc(col position) of call or put of open interest

def insertCPIOMOIchartToCPMISheet(sheet_obj,symbol,finalOptionExpDate,num_of_exp,final_OTMOI_chart_insert_pos,iotmio_data_col_loc,getNumberColsData,iotmio_row_loc):

    if(Commonapi.debug == 1):
        print("insertCPIOMOIchartToCPMISheet started")
    for i in range(0,num_of_exp):
        min_rows = (int)(iotmio_row_loc[1])
        min_cols = (int)(iotmio_data_col_loc[i])
        max_cols =min_cols+3
        max_rows = min_rows+getNumberColsData
        chart = BarChart()
        chart.type = "col"
        chart.grouping = "stacked"
        chart.overlap = 100
        chart.title = symbol+'_'+finalOptionExpDate[i]
        chart.y_axis.title = final_OTM_chart_y_axis[0]
        chart.x_axis.title = 'Dates'
        data = Reference(sheet_obj, min_col=min_cols, min_row=min_rows, max_row=max_rows, max_col=max_cols)
        cats = Reference(sheet_obj, min_col=1, min_row=min_rows+1, max_row=max_rows)
        chart.add_data(data, titles_from_data=True)
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showVal = True
        chart.set_categories(cats)
        sheet_obj.add_chart(chart, final_OTMOI_chart_insert_pos[i])
        title = symbol+'_'+finalOptionExpDate[i]
        print("Bar chart :",title)
    if(Commonapi.debug == 1):
        print("insertCPIOMOIchartToCPMISheet ended")

