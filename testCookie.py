from cgitb import html
from datetime import date, timedelta
import datetime
from itertools import count
import json
import pathlib
import re
from urllib.parse import urlparse
from datetime import date
from datetime import datetime
import pandas as pd
import Web_thread as webTread
import webScraping as web
import DataManager as data
from io import StringIO
import os
import ast
from langdetect import detect
import scrapingGUI as scrap
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidget, QTableWidgetItem,QMessageBox, QProgressBar

# sc = scrap.Ui_MainWindow()
ex = web.webScraping()
dm = data.DataManager()
wt = webTread.WebThread()

link = "https://www.animenewsnetwork.com/"
# path = "C:/Users/tongu/Desktop/Web SC 2/Web-Scraping/web search"
# path = "C:/Users/Pooncharat Wongkom/Web-Scraping/WebData"
# rawData = os.listdir(path)
today = ex.getTodayDate()
newpath = os.path.join('web search',today,"anime(1).csv")
              
dateList =  ['11-04-2022_10_WebJsonData.json', '11-04-2022_11_WebJsonData.json', 
              '11-04-2022_12_WebJsonData.json', '11-04-2022_13_WebJsonData.json',
              '11-04-2022_14_WebJsonData.json', '11-04-2022_15_WebJsonData.json', 
              '11-04-2022_16_WebJsonData.json', '11-04-2022_17_WebJsonData.json', 
              '11-04-2022_18_WebJsonData.json', '11-04-2022_19_WebJsonData.json', 
              '11-04-2022_1_WebJsonData.json', '11-04-2022_2_WebJsonData.json', 
              '11-04-2022_3_WebJsonData.json', '11-04-2022_4_WebJsonData.json', 
              '11-04-2022_5_WebJsonData.json', '11-04-2022_6_WebJsonData.json', 
              '11-04-2022_7_WebJsonData.json', '11-04-2022_8_WebJsonData.json', 
              '11-04-2022_9_WebJsonData.json'] 
            #   '11-04-2022_10_WebJsonData.json', '11-04-2022_11_WebJsonData.json', '11-04-2022_12_WebJsonData.json', '11-04-2022_13_WebJsonData.json', '11-04-2022_14_WebJsonData.json', '11-04-2022_15_WebJsonData.json', '11-04-2022_16_WebJsonData.json', '11-04-2022_17_WebJsonData.json', '11-04-2022_18_WebJsonData.json', '11-04-2022_19_WebJsonData.json', '11-04-2022_1_WebJsonData.json', '11-04-2022_2_WebJsonData.json', '11-04-2022_3_WebJsonData.json', '11-04-2022_4_WebJsonData.json', '11-04-2022_5_WebJsonData.json', '11-04-2022_6_WebJsonData.json', '11-04-2022_7_WebJsonData.json', '11-04-2022_8_WebJsonData.json', '11-04-2022_9_WebJsonData.json', '11-04-2022_10_WebJsonData.json', '11-04-2022_11_WebJsonData.json', '11-04-2022_12_WebJsonData.json', '11-04-2022_13_WebJsonData.json', '11-04-2022_14_WebJsonData.json', '11-04-2022_15_WebJsonData.json', '11-04-2022_16_WebJsonData.json', '11-04-2022_17_WebJsonData.json', '11-04-2022_18_WebJsonData.json', '11-04-2022_19_WebJsonData.json', '11-04-2022_1_WebJsonData.json', '11-04-2022_2_WebJsonData.json', '11-04-2022_3_WebJsonData.json', '11-04-2022_4_WebJsonData.json', '11-04-2022_5_WebJsonData.json', '11-04-2022_6_WebJsonData.json', '11-04-2022_7_WebJsonData.json', '11-04-2022_8_WebJsonData.json', '11-04-2022_9_WebJsonData.json', '11-04-2022_10_WebJsonData.json', '11-04-2022_11_WebJsonData.json', '11-04-2022_12_WebJsonData.json', '11-04-2022_13_WebJsonData.json', '11-04-2022_14_WebJsonData.json', '11-04-2022_15_WebJsonData.json', '11-04-2022_16_WebJsonData.json', '11-04-2022_17_WebJsonData.json', 
            # '11-04-2022_18_WebJsonData.json', '11-04-2022_19_WebJsonData.json', '11-04-2022_1_WebJsonData.json', '11-04-2022_2_WebJsonData.json', '11-04-2022_3_WebJsonData.json', '11-04-2022_4_WebJsonData.json', '11-04-2022_5_WebJsonData.json', '11-04-2022_6_WebJsonData.json', 
            # '11-04-2022_7_WebJsonData.json', '11-04-2022_8_WebJsonData.json', '11-04-2022_9_WebJsonData.json', '11-04-2022_10_WebJsonData.json', 
            # '11-04-2022_11_WebJsonData.json', '11-04-2022_12_WebJsonData.json', '11-04-2022_13_WebJsonData.json', '11-04-2022_14_WebJsonData.json', '11-04-2022_15_WebJsonData.json', '11-04-2022_16_WebJsonData.json', '11-04-2022_17_WebJsonData.json', '11-04-2022_18_WebJsonData.json', '11-04-2022_19_WebJsonData.json', '11-04-2022_1_WebJsonData.json', '11-04-2022_2_WebJsonData.json', '11-04-2022_3_WebJsonData.json', '11-04-2022_4_WebJsonData.json', '11-04-2022_5_WebJsonData.json', '11-04-2022_6_WebJsonData.json', '11-04-2022_7_WebJsonData.json', '11-04-2022_8_WebJsonData.json', '11-04-2022_9_WebJsonData.json', '11-04-2022_10_WebJsonData.json', '11-04-2022_11_WebJsonData.json', '11-04-2022_12_WebJsonData.json', '11-04-2022_13_WebJsonData.json', '11-04-2022_14_WebJsonData.json', '11-04-2022_15_WebJsonData.json', '11-04-2022_16_WebJsonData.json', '11-04-2022_17_WebJsonData.json', '11-04-2022_18_WebJsonData.json', '11-04-2022_19_WebJsonData.json', '11-04-2022_1_WebJsonData.json', '11-04-2022_2_WebJsonData.json', '11-04-2022_3_WebJsonData.json', '11-04-2022_4_WebJsonData.json', '11-04-2022_5_WebJsonData.json', '11-04-2022_6_WebJsonData.json', '11-04-2022_7_WebJsonData.json', '11-04-2022_8_WebJsonData.json', '11-04-2022_9_WebJsonData.json', '11-04-2022_10_WebJsonData.json', '11-04-2022_11_WebJsonData.json', '11-04-2022_12_WebJsonData.json', '11-04-2022_13_WebJsonData.json', '11-04-2022_14_WebJsonData.json', '11-04-2022_15_WebJsonData.json', '11-04-2022_16_WebJsonData.json', '11-04-2022_17_WebJsonData.json', '11-04-2022_18_WebJsonData.json', '11-04-2022_19_WebJsonData.json', '11-04-2022_1_WebJsonData.json', '11-04-2022_2_WebJsonData.json', '11-04-2022_3_WebJsonData.json', '11-04-2022_4_WebJsonData.json', '11-04-2022_5_WebJsonData.json', '11-04-2022_6_WebJsonData.json', '11-04-2022_7_WebJsonData.json', '11-04-2022_8_WebJsonData.json', '11-04-2022_9_WebJsonData.json', '12-04-2022_10_WebJsonData.json', '12-04-2022_11_WebJsonData.json', '12-04-2022_12_WebJsonData.json', '12-04-2022_13_WebJsonData.json', '12-04-2022_14_WebJsonData.json', '12-04-2022_15_WebJsonData.json', '12-04-2022_16_WebJsonData.json', '12-04-2022_17_WebJsonData.json', '12-04-2022_18_WebJsonData.json', '12-04-2022_19_WebJsonData.json', '12-04-2022_1_WebJsonData.json', '12-04-2022_2_WebJsonData.json', '12-04-2022_3_WebJsonData.json', '12-04-2022_4_WebJsonData.json', '12-04-2022_5_WebJsonData.json', '12-04-2022_6_WebJsonData.json', '12-04-2022_7_WebJsonData.json', '12-04-2022_8_WebJsonData.json', '12-04-2022_9_WebJsonData.json', '13-04-2022_10_WebJsonData.json', '13-04-2022_11_WebJsonData.json', '13-04-2022_12_WebJsonData.json', '13-04-2022_13_WebJsonData.json', '13-04-2022_14_WebJsonData.json', '13-04-2022_15_WebJsonData.json', '13-04-2022_16_WebJsonData.json', '13-04-2022_17_WebJsonData.json', '13-04-2022_18_WebJsonData.json', '13-04-2022_19_WebJsonData.json', '13-04-2022_1_WebJsonData.json', '13-04-2022_2_WebJsonData.json', '13-04-2022_3_WebJsonData.json', '13-04-2022_4_WebJsonData.json', '13-04-2022_5_WebJsonData.json', '13-04-2022_6_WebJsonData.json', '13-04-2022_7_WebJsonData.json', '13-04-2022_8_WebJsonData.json', '13-04-2022_9_WebJsonData.json', '14-04-2022_10_WebJsonData.json', '14-04-2022_11_WebJsonData.json', '14-04-2022_12_WebJsonData.json', '14-04-2022_13_WebJsonData.json', '14-04-2022_14_WebJsonData.json', '14-04-2022_15_WebJsonData.json', '14-04-2022_16_WebJsonData.json', '14-04-2022_17_WebJsonData.json', '14-04-2022_18_WebJsonData.json', '14-04-2022_19_WebJsonData.json', '14-04-2022_1_WebJsonData.json', '14-04-2022_2_WebJsonData.json', '14-04-2022_3_WebJsonData.json', '14-04-2022_4_WebJsonData.json', '14-04-2022_5_WebJsonData.json', '14-04-2022_6_WebJsonData.json', '14-04-2022_7_WebJsonData.json', '14-04-2022_8_WebJsonData.json', '14-04-2022_9_WebJsonData.json']

now = datetime.now()
starttime = now.strftime("%H:%M:%S")

# ex.startScraping()

# for i in dateList:
#     dm.setDataByAllKeyword(i)
# now = datetime.now()
Endtime = now.strftime("%H:%M:%S")
print(starttime,Endtime)
# print(dm.currentLen)



# dm.startSearch(["16-04-2022","17-04-2022"],['anime','animation'])
# print(dm.currentLen)
# wt.start()



dm.addNewWordToAll(['Manga'])

# dm.delWordAllFile('kj')
#dm.addNewWord(['kk'],[datetime.date(2022, 3, 17), datetime.date(2022, 4, 19)])

# file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
# response = QFileDialog.getSaveFileName(
#         parent=None,
#         caption='Select a data file',
#         directory= 'fname.csv',
#         filter=file_filter,
#         initialFilter='Excel File (*.xlsx *.xls)'
#         )