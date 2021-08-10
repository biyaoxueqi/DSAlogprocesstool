import os
from typing import Pattern
import pandas as pd
import xlsxwriter
from DSAlogprocess import DSAlogprocess,CreatDataFrameFromDSAlog,getpath
#from DSAlogprocess import CreatDataFrameFromDSAlog
import re

def UMCMcheckresult(DSAData):
    oder = [None] * len(DSAData)
    expectresult = [None] * len(DSAData)
    result = [None] * len(DSAData)
    status = [None] * len(DSAData)
    i = 0
    while i < len(DSAData):
        if '1A01 2F DD 0A 03 01' in DSAData['request'][i]:
            oder[i] = 'set usgmode to inactive'
            expectresult[i] = 'inactive'
            if '1A01 6F DD 0A 03 01' in DSAData['response'][i]:
                status[i] = 'inactive'
                # result[i] = 'OK'
            else:
                status[i] = 'unknown'
                # result[i] = 'NOK'
            # flag[0] = i
            i = i + 1
        elif '1A01 2F DD 0A 03 02' in DSAData['request'][i]:
            oder[i] = 'set usgmode to convenience'
            expectresult[i] = 'convenience'
            if '1A01 6F DD 0A 03 02' in DSAData['response'][i]:
                status[i] = 'convenience'
                # result[i] = 'OK'
            else:
                status[i] = 'unknown'
                # result[i] = 'NOK'
            # flag[1] = i
            i = i + 1

        elif '1A01 2F DD 0A 03 0B' in DSAData['request'][i]:
            oder[i] = 'set usgmode to active'
            expectresult[i] = 'active'
            if '1A01 6F DD 0A 03 0B' in DSAData['response'][i]:
                status[i] = 'active'
                # result[i] = 'OK'
            else:
                status[i] = 'unknown'
                # result[i] = 'NOK'
            # flag[3]= i
            i = i + 1
        elif '1A01 2F DD 0A 03 0D' in DSAData['request'][i]:
            oder[i] = 'set usgmode to driving'
            expectresult[i] = 'driving'
            if '1A01 6F DD 0A 03 0D' in DSAData['response'][i]:
                status[i] = 'driving'
                # result[i] = 'OK'
            else:
                status[i] = 'unknown'
                # result[i] = 'NOK'
            # flag[2]= i
            i = i + 1
        elif '1A01 2F D1 34 03 00' in DSAData['request'][i]:
            oder[i] = 'set carmode to normal'
            expectresult[i] = 'normal'
            if '1A01 6F D1 34 03 00' in DSAData['response'][i]:
                status[i] = 'normal'
                # result[i] = 'OK'
            else:
                status[i] = 'unknown'
                # result[i] = 'NOK'
            # flag[7] = i
            i = i + 1
        elif '1A01 2F D1 34 03 01' in DSAData['request'][i]:
            oder[i] = 'set carmode to transport'
            expectresult[i] = 'transport'
            if '1A01 6F D1 34 03 01' in DSAData['response'][i]:
                status[i] = 'transport'
                # result[i] = 'OK'
            else:
                status[i] = 'unknown'
                # result[i] = 'NOK'
            # flag[4]= i
            i = i + 1
        elif '1A01 2F D1 34 03 02' in DSAData['request'][i]:
            oder[i] = 'set carmode to factory'
            expectresult[i] = 'factory'
            if '1A01 6F D1 34 03 02' in DSAData['response'][i]:
                status[i] = 'factory'
                # result[i] = 'OK'
            else:
                status[i] = 'unknown'
                # result[i] = 'NOK'
            # flag[5]= i
            i = i + 1
        elif '1A01 2F D1 34 03 05' in DSAData['request'][i]:
            oder[i] = 'set carmode to Dyno'
            expectresult[i] = 'Dyno'
            if '1A01 6F D1 34 03 05' in DSAData['response'][i]:
                status[i] = 'Dyno'
                # result[i] = 'OK'
            else:
                status[i] = 'unknown'
                # result[i] = 'NOK'
            # flag[6]= i
            i = i + 1
        elif '1FFF 22 DD 0A' in DSAData['request'][i]:
            oder[i] = 'read usgmode'
            if '62 DD 0A 01' in DSAData['response'][i]:
                status[i] = 'inactive'
            elif '62 DD 0A 02' in DSAData['response'][i]:
                status[i] = 'convenience'
            elif '62 DD 0A 0B' in DSAData['response'][i]:
                status[i] = 'active'
            elif '62 DD 0A 0D' in DSAData['response'][i]:
                status[i] = 'driving'
            elif '7F 22' in DSAData['response'][i]:
                status[i] = 'nagtive response'
                result[i] = 'NOK'
            else:
                status[i] = 'unknown'
                result[i] = 'NOK'
            i = i + 1
        elif '1FFF 22 D1 34' in DSAData['request'][i]:
            oder[i] = 'read carmode'
            if '62 D1 34 00' in DSAData['response'][i]:
                status[i] = 'normal'
            elif '62 D1 34 01' in DSAData['response'][i]:
                status[i] = 'transport'
            elif '62 D1 34 02' in DSAData['response'][i]:
                status[i] = 'factory'
            elif '62 D1 34 05' in DSAData['response'][i]:
                status[i] = 'Dyno'
            elif '7F 22' in DSAData['response'][i]:
                status[i] = 'nagtive response'
                result[i] = 'NOK'
            else:
                status[i] = 'unknown'
                result[i] = 'NOK'
            i = i + 1
        else:
            oder[i] = 'unknown'
            i = i + 1
    i = 1
    while i < len(expectresult):
        if expectresult[i] == None and oder[i] != 'unknown':
            expectresult[i] = expectresult[i - 1]
            i = i + 1
        elif oder[i] == 'unknown':
            expectresult[i] = 'no expect result'
            i = i + 1
        else:
            i = i + 1

    i = 0
    while i < len(result):
        if oder[i] == 'unknow':
            result[i] = 'no expect result'

        elif status[i] == expectresult[i]:
            result[i] = 'OK'

        else:
            result[i] = 'NOK'
        i = i + 1


    finalResult = pd.DataFrame.from_dict(dict(
        [('ECU', DSAData['ECU']), ('ECU address', DSAData['ECU address']), ("REQ", DSAData['request']),
         ('request', oder), ("RESP", DSAData['response']), ('expect result', expectresult), ('status', status),
         ('result', result)]))
    return finalResult

def UMCMcheckfailresult(finalResult):
    failECU = []
    failECUAddress = []
    failrequest = []
    failresponse = []
    failresult = []
    failexpectresult = []
    failstatus = []
    i = 0
    while i < len(finalResult):
        if finalResult['result'][i] == 'NOK':
            failECU.append(finalResult['ECU'][i])
            failECUAddress.append(finalResult['ECU address'][i])
            failrequest.append(finalResult['REQ'][i])
            failresponse.append(finalResult['RESP'][i])
            failresult.append(finalResult['result'][i])
            failexpectresult.append(finalResult['expect result'][i])
            failstatus.append(finalResult['status'][i])
        i = i + 1
    failData = pd.DataFrame.from_dict(
        {"ECU": failECU, 'ECUaddress': failECUAddress, 'request': failrequest, 'response': failresponse,
         'expect result': failexpectresult, 'status': failstatus, 'result': failresult})
    return failData

if __name__ == '__main__':
    # sourceFolder = "D:\\Python\\DSA处理工具"
    # logName = "506 Usage&Carmode resp 6-10.txt"
    Path = getpath()
    DSA = DSAlogprocess(targetFile=Path)
    DSAData = CreatDataFrameFromDSAlog(DSAlog=DSA)
    finalResult = UMCMcheckresult(DSAData=DSAData)
    failResult = UMCMcheckfailresult(finalResult=finalResult)


    # print (DSAData)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print (finalResult)
    print (failResult)
    #failResult.to_excel('FAIL.xlsx')
    with pd.ExcelWriter(r'DSALogProcess.xlsx', engine='xlsxwriter') as writer:
        DSAData.to_excel(writer, sheet_name='DSALog')
        failResult.to_excel(writer, sheet_name='FailResult')
