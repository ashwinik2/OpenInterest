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


final_chart_insert_pos = ["A24","K24","T24","AD24","AN24","AX24","BH24","BR24"]
final_OTM_chart_insert_pos = ["A70","K70","T70","AD70","AN70","AX70","BH70","BR70"]
final_OTM_chart_y_axis =['CPIOTM x K']
num_of_chart_per_sheet = 3

def insertLineChart(sheet_obj,strikeprices,symbol,finalOptionExpDate,expdate_chart_y_axis,expdate_chart_col_loc,expdate_chart_insert_pos):
    
    for j in range(0,num_of_chart_per_sheet):
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
        cats = Reference(sheet_obj, min_col=(int)(expdate_chart_col_loc[0])-1, min_row=2, max_row=m_rows)
        chart.add_data(data, titles_from_data=True)

        chart.set_categories(cats)
        sheet_obj.add_chart(chart, expdate_chart_insert_pos[j])
        title = symbol+'_'+finalOptionExpDate
        print("Line chart :",title)
        
def insertTotalMoneyCPChart(sheet_obj,num_of_exp,symbol,finalOptionExpDate,final_chart_col_loc):

    for i in range(0,num_of_exp):
        min_cols = (int)(final_chart_col_loc[i])
        max_cols =min_cols+1
        m_rows = sheet_obj.max_row
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


def insertCPIOMchartToCPMISheet(sheet_obj,symbol,finalOptionExpDate,num_of_exp,final_OTM_chart_col_loc,getNumberColsData):
    min_rows = 42
    for i in range(0,num_of_exp):
        min_cols = (int)(final_OTM_chart_col_loc[i])
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

