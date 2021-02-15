import Kiwoom as kw
import StockDB as db
from datetime import date, timedelta


class MainFunctions():

    def __init__(self):
        self.ki = kw.Kiwoom()
        self.dB = db.StockDB()

        self.date = date.today() - timedelta(1)

    def db_login(self,password):
        return self.dB.init(password)

    def is_stock(self,code):
        if code == 'kospi' or code == 'kosdaq' or  self.ki.is_stock(code) != "":
            return True
        else:
            return False

    def db_insert_stock(self, code):
        print("insertStock : "+code)
        table_name = ""
        if code == 'kospi':
            table_name = code
            code = '001'

        elif code == 'kosdaq':
            table_name = code
            code = '101'

        else:
            table_name= 'a'+code

        # 테이블이 생성되지 않았으면 테이블 생성
        self.dB.create_table(table_name)
        # 테이블에 입력된 데이터 중 가장 최근 날짜 획득
        recent_day = self.dB.select_max_date(table_name)
        print(recent_day)
        print(self.date)

        if recent_day == self.date:
            return

        #  일봉 데이터 획득
        if code == '001' or code == '101':
            data = self.ki.req_index_daily_value(code, recent_day)
        else:
            data = self.ki.req_stock_daily_value(code, recent_day)
        # 테이블에 데이터 insert
        self.dB.insert_chart(data, table_name)

    def db_insert_main(self, code):
        print("insertStockMain : "+code)

        table_name= 'codedaily'

        # 테이블에 입력된 데이터 중 가장 최근 날짜 획득
        recent_day = self.dB.select_code_date_chk(code)
        if recent_day is None:
            startDate = date.fromisoformat('2015-12-31')
            recent_day = startDate

        print("보유 최신 데이터 일자 : ",recent_day)
        print("요청 데이터 일자 : ",self.date)

        if recent_day == self.date:
            return

        data = self.ki.req_stock_daily_main(code, recent_day)
        # 테이블에 데이터 insert
        #print("Call Test")
        self.dB.insert_chart(data, table_name)
        #print("DB Insert Test")

    def data_to_excel(self,code):
        if code == 'kospi':
            # 코스피 일봉 데이터 획득
            data = self.ki.req_index_daily_value('001', None)
            data.to_excel('./kospi.xlsx')
        elif code == 'kosdaq':
            # 코스닥 일봉 데이터 획득
            data = self.ki.req_index_daily_value('101', None)
            data.to_excel('./kosdaq.xlsx')
        else:
            # 종목 일봉 데이터 획득
            data = self.ki.req_stock_daily_value(code, None)
            data.to_excel('./a'+code+'.xlsx')

    def Codelist_to_excel(self,code):
        data = self.ki.req_stock_base_value(code)
        data.to_excel('./codeList.xlsx')

    def allList_to_excel(self):
        data = self.ki.req_stock_allCode_value()
        data.to_excel('./codeAllList.xlsx')

    def CodeList_to_DB(self,code):
        table_name = 'codemaster'
        data = self.ki.req_stock_base_value(code)
        self.dB.insert_master(data,table_name)

    def AllCodeList_to_DB(self):
        table_name = 'codemaster'
        data = self.ki.req_stock_allCode_value()
        #print(data)
        self.dB.insert_master(data,table_name)

    def CodeListUp(self):
        data = self.dB.select_code()
        #print(data)

        for res in data:
            #print(res['CODE_ID'])
            self.db_insert_main(res['CODE_ID'])
