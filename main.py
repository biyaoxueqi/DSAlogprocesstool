import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import UMCMcheck2
from UMCMcheckprocess import*
from DSAlogprocess import*
from E103checkprocess import*
import xlsxwriter


if __name__ == '__main__':
    def selectfile():
        Path = getpath()
        ui.lineEdit.setText(Path)
        #print(ui.lineEdit.text())
        return Path
    def umcmcheck():
        TF = ui.lineEdit.text()
        print(TF)
        DSA = DSAlogprocess(targetFile=TF)
        DSAData = CreatDataFrameFromDSAlog(DSAlog=DSA)
        finalResult = UMCMcheckresult(DSAData=DSAData)
        failResult = UMCMcheckfailresult(finalResult=finalResult)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        print(failResult)
        print(failResult.empty)
        if failResult.empty:
            ui.textBrowser.setText("All is ok")
        else:
            ui.textBrowser.setText(str(failResult))
        with pd.ExcelWriter(r'DSALogProcessResult.xlsx', engine='xlsxwriter') as writer:
            DSAData.to_excel(writer, sheet_name='DSALog')
            failResult.to_excel(writer, sheet_name='FailResult')

    def E103check():
        TF = ui.lineEdit.text()
        print(TF)
        DSA = DSAlogprocess(targetFile=TF)
        DSAData = CreatDataFrameFromDSAlog(DSAlog=DSA)
        checkresult = E103checkresult(DSAData=DSAData)
        #print(checkresult)
        checkfailresult = E103checkfailresult(E103checkresult=checkresult)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        print(checkfailresult)
        print(checkfailresult.empty)
        if checkfailresult.empty:
            ui.textBrowser.setText("All is ok")
        else:
            ui.textBrowser.setText(str(checkfailresult))
        with pd.ExcelWriter(r'DSALogProcessResult.xlsx', engine='xlsxwriter') as writer:
            DSAData.to_excel(writer, sheet_name='DSALog')
            checkfailresult.to_excel(writer, sheet_name='FailResult')
    def DSAlogoutput():
        TF = ui.lineEdit.text()
        print(TF)
        DSA = DSAlogprocess(targetFile=TF)
        DSAData = CreatDataFrameFromDSAlog(DSAlog=DSA)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        print(DSAData)
        ui.textBrowser.setText(str(DSAData))
        with pd.ExcelWriter(r'DSALogProcessResult.xlsx', engine='xlsxwriter') as writer:
            DSAData.to_excel(writer, sheet_name='DSALog')

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = UMCMcheck2.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.toolButton.clicked.connect(selectfile)
    ui.pushButton.clicked.connect(umcmcheck)
    ui.pushButton_2.clicked.connect(E103check)
    ui.pushButton_3.clicked.connect(DSAlogoutput)
    sys.exit(app.exec_())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
