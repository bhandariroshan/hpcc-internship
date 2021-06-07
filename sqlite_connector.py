import sqlite3
from sqlite3 import Error


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
                    time,  region,  size, api_price, cli_price, one_year_reserved_price, 
                    three_year_reserved_price, pay_as_you_go_price, per_saving_pay_as_you_go,
                    per_saving_1y_reserved, per_saving_3y_reserved
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
                time,  region,  size, api_price, cli_price, one_year_reserved_price, 
                three_year_reserved_price, pay_as_you_go_price, per_saving_pay_as_you_go,
                per_saving_1y_reserved, per_saving_3y_reserved
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?) 
        '''

        dat = None
        with self.conn:
            self.cur.execute(sql, benchmark)
            self.conn.commit()
            dat = self.cur.lastrowid

        return dat

