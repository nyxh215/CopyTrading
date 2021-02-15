import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import MainFunctions as mf

form_class = uic.loadUiType("stock_regist.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(900,600)
        self.loginBtn.clicked.connect(self.loginBtn_clicked)
        self.dbBtn.clicked.connect(self.dbBtn_clicked)
        self.excelBtn.clicked.connect(self.excelBtn_clicked)
        self.getAllCodeBtn.clicked.connect(self.getAllCodeBtn_Clicked)
        self.getCodeBtn.clicked.connect(self.getCodeBtn_Clicked)
        self.getCodeDBBtn.clicked.connect(self.getCodeDBBtn_Clicked)
        self.getAllCodeDBBtn.clicked.connect(self.getAllCodeDBBtn_Clicked)
        self.codeListBtn.clicked.connect(self.codeListBtn_Clicked)

        self.mainFucntions = mf.MainFunctions()

    def loginBtn_clicked(self):
        pwd = self.pwdEdit.toPlainText()
        if pwd == "":
            QMessageBox.about(self, "로그인 실패", "패스워드를 입력하세요")
            self.listWidget.addItem(QListWidgetItem("패스워드를 입력하세요"))
            return
        if self.mainFucntions.db_login(pwd):
            QMessageBox.about(self, "로그인 성공", "로그인 성공")
            self.pwdEdit.setEnabled(False)
            self.loginBtn.setEnabled(False)
            self.dbBtn.setEnabled(True)
            self.listWidget.addItem(QListWidgetItem("로그인 성공"))
        else:
            QMessageBox.about(self, "로그인 실패", "패스워드를 다시 입력하세요")
            self.listWidget.addItem(QListWidgetItem("비밀번호가 틀렸습니다. 다시 입력하세요"))

    def dbBtn_clicked(self):
        code = self.codeEdit.toPlainText()
        if code == '':
            QMessageBox.about(self, "실패", "종목 코드를 입력하세요")
            self.listWidget.addItem(QListWidgetItem("종목 코드를 입력하세요"))
            return

        if self.mainFucntions.is_stock(code):
            QMessageBox.about(self, "입력 시작", "종목 데이터 전송을 시작하겠습니다.  OK를 눌러주세요")
            self.mainFucntions.db_insert_stock(code)
            QMessageBox.about(self, "입력 성공", "종목 데이터를 DB에 저장했습니다.")
            self.listWidget.addItem(QListWidgetItem("종목 데이터 전송 성공. DB에 데이터가 저장되었습니다."))

        else:
            QMessageBox.about(self, "실패", "종목 코드를 다시 입력하세요")
            self.listWidget.addItem(QListWidgetItem("종목 코드를 다시 입력하세요. 코드에 해당하는 종목이 없습니다."))

    def excelBtn_clicked(self):
        code = self.codeEdit.toPlainText()
        if code == '':
            QMessageBox.about(self, "실패", "종목 코드를 입력하세요")
            self.listWidget.addItem(QListWidgetItem("종목 코드를 입력하세요"))
            return
        if self.mainFucntions.is_stock(code):
            QMessageBox.about(self, "입력 시작", "종목 데이터 전송 시작을 시작하겠습니다.. OK를 눌러주세요")
            self.mainFucntions.data_to_excel(code)
            QMessageBox.about(self, "입력 성공", "종목 데이터 엑셀 파일을 다운로드했습니다.")
            self.listWidget.addItem(QListWidgetItem("종목 데이터 전송 성공. 엑셀에 데이터가 저장되었습니다."))
            self.listWidget.addItem(QListWidgetItem("이 프로그램 설치 위치에 엑셀 파일이 있습니다."))
        else:
            QMessageBox.about(self, "실패", "종목 코드를 다시 입력하세요")
            self.listWidget.addItem(QListWidgetItem("종목 코드를 다시 입력하세요. 코드에 해당하는 종목이 없습니다."))

    def getCodeBtn_Clicked(self):
        code = self.codeEdit.toPlainText()
        if code == '':
            QMessageBox.about(self, "실패", "종목 코드를 입력하세요")
            self.listWidget.addItem(QListWidgetItem("종목 코드를 입력하세요"))
            return
        if self.mainFucntions.is_stock(code):
            self.mainFucntions.Codelist_to_excel(code)
            self.listWidget.addItem(QListWidgetItem("종목 데이터 전송 성공. 엑셀에 데이터가 저장되었습니다."))
            self.listWidget.addItem(QListWidgetItem("이 프로그램 설치 위치에 엑셀 파일이 있습니다."))
        else:
            QMessageBox.about(self, "실패", "종목 코드를 다시 입력하세요")
            self.listWidget.addItem(QListWidgetItem("종목 코드를 다시 입력하세요. 코드에 해당하는 종목이 없습니다."))

    def getAllCodeBtn_Clicked(self):
        code = self.codeEdit.toPlainText()
        #QMessageBox.about(self, "입력 시작", "종목 데이터 전송 시작을 시작하겠습니다.. OK를 눌러주세요")
        self.mainFucntions.allList_to_excel()

        self.listWidget.addItem(QListWidgetItem("종목 데이터 전송 성공. 데이터가 저장되었습니다."))

    def getCodeDBBtn_Clicked(self):
        code = self.codeEdit.toPlainText()
        if code == '':
            QMessageBox.about(self, "실패", "종목 코드를 입력하세요")
            self.listWidget.addItem(QListWidgetItem("종목 코드를 입력하세요"))
            return
        if self.mainFucntions.is_stock(code):
            QMessageBox.about(self, "입력 시작", "종목 데이터 전송 시작을 시작하겠습니다.. OK를 눌러주세요")
            self.mainFucntions.CodeList_to_DB(code)
            self.listWidget.addItem(QListWidgetItem("종목 데이터 전송 성공. 데이터가 저장되었습니다."))
        else:
            QMessageBox.about(self, "실패", "종목 코드를 다시 입력하세요")
            self.listWidget.addItem(QListWidgetItem("종목 코드를 다시 입력하세요. 코드에 해당하는 종목이 없습니다."))

    def getAllCodeDBBtn_Clicked(self):

        self.mainFucntions.AllCodeList_to_DB()
        self.listWidget.addItem(QListWidgetItem("종목 데이터 전송 성공. 데이터가 저장되었습니다."))


    def codeListBtn_Clicked(self):
        self.listWidget.addItem(QListWidgetItem("CodeListSelect Test"))
        self.mainFucntions.CodeListUp()
        self.listWidget.addItem(QListWidgetItem("업종 리스트 데이터 저장 완료"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()