from datetime import datetime
import json
import os
from urllib.parse import urlparse
from PyQt5 import QtCore
import DataManager
from pythainlp import word_tokenize
import pandas as pd
import time
import DataManager as data
# import progress
import sys, time
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
dm = data.DataManager()
class WebThread(QThread):
    any_signal = pyqtSignal(int)
    dm = data.DataManager()
    def __init__(self, parent=None,sdate=None,edate=None,kw=None):
        super(WebThread, self).__init__(parent)
        # QThread.__init__(self, parent)
        self.sdate = sdate
        self.edate = edate
        self.keyword = kw
        self.val = 0
        self.FullLen =  1
        self.currentLen = 0
        # self.any_signal = QtCore.pyqtSignal(float)
        self.result = pd.DataFrame()
        self.is_running = True
        
    def getDf(self):
        # return self.startSearch([self.sdate,self.edate],self.keyword)
        return self.result.sample(frac=1).reset_index(drop=True)
            
    def run(self):
    
        ListOfDate = dm.date_range(self.sdate,self.edate)
        # print("List Of Date : ",ListOfDate)
        # print("List Of Word : ",self.keyword)
        dfResult = []
        self.FullLen =  len(ListOfDate)+1
        self.currentLen = 0
        path = "web search"
        checkDate = os.listdir(path)
        # print("checkDate : ",checkDate)
        for j in ListOfDate:
            # print("Date Type",j,type(j))
            if j in checkDate:
                for kw in self.keyword:
                    # print("kw in self.keyword",j,kw)
                    fileListForSearch = dm.getReadByKeyword(j,kw) #List of DataFrame
                    # print("Return : ",fileListForSearch)
                    if len(fileListForSearch)!=0 :
                        dfResult += fileListForSearch
                        print("Len Dataframe :",len(dfResult),len(fileListForSearch))
                        print("\n-------------------- ConCat --------------------")
                        newDf = pd.concat(dfResult,ignore_index=True)
                        field_names = ['Date','Keyword','Word Count','Ref','Link','Title','Data','Sentiment','Lang','Ref Link']
                        newDf.sort_values(field_names)
                        self.result = newDf
                        self.result = self.result.drop_duplicates()
                        print("thread result : ",len(self.result))
            self.currentLen += 1
            self.val = (self.currentLen/self.FullLen)*100
            print(self.currentLen,"/",self.FullLen)
            self.any_signal.emit(self.val)
        
        # for i in range(len(self.result)):
        #     getRef = self.result.iloc[i]['Ref Link']
        #     getRef = getRef.replace("'",'"')
        #     getRef = json.loads(getRef)
        #     # print(type(getRef),getRef)
            
        #     for linkKey in getRef.keys():
        #         # linkKey = urlparse(linkKey).netloc
        #         # linkKey = "https://"+linkKey
        #         print(linkKey)
        #         self.result.loc[self.result['Link'].isin([linkKey])] = str(int(getRef[linkKey])+int(self.result.loc[self.result['Link'].isin([linkKey])]))
        #         # self.result.iloc[i]['Ref Link']
        self.val = 100 
        self.any_signal.emit(self.val)
            # if len(dfResult)>0:
            #     # print(dfResult)
            #     print("\n-------------------- ConCat --------------------")
            #     newDf = pd.concat(dfResult,ignore_index=True)
            #     field_names = ['Date','Keyword','Word Count','Ref','Link','Title','Data','Sentiment','Lang','Ref Link']
            #     newDf.sort_values(field_names)
            #     self.result = newDf
            #     self.result = self.result.drop_duplicates()
            #     print("thread result : ",len(self.result))
        # self.stop()
    def stop(self):
        self.is_running = False
        print('Stopping Web thread...')
        self.any_signal.emit(0)    
        self.terminate()
