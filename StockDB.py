from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd

class StockDB():
    def init(self, password):
        if self._create_database(password) is False:
            return False
        self.engine = create_engine("mysql+mysqldb://root:"+password+"@localhost/stock", encoding='utf-8')
        self.conn = pymysql.connect(host='localhost', user='root', password=password, db='stock', charset='utf8')
        self.cursor = self.conn.cursor()
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        return True

    def _create_database(self,password):
        try:
            conn = pymysql.connect(host='localhost', user='root', password=password, charset='utf8')
            cursor = conn.cursor()

            sql = 'SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = \'stock\''
            result = cursor.execute(sql)

            if result == 0:
                sql = 'CREATE DATABASE stock'
                cursor.execute(sql)
                conn.commit()
        except:
            return False
        return True


    def close(self):
        self.conn.close()

    def select_max_date(self,table_name):
        sql = 'select max(Date) from ' + table_name
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result[0]

    def select_code_date_chk(self,code):
        sql = "select max(Date) from codedaily where code_id='" +code+ "';"
        #print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result[0]

    def insert_chart(self,data, table_name):
        data.to_sql(name=table_name, con=self.engine, if_exists='append')
        self.conn.commit()


    def create_table(self,table_name):
        sql = 'SHOW TABLES LIKE \'' + table_name + '\''
        result = self.cursor.execute(sql)
        if result == 0:
            sql = 'create table ' + table_name + '(Date date primary key,Open Decimal,High Decimal,Low Decimal,Close Decimal, Volume Decimal);'
            self.cursor.execute(sql)
            self.conn.commit()

    def insert_master(self,data,table_name):
        #print(data)
        data.to_sql(name=table_name, con=self.engine, if_exists='append')
        self.conn.commit()

    def select_code(self):
        sql = 'SELECT CODE_ID FROM CODEMASTER WHERE MARKET_CAP < 5000;'

        self.curs.execute(sql)
        result = self.curs.fetchall()

        return result
