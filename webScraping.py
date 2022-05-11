from csv import DictWriter, writer
import csv
from datetime import date
import datetime
from datetime import datetime
import os
from textwrap import wrap
from turtle import ht
from bs4 import BeautifulSoup
import requests
from soupsieve import escape
import re
import pandas as pd
from urllib.parse import urlparse
import json
import urllib.robotparser
import DataManager
from langdetect import detect
import langdetect
from collections import Counter
# from testCookie import write, writeJson
class webScraping():
    def __init__(self):
        self.keyword = os.listdir("collectkeys")
        # self.web = [
        #             "https://www.animenewsnetwork.com/",
        #             "https://www.cbr.com/category/anime-news/",
        #             "https://myanimelist.net/",
        #             "https://otakumode.com/news/anime",
                    
        #             "https://news.dexclub.com/",
        #             "https://my-best.in.th/49872",
        #             "https://www.anime-japan.jp/2021/en/news/",
        #             "https://todayanimenews.com",
                    
        #             "https://anime-news.tokyo/" ,
                    
        #             "https://manga.tokyo/news/",
                    
        #             "https://www.bbc.com/news/topics/c1715pzrj24t/anime",
        #             "https://www.independent.co.uk/topic/anime",
        #             "https://soranews24.com/tag/anime/",
        #             "https://anitrendz.net/news/",
        #             "https://thebestjapan.com/the-best-of-japan/anime-fans/",
        #             "https://wiki.anime-os.com/chart/all-2020/",
        #             "https://kwaamsuk.net/10-anime-netflix/",
        #             "https://www.online-station.net/anime/326294/",
        #             "https://th.kokorojapanstore.com/blogs/blogs/35-best-anime-of-all-time-new-and-old-in-2021",
        #             "https://www.metalbridges.com/cool-anime-songs/"
        #             ] 
        self.web = ["https://www.animenewsnetwork.com/"
                    ]
        # self.web = ["https://www.animenewsnetwork.com/","https://www.cbr.com/",
        #             "https://myanimelist.net/","https://otakumode.com/"
        #             ]
        
        # self.web = ["https://www.animenewsnetwork.com/"]    
        self.SaveFileName = "_WebJsonData.json"
        self.soupList = []
        self.dfdict = {"Page Title": [] ,"Page Date":[],"Page Data":[],"Page Image":[],"Page Link":[]}
        self.df = pd.DataFrame.from_dict(self.dfdict)
        self.MainDomain = ""
        self.currentLink = ""
        self.subLink = []
        self.refLink = []
    # def setCurLink(self,Link):
    #     self.currentLink = Link
    
    # def getCurLink(self):
    #     return self.currentLink
    
    def setFileName(self,newName):
        self.SaveFileName = newName
        
    def getFileName(self):
        return self.SaveFileName
    
    def getPath(self,path,fileName): #return path
        fileJsonName = fileName #self.SaveFileName
        path = os.path.join(path,(str(self.getTodayDate())+fileJsonName))
        return path
    
    def setMainDomain(self,link): #set Web Domain
        domain = urlparse(link).netloc
        self.MainDomain = "https://" + str(domain)
    
    def getMainDomain(self): #set Web Domain
        return self.MainDomain
    
    def getStatus(self,link): #get status code of link 
        req = requests.get(link)
        if req.status_code == 200:
            return True
        else:
            return False
    
    def canFetch(self,link): # False - if can get data
        rp = urllib.robotparser.RobotFileParser()
        result = rp.can_fetch("*", link)
        return result
    
    def setSubLink(self,soup): #find down level of link(soup)
        # print("in")
        refl = []
        subl = []
        # n = len(soup.find_all('a', href=True))
        for link in soup.find_all('a', href=True):
            # print(n)
            # n-=1
            if urlparse(link['href']).netloc == self.MainDomain:
                if self.canFetch(link['href']) == False:
                    subl.append(link['href'])
                # print(link['href'])
            elif urlparse(link['href']).netloc == "":
                if self.canFetch(self.MainDomain + link['href']) == False:
                    subl.append(self.MainDomain + link['href'])
                # print(self.MainDomain + link['href'])
            else:
                if self.canFetch(link['href']) == False:
                    refl.append(link['href'])
                # print(link['href'])
        # print("Href Type : ",type(href[0]))
        self.subLink = list(set(subl))
        self.refLink = list(refl)
    
    def getAllSubLink(self): #return down level
        return self.subLink
    
    def getAllRefLink(self):#return link down level different domain
        return self.refLink
        
    def getLang(self,soup): # get Langeuge
        try:
            for link in soup.find_all('html', lang=True):
                # print(link['lang'])
                return link['lang']
        except :
            return "Don't Set"
    
    def getTodayDate(self): # get today Date
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        return d1
    
    def getTitle(self,soup): #get web title
        # for t in self.soupList:
        if soup != None:
            for i in soup.find_all('title'):            
                return i.text.strip()
        else:
            return "None Title"
    
    def makeSoup(self,link):# Make soup
        try:
            req = requests.get(link)
            if req.status_code == 200:
                req.encoding = "utf-8"
                soup = BeautifulSoup(req.text,"html.parser")
                self.soupList.append(soup)
                return soup
        except :
            print("Error makeSoup",link)
            # print(req)
            pass
        # print(self.soupList)
        # else: return None
        
    def getDomain(self,link): #get web domain
        domain = urlparse(link).netloc
        return str(domain)
        
    def getFullLink(self,href): #get Full web By href
        if urlparse(href).netloc == self.MainDomain:
            return 'https://'+str(href)
        elif urlparse(href).netloc == "":
            # if self.getStatus(self.MainDomain + link['href']):
            return 'https://'+self.MainDomain + str(href)
        else:
            return ""
        
    # def getSubLink(self,tag): 
    #     Alink = tag.find_all('a', href = True)
    #     wrapTag = tag.previous_element.previous_element
    #     dictForJson = {}
    #     for ListAlink in Alink:
    #         try:
    #             soup = self.makeSoup(self.getFullLink(ListAlink['href']))
    #             if self.getFullLink(ListAlink['href']) not in dictForJson.keys():
    #                 dictForJson.update({self.getFullLink(ListAlink['href']):{'Lang': self.getLang(soup),
    #                                                                     'Title' : self.getTitle(soup),
    #                                                                     'Ref' : 0,
    #                                                                     'Data' : self.getDataList(soup)
    #                                                                     }})
    #             else:
    #                 # print("Dub")
    #                 dictForJson[self.getFullLink(ListAlink['href'])]['Ref'] += 1
    #         except :
    #             pass
    #     return dictForJson
    
    
    def writeJson(self,dictForWrite): #write Json By Dict
            #Over write
        with open(self.getPath("WebData",self.SaveFileName),"w") as f:
            json.dump(dictForWrite,f)
        f.close()
        
    def writeCsvByList(self,path,dataList): #write CSV By List
        # Open file in append mode
        with open(path, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(dataList)
            print("... Save List to ",path,"  successful.")
    
    def writCsvByDict(self,path,head,dict): #write CSV By Dict
        print("Dict in write")
        with open(path, 'a+', newline='', encoding="utf-8") as f:
            print("Dict in write")
            dictwriter_object = DictWriter(f, fieldnames=head)
            dictwriter_object.writerow(dict)
            print("\n... Save Dict to ",path,"  successful.")
            f.close()
    
    def creatNewSearchFile(self,path): #Creat Bast file for search
        field_names = ['Date','Keyword','Word Count','Ref','Link','Title','Data','Sentiment','Lang','Ref Link']
        with open(path, 'a+', newline='', encoding="utf8") as f: 
            write = csv.writer(f) 
            write.writerow(field_names)
            f.close()
    
    def setDataByKeyWord(self,soup,data): # for old data to search format
        dm = DataManager.DataManager()
        today = self.getTodayDate()
        field_names = ['Date','Keyword','Word Count','Ref','Link','Title','Data','Sentiment','Lang','Ref Link']
        # print("Data : ",data)
        try:
            wc = dm.paragraphToList(data)
            
            stm = ''
            if detect(data) == 'th':
                stm = dm.getSentimentTH(data)
            elif detect(data) == 'en':
                stm = dm.getSentimentENG(data)
                
            newpath = os.path.join('web search',today)
            if not os.path.exists(newpath):
                print("File not exist Taday Folder")
                os.makedirs(newpath)
            
            for i in self.keyword:
                newpath = os.path.join('web search',today,i+'.csv')
                if not os.path.exists(newpath):
                    print("File not exist File ",i+'.csv')
                    self.creatNewSearchFile(newpath)
                    
            for tuplew in wc:
                if tuplew[0] in self.keyword:
                    i = tuplew[0]
                    wcCount = tuplew[1]
                    # print("Lang : ",detect(data))
                    if stm != '':
                        dfdict = {'Date':today,
                            'Keyword':i,
                            'Word Count':wcCount,
                            'Ref':0,'Link':self.currentLink,
                            'Title':self.getTitle(soup),
                            'Data':data,
                            'Sentiment':stm,
                            'Lang':self.getLang(soup),
                            'Ref Link':dict(Counter(self.getAllRefLink()))}
                        # print(data)
                        print("----------",i,tuplew)
                        
                        # print(df)
                        savePath = os.path.join("web search",today,i+'.csv') 
                        
                        # dataraw = pd.read_csv(newpath)
                        # newdata = dataraw.drop_duplicates()
                        # newdata.to_csv(savePath, encoding='utf-8', index=False)
                        
                        try:
                            filesize = dm.getCountCsvLine(savePath)
                        except :
                            filesize = 1000
                            pass
                        if filesize >= 1000:
                            n=1
                            newname = os.path.join("web search",today,i+"("+str(n)+")"+'.csv')
                            while os.path.exists(newname):
                                n+=1
                                newname = os.path.join("web search",today,i+"("+str(n)+")"+'.csv')
                            self.renameFile(savePath,newname)
                            self.creatNewSearchFile(savePath)
                        
                        self.writCsvByDict(savePath,field_names,dfdict)
                    
                    # else:
                    #     os.system('clear')
        except langdetect.lang_detect_exception.LangDetectException:
            print("\n******* Error Data : ",data)
            pass
                    
    def renameFile(self,oldpath,newpath): # Rename file
        os.rename(oldpath, newpath)
        
    def getDataList(self,soup): #Get data in List format
        # print(len(soup))
        # try:
        divClass = soup.find_all('div')
        n = len(divClass)
        # return [ i.text.replace("\n"," ") for i in divClass]
        resualt = []
        for i in divClass:
            print("\t\tData List",n)
            n-=1
            data = i.text.replace("\n"," ")
            resualt.append(data)
            # self.setDataByKeyWord(soup,data)   
        return resualt    
        
    def startScraping(self): #Scraping web data today
        now = datetime.now()
        starttime = now.strftime("%H:%M:%S")
        # countWeb = len(self.web)
        countWeb = 0
        for link in self.web:
            print(link)
            try:
                countWeb += 1
                dictForJson = {}
                soup = self.makeSoup(link)
                self.setMainDomain(link)
                self.setSubLink(soup)
                self.currentLink = link
                dictForJson[self.getTodayDate()] = { link : {'Lang' : self.getLang(soup),
                                                            'Title' : self.getTitle(soup),
                                                            # 'Sub' : len(self.getAllSubLink()),
                                                            'Ref' : dict(Counter(self.getAllRefLink())),
                                                            'Data' : self.getDataList(soup)
                                                            }
                                                    }
                self.SaveFileName = "_"+str(countWeb)+"_WebJsonData.json"
                # countWeb += 1
                sl = self.getAllSubLink()
                n = len(sl)
                for i in sl:
                    print("\t",n)
                    n-=1
                    try:
                        soup = self.makeSoup(i)
                        self.setSubLink(soup)
                        self.currentLink = i
                        dictForJson[self.getTodayDate()].update({ i : {'Lang': self.getLang(soup),
                                                'Title' : self.getTitle(soup),
                                                # 'Sub' : len(self.getAllSubLink()),
                                                'Ref' : dict(Counter(self.getAllRefLink())),
                                                'Data' : self.getDataList(soup)
                                                }
                                                })
                        ##
                        # ssl = len(self.getAllSubLink())
                        # for j in self.getAllSubLink():
                        #     print("\t\t",ssl)
                        #     ssl -= 1
                        #     try:
                        #         soup = self.makeSoup(j)
                        #         self.setSubLink(soup)
                        #         dictForJson[self.getTodayDate()].update({ j : {'Lang': self.getLang(soup),
                        #                                 'Title' : self.getTitle(soup),
                        #                                 # 'Sub' : len(self.getAllSubLink()),
                        #                                 'Ref' : dict(Counter(self.getAllRefLink())),
                        #                                 'Data' : self.getDataList(soup)
                        #                                 }
                        #                                 })
                        #     except :
                        #         pass
                        ##
                    except :
                        pass
                    # print(json.dumps(dictForJson, indent=4))
                    # now = datetime.now()
                    # Endtime = now.strftime("%H:%M:%S")
                    # print(starttime,Endtime)
                self.writeJson(dictForJson)
            except :
                pass
        now = datetime.now()
        Endtime = now.strftime("%H:%M:%S")
        print(starttime,Endtime)
    
    