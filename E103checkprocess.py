import os
from typing import Pattern
import pandas as pd
from DSAlogprocess import *
import re

def E103checkresult(DSAData):
    oder = [None] * len(DSAData)
    #expectresult = [None] * len(DSAData)
    result = [None] * len(DSAData)
    #status = [None] * len(DSAData)
    i = 0
    while i < len(DSAData):
        if '22 E1 03' in DSAData['request'][i]:
            oder[i] = 'Read carconfig fault'
            if '62 E1 03 00' in DSAData['response'][i]:
                result[i] = 'OK'
            else:
                result[i] = 'NOK'
            i = i + 1
        else:
            oder[i] = 'unknown'
            result[i] = 'unknown'
            i = i + 1


    E103checkresult = pd.DataFrame.from_dict(dict(
        [('ECU', DSAData['ECU']), ('ECU address', DSAData['ECU address']), ("REQ", DSAData['request']),
         ('request', oder), ('result', result),("RESP", DSAData['response'])]))
    return E103checkresult

def E103checkfailresult(E103checkresult):
    failECU = []
    failECUAddress = []
    failrequest = []
    failoder = []
    failresult = []
    failresponse = []
    i = 0
    while i < len(E103checkresult):
        if E103checkresult['result'][i] == 'NOK':
            failECU.append(E103checkresult['ECU'][i])
            failECUAddress.append(E103checkresult['ECU address'][i])
            failrequest.append(E103checkresult['REQ'][i])
            failoder.append(E103checkresult['request'][i])
            failresult.append(E103checkresult['result'][i])
            failresponse.append(E103checkresult['RESP'][i])
        i = i + 1
    E103failData = pd.DataFrame.from_dict(
        {"ECU": failECU, 'ECUaddress': failECUAddress, 'request': failrequest,
          'REQ Status': failoder, 'result': failresult, 'response': failresponse})
    return E103failData

if __name__ == '__main__':
    # sourceFolder = "D:\\Python\\DSA处理工具"
    # logName = "506 Usage&Carmode resp 6-10.txt"
    Path = getpath()
    DSA = DSAlogprocess(targetFile=Path)
    DSAData = CreatDataFrameFromDSAlog(DSAlog=DSA)
    E103checkresult = E103checkresult(DSAData=DSAData)
    E103failResult = E103checkfailresult(E103checkresult=E103checkresult)


    # print (DSAData)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print (E103checkresult)
    print (E103failResult)
    E103failResult.to_excel('E103FAIL.xlsx')
