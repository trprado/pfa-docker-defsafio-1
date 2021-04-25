import sys
import logging
import config
import pymysql

logging.basicConfig(filename='db.log', level=logging.DEBUG)

class Database:
    def __init__(self, config):
        self.host = config.db_host
        self.username = config.db_user
        self.password = config.db_pass
        self.dbname = config.db_name
        self.port = config.db_port
        self.conn = None

    def connect(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(
                        host=self.host,
                        user=self.username,
                        password=self.password,
                        database=self.dbname,
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor
                    )
        except pymysql.MySQLError as e:
            logging.error(e)
            raise Exception(e)
        finally:
            logging.info('Database connection success.')

    def query(self, query):
        try:
            self.connect()
            with self.conn.cursor() as cur:
                records = []
                cur.execute(query)
                result = cur.fetchall()
                for row in result:
                    records.append(row)
                cur.close()
                return records
        except pymysql.MySQLError as e:
            logging.error(e)
            print(e)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                logging.info('Database connection closed.')
