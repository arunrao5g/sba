import pymysql
from utils.generic import USR, PWD, HOST

class CreateSession:
    @staticmethod
    def connect(database):
        return pymysql.connect(host=HOST, user=USR, passwd=PWD, db=database)
