import sqlite3
from sqlite3 import Error
import pandas as pd


class SqliteConnector(object):
    def __init__(self, db_file=r"sqlite.db"):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS benchmark
                (
                   time,  region,  size, api_price, cli_price, pay_as_you_go_price, one_year_reserved_price, 
                    three_year_reserved_price, percent_saving_pay_as_you_go,
                    percent_saving_1y_reserved, percent_saving_3y_reserved
                )
            ''')
        except Error as e:
            print(e) 


    def create_benchmark(self, benchmark):
        """
        Create a new benchmark into the benchmark table
        :param conn:
        :param benchmark:
        :return: benchmark id
        """ 
        sql = ''' 
            INSERT INTO benchmark(
                time,  region,  size, api_price, cli_price, pay_as_you_go_price, one_year_reserved_price, 
                three_year_reserved_price, percent_saving_pay_as_you_go,
                percent_saving_1y_reserved, percent_saving_3y_reserved
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?) 
        '''

        dat = None
        with self.conn:
            self.cur.execute(sql, benchmark)
            self.conn.commit()
            dat = self.cur.lastrowid

        return dat

    def select_data_as_dataframe(self, region, size):
        filter = ''
        if region:
            filter += " where region='" + str(region)  + "'"

            if size:
                filter += " and size='" + str(size) + "'"

        if size and not region:
            filter += " where size='" + str(size) + "'"

        query = "Select * from benchmark " + filter + ";"

        dat = None
        with self.conn:
            dat = pd.read_sql_query(query, self.conn)

        return dat

