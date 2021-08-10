import os
import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog

def DSAlogprocess(targetFile):
    with open(targetFile, "r") as f:
        txtData = f.read()
    DSA = txtData.split('\n\n')
    i = 0
    while i < len(DSA):
        if "Complete Response:" not in DSA[i]:
            del DSA[i]
        else:
            i = i + 1
    return DSA

def CreatDataFrameFromDSAlog(DSAlog):
    ecu = [None] * len(DSAlog)
    response = [None] * len(DSAlog)
    timestamp = [None] * len(DSAlog)
    request = [None] * len(DSAlog)
    ecuaddress = [None] * len(DSAlog)
    i = 0
    while i < len(DSAlog):
        if "ECU:" in DSAlog[i]:
            str1=str(DSAlog[i])
            ECURules=re.compile(r"\/(\w*\s?\w*)\_APP")
            RespRules=re.compile(r'[Complete\sResponse:\s](\w{4}\s[5-7]\w\s\w\w\s\w\w[\s?\w?\w?]*)\n')
            TimeRules=re.compile(r'(\d{9})\n')
            ECUaddressRules=re.compile(r"[Complete\sResponse:\s](1\w\w\d\s)")
            RequestRules = re.compile(r'[Tester\-\>\s](\w{4}\s[1-3]\w\s\w\w\s\w\w\s?\w?\w?\s?\w?\w?)')
            ecu[i]=ECURules.search(str1).group(1)
            response[i]=RespRules.search(str1).group(1)
            timestamp[i]=TimeRules.search(str1).group(1)
            ecuaddress[i]=ECUaddressRules.search(str1).group(1)
            request[i]=RequestRules.search(str1).group(1)
            i=i+1

        else:
            str1 = str(DSAlog[i])
            ECURules = re.compile(r'\s(\w*\s?\w*)\_APP')
            RespRules = re.compile(r'[Complete\sResponse:\s](\w{4}\s[5-9]\w\s\w\w\s\w\w[\s?\w?\w?]*)\n')
            TimeRules = re.compile(r'(\d{9})\n')
            ECUaddressRules = re.compile(r"[Complete\sResponse:\s](1\w\w\d\s)")
            RequestRules = re.compile(r'[Tester\-\>\s](\w{4}\s[1-3]\w\s\w\w\s\w\w[\s?\w?\w?]*)')
            ecu[i] = ECURules.search(str1).group(1)
            response[i] = RespRules.search(str1).group(1)
            timestamp[i] = TimeRules.search(str1).group(1)
            ecuaddress[i] = ECUaddressRules.search(str1).group(1)
            request[i]=RequestRules.search(str1).group(1)

            i=i+1

    DSAData = pd.DataFrame.from_dict(dict([("ECU",ecu),("ECU address",ecuaddress),("request",request),("response",response)]))
    #DSAData.to_excel('DSAData.xlsx')
    return DSAData

def getpath():
    root = tk.Tk()
    root.withdraw()
    Filepath = filedialog.askopenfilename() #获得选择好的文件
    #print(Filepath)
    return Filepath

if __name__ == '__main__':
    # sourceFolder = "D:\\Python\\DSA处理工具"
    # logName = "506 Usage&Carmode resp 6-10.txt"
    Path = getpath()
    DSA = DSAlogprocess(targetFile= Path)
    DSAData = CreatDataFrameFromDSAlog(DSAlog=DSA)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print (DSAData)





